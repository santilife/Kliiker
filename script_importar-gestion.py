from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
import json
import re

app = Flask(__name__)

# Configuración de conexión
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "kliiker1"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


def validar_celular(celular):
    """Valida que el celular sea numérico y esté en rango válido (3000000000 - 3999999999)"""
    try:
        num = int(celular)
        return 3000000000 <= num <= 3999999999
    except (ValueError, TypeError):
        return False


def importar_gestiones_simple():
    try:
        with open(
            f"Gestion_{datetime.now().strftime('%d-%m-%Y')}.json",
            "r",
            encoding="utf-8",
        ) as file:
            gestiones = json.load(file)

        registros_insertados = 0
        registros_invalidos = 0

        with app.app_context():
            cursor = mysql.connection.cursor()

            # Obtener datos de referencia para validaciones
            cursor.execute("SELECT id_tipificacion FROM tipificacion")
            valid_tipificaciones = {row["id_tipificacion"] for row in cursor.fetchall()}

            cursor.execute("SELECT id_estado FROM estadokliiker")
            valid_estados = {row["id_estado"] for row in cursor.fetchall()}

            cursor.execute("SELECT id_llamada FROM gestiones")
            existing_llamadas = {row["id_llamada"] for row in cursor.fetchall()}

            for gestion in gestiones:
                errores = []

                # Validación de campos obligatorios
                campos_obligatorios = [
                    "id_llamada",
                    "nombre_as",
                    "id_tipificacion",
                    "id_estado",
                ]
                for campo in campos_obligatorios:
                    if not gestion.get(campo):
                        errores.append(f"Campo obligatorio faltante: {campo}")

                # Validación de FK
                if gestion.get("id_tipificacion") not in valid_tipificaciones:
                    errores.append("id_tipificacion inválido")

                if gestion.get("id_estado") not in valid_estados:
                    errores.append("id_estado inválido")

                # Validar unicidad de id_llamada
                if gestion.get("id_llamada") in existing_llamadas:
                    errores.append("id_llamada duplicado")

                # Validación de celular
                if gestion.get("celular") and not validar_celular(gestion["celular"]):
                    errores.append("Celular inválido")

                # Manejo de fechas
                fecha = None
                if gestion.get("fecha"):
                    try:
                        fecha = datetime.strptime(gestion["fecha"], "%d/%m/%Y").date()
                    except ValueError:
                        errores.append("Formato de fecha inválido (DD/MM/YYYY)")

                fecha_proxima = None
                if gestion.get("fechaproximagestion"):
                    try:
                        fecha_proxima = datetime.strptime(
                            gestion["fechaproximagestion"], "%d/%m/%Y"
                        ).date()
                    except ValueError:
                        errores.append("Formato de fecha próxima inválido (DD/MM/YYYY)")

                # Si hay errores, omitir registro
                if errores:
                    print(
                        f"Registro {gestion.get('id_llamada')} inválido - Errores: {', '.join(errores)}"
                    )
                    registros_invalidos += 1
                    continue

                try:
                    cursor.execute(
                        """
                        INSERT INTO gestiones (
                            id_llamada, fecha, canal, tipoGestion, comentario,
                            fechaProximaGestion, nombre_AS, id_tipificacion,
                            motivoNoInteres, id_estado, celular
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            gestion["id_llamada"],
                            fecha,
                            gestion.get("canal"),
                            gestion.get("tipogestion"),
                            gestion.get("comentario"),
                            fecha_proxima,
                            gestion["nombre_as"],
                            gestion["id_tipificacion"],
                            gestion.get("motivonointeres"),
                            gestion["id_estado"],
                            gestion.get("celular"),
                        ),
                    )
                    registros_insertados += 1
                    existing_llamadas.add(gestion["id_llamada"])  # Actualizar cache

                except Exception as e:
                    print(f"Error insertando {gestion.get('id_llamada')}: {str(e)}")
                    registros_invalidos += 1

            mysql.connection.commit()
            print(f"\nResultado final:")
            print(f"✅ Registros insertados: {registros_insertados}")
            print(f"❌ Registros omitidos: {registros_invalidos}")
            return True

    except Exception as e:
        print(f"\nError crítico: {str(e)}")
        return False


if __name__ == "__main__":
    importar_gestiones_simple()
