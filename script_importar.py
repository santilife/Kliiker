# Importación de bibliotecas necesarias
from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
import json

# Crear instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de la conexión a MySQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "kliiker1"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Inicializar la conexión MySQL
mysql = MySQL(app)


def importar_datos_desde_json():
    """
    Importa datos desde un archivo JSON a la base de datos MySQL,
    validando números celulares y evitando duplicados.
    """
    try:
        # Abrir y leer el archivo JSON
        with open(
            f"Kliiker_{datetime.now().strftime('%d-%m-%Y')}.json", "r", encoding="utf-8"
        ) as file:
            datos = json.load(file)

        # Crear contexto de aplicación
        with app.app_context():
            cursor = mysql.connection.cursor()

            # Obtener celulares existentes en la base de datos
            cursor.execute("SELECT celular FROM kliiker")
            existing_celulares = {row["celular"] for row in cursor.fetchall()}

            # Conjunto para trackear celulares procesados del JSON
            processed_celulares = set()

            # Contadores para estadísticas
            registros_insertados = 0
            registros_invalidos = 0

            for registro in datos:
                celular = registro.get("celular", "").strip()

                # ========== Validaciones de celular ==========
                # 1. Celular vacío
                if not celular:
                    print("Registro sin celular. Omitiendo.")
                    registros_invalidos += 1
                    continue

                # 2. Validar que sea numérico
                if not celular.isdigit():
                    print(f"Celular no numérico: {celular}. Omitiendo.")
                    registros_invalidos += 1
                    continue

                # 3. Convertir a número y validar rango
                try:
                    num_celular = int(celular)
                except ValueError:
                    print(f"Formato de celular inválido: {celular}. Omitiendo.")
                    registros_invalidos += 1
                    continue

                # 4. Validar rango 3000000000 - 3999999999
                if not (3000000000 <= num_celular <= 3999999999):
                    print(f"Celular fuera de rango válido: {celular}. Omitiendo.")
                    registros_invalidos += 1
                    continue

                # 5. Verificar duplicados en DB y JSON
                if celular in existing_celulares or celular in processed_celulares:
                    print(f"Duplicado: {celular} - Omitiendo registro")
                    registros_invalidos += 1
                    continue
                # ========== Fin validaciones ==========

                # Procesar fecha
                fecha_mysql = None
                if registro.get("fecha_de_registro"):
                    try:
                        fecha_original = registro["fecha_de_registro"]
                        fecha_mysql = datetime.strptime(
                            fecha_original, "%d/%m/%Y"
                        ).strftime("%Y-%m-%d")
                    except ValueError as e:
                        print(f"Error en fecha {fecha_original}: {str(e)}")

                # Construir registro para inserción
                valores = (
                    registro.get("id_kliiker") or None,  # id_Kliiker
                    registro.get("nombres", "").strip(),  # nombre
                    registro.get("apellidos", "").strip(),  # apellido
                    celular,  # celular validado
                    registro.get("codigo", "").strip(),  # nivel
                    registro.get("correo_electronico", "").strip(),  # correo
                    fecha_mysql,  # fecha
                    registro.get("ventas", 0),  # venta
                )

                # Ejecutar inserción
                try:
                    cursor.execute(
                        """INSERT INTO kliiker (
                            id_Kliiker, nombre, apellido, celular,
                            nivel, correo, fecha, venta
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        valores,
                    )
                    registros_insertados += 1
                    processed_celulares.add(celular)
                except Exception as e:
                    print(f"Error insertando registro {celular}: {str(e)}")
                    registros_invalidos += 1

            # Confirmar cambios y cerrar conexión
            mysql.connection.commit()
            cursor.close()

            # Reporte final
            print(f"\nProceso completado:")
            print(f"- Registros insertados: {registros_insertados}")
            print(f"- Registros omitidos: {registros_invalidos}")
            return True

    except Exception as e:
        print(f"\nError crítico: {str(e)}")
        return False


# Punto de entrada principal
if __name__ == "__main__":
    importar_datos_desde_json()
