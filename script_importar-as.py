from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
import json
import random

app = Flask(__name__)

# Configuración de conexión
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "kliiker1"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


def importar_gestiones_simple():
    try:
        with open(
            f"Gestion_{datetime.now().strftime('%d-%m-%Y')}.json",
            "r",
            encoding="utf-8",
        ) as file:
            gestiones = json.load(file)

        rol = "Asesor"
        registros_insertados = 0
        registros_invalidos = 0

        with app.app_context():
            cursor = mysql.connection.cursor()

            # Obtener datos existentes
            cursor.execute("SELECT documento, nombre_AS FROM usuarios")
            existing_data = cursor.fetchall()
            existing_documentos = {row["documento"] for row in existing_data}
            existing_nombres = {row["nombre_AS"] for row in existing_data}

            processed_documentos = set()
            processed_nombres = set()

            for gestion in gestiones:
                nombre_as = gestion.get("nombre_as", "").strip()

                # ========== Validaciones de nombre_as ==========
                # 1. Nombre vacío
                if not nombre_as:
                    print("Registro sin nombre_as. Omitiendo.")
                    registros_invalidos += 1
                    continue

                # 2. Verificar duplicados en DB y JSON
                if nombre_as in existing_nombres or nombre_as in processed_nombres:
                    print(f"Duplicado: {nombre_as} - Omitiendo registro")
                    registros_invalidos += 1
                    continue

                # Marcar como procesado antes de insertar
                processed_nombres.add(nombre_as)
                # ========== Fin validaciones ==========

                # Generar documento único
                documento = None
                for _ in range(10):
                    doc_temp = random.randint(10**9, 10**10 - 1)
                    if (
                        doc_temp not in existing_documentos
                        and doc_temp not in processed_documentos
                    ):
                        documento = doc_temp
                        break

                if not documento:
                    print(f"Error: No se pudo generar documento único para {nombre_as}")
                    registros_invalidos += 1
                    continue

                # Validar formato del documento
                if not (10**9 <= documento <= 10**10 - 1):
                    print(f"Documento inválido: {documento}")
                    registros_invalidos += 1
                    continue

                # Insertar registro
                try:
                    cursor.execute(
                        """
                        INSERT INTO usuarios (
                            nombre_AS, documento, password, usuario, rol, estadoUsuario
                        ) VALUES (%s, %s, 12345, %s, %s, 1)
                        """,
                        (nombre_as, documento, nombre_as, rol),
                    )
                    registros_insertados += 1
                    processed_documentos.add(documento)
                except Exception as e:
                    print(f"Error insertando {nombre_as}: {str(e)}")
                    registros_invalidos += 1

            mysql.connection.commit()
            print(f"\nResumen final:")
            print(f"- Registros insertados: {registros_insertados}")
            print(f"- Registros omitidos: {registros_invalidos}")
            return True

    except Exception as e:
        print(f"\nError crítico: {str(e)}")
        return False


if __name__ == "__main__":
    importar_gestiones_simple()
