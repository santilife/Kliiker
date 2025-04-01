from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
import json
import os
import glob
import sys

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "kliiker1"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


def obtener_ultimo_json():
    """Busca el archivo JSON más reciente en temp_uploads"""
    upload_dir = "temp_uploads"
    json_files = glob.glob(os.path.join(upload_dir, "Kliiker_*.json"))

    if not json_files:
        raise FileNotFoundError("No se encontraron archivos JSON en temp_uploads")

    return max(json_files, key=os.path.getctime)


def limpiar_celular(celular):
    """Limpia caracteres no numéricos y valida formato"""
    return "".join(filter(str.isdigit, str(celular))).lstrip("0")


def importar_datos_desde_json():
    try:
        json_path = obtener_ultimo_json()

        with open(json_path, "r", encoding="utf-8") as file:
            datos = json.load(file)

        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT celular FROM kliiker")
            existing_celulares = {str(row["celular"]) for row in cursor.fetchall()}

            processed_celulares = set()
            registros_insertados = 0
            registros_invalidos = 0

            for idx, registro in enumerate(datos, 1):
                try:
                    # Limpieza y validación de celular
                    raw_celular = registro.get("celular", "")
                    celular = limpiar_celular(raw_celular)

                    # Validación de celular obligatorio
                    if not celular:
                        print(f"Registro {idx}: Celular vacío - Omitido")
                        registros_invalidos += 1
                        continue

                    if not (3000000000 <= int(celular) <= 3999999999):
                        print(f"Registro {idx}: Celular {celular} fuera de rango")
                        registros_invalidos += 1
                        continue

                    if celular in existing_celulares or celular in processed_celulares:
                        print(f"Registro {idx}: Celular {celular} duplicado")
                        registros_invalidos += 1
                        continue

                    # Procesamiento de fecha
                    fecha_mysql = None
                    fecha_raw = registro.get("fecha_de_registro", "")
                    if fecha_raw:
                        try:
                            fecha_mysql = datetime.strptime(
                                str(fecha_raw), "%d/%m/%Y"
                            ).date()
                        except Exception as e:
                            print(
                                f"Registro {idx}: Error en fecha {fecha_raw} - {str(e)}"
                            )
                            fecha_mysql = None

                    # Manejo de ID_Kliiker (campo obligatorio)
                    id_kliiker = registro.get("id_kliiker")

                    # Asignar valor por defecto si no existe o está vacío
                    if not id_kliiker:
                        id_kliiker = f"SIN_ID_{idx}"  # ID único temporal

                    # Validar y limpiar otros campos
                    nombres = str(registro.get("nombres", "")).strip() or "Sin nombre"
                    apellidos = (
                        str(registro.get("apellidos", "")).strip() or "Sin apellido"
                    )
                    codigo = str(registro.get("codigo", "")).strip() or "Sin código"
                    correo = (
                        str(registro.get("correo_electronico", "")).strip()
                        or "Sin correo"
                    )
                    ventas = registro.get("ventas", 0) or 0

                    # Inserción de datos
                    valores = (
                        id_kliiker,
                        nombres,
                        apellidos,
                        celular,
                        codigo,
                        correo,
                        fecha_mysql,
                        ventas,
                    )

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
                    registros_invalidos += 1
                    print(f"Registro {idx}: Error crítico - {str(e)}")
                    print(f"Datos del registro: {registro}")

            mysql.connection.commit()
            cursor.close()

            print(
                f"\n[EXITO] Importación completada desde: {os.path.basename(json_path)}"
            )
            print(f"Registros insertados: {registros_insertados}")
            print(f"Registros omitidos: {registros_invalidos}")
            return True

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        return False


if __name__ == "__main__":
    if not os.path.exists("temp_uploads"):
        os.makedirs("temp_uploads")

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    importar_datos_desde_json()
