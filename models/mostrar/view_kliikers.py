from flask import render_template, Blueprint, Flask
from database.config import mysql
from datetime import datetime

app = Flask(__name__)
kliiker_table = Blueprint("kliiker_table", __name__)


def obtener_datos():
    try:
        cursor = mysql.connection.cursor()

        # Verificar primero si la tabla existe
        cursor.execute("SHOW TABLES LIKE 'kliker'")
        if not cursor.fetchone():
            raise Exception("La tabla 'kliker' no existe en la base de datos")

        consulta = """
            SELECT
                id_Kliiker,
                nombre,
                apellido,
                celular,
                nivel
            FROM kliiker
            ORDER BY fecha DESC
        """
        cursor.execute(consulta)

        # Obtener metadatos ANTES de cerrar el cursor
        column_names = [column[0] for column in cursor.description]
        datos = cursor.fetchall()

        # Convertir resultados a diccionarios
        resultados = [dict(zip(column_names, row)) for row in datos]

        cursor.close()

        return resultados

    except Exception as err:
        print(f"Error al obtener datos: {str(err)}")
        return []


# def obtener_datos():
#     try:
#         cursor = mysql.connection.cursor()

#         # Verificar primero si la tabla existe
#         cursor.execute("SHOW TABLES LIKE 'kliiker'")
#         if not cursor.fetchone():
#             raise Exception("La tabla 'kliiker' no existe en la base de datos")

#         consulta = """
#             SELECT
#                 k.id_Kliiker AS idKliiker,
#                 k.nombre,
#                 k.apellido,
#                 k.celular,
#                 k.id_Kliiker,
#                 g.canal,
#                 g.tipoGestion AS tipo_gestor,
#                 g.fecha,
#                 g.comentario,
#                 u.nombre_AS AS asesor,
#                 t.tipificacion
#             FROM kliker k
#             LEFT JOIN gestiones g ON k.celular = g.celular
#             LEFT JOIN usuarios u ON g.nombre_AS = u.nombre_AS
#             LEFT JOIN tipificacion t ON g.tipificacion = t.tipificacion
#             ORDER BY g.fecha DESC
#         """
#         cursor.execute(consulta)

#         # Obtener metadatos ANTES de cerrar el cursor
#         column_names = [column[0] for column in cursor.description]
#         datos = cursor.fetchall()

#         # Convertir resultados a diccionarios
#         resultados = [dict(zip(column_names, row)) for row in datos]

#         cursor.close()

#         return resultados

#     except Exception as err:
#         print(f"Error al obtener datos: {str(err)}")
#         return []


def mostrar_tabla():
    datos = obtener_datos()
    return render_template("/formGestion/gestion.html", datos=datos)
