from flask import Blueprint, url_for, render_template
from database.config import mysql

asesores_tables = Blueprint("asesores_tables", __name__)


@asesores_tables.route("/asesores_tables")
def index():  #     return render_template("mostrar/view_usersAS.html")
    return render_template("/asesores/index.html")


def obtener_asesores():
    try:
        cursor = mysql.connection.cursor()

        cursor.execute("SHOW TABLES LIKE 'usuarios'")
        if not cursor.fetchone():
            raise Exception("Tabla 'kliiker' no existe")

        consulta = """
            SELECT
                nombre,
                documento,
                usuario,
                rol
            FROM usuarios
            
        """
        cursor.execute(consulta)

        column_names = [column[0] for column in cursor.description]
        datos = cursor.fetchall()

        # Convertir a diccionarios (HABILITAR)
        # resultados = [dict(zip(column_names, row)) for row in datos]

        cursor.close()
        # return resultados
        return datos
    except Exception as err:
        print(f"Error en obtener_datos_gestion: {str(err)}")
        return []


mostrar_asesores = Blueprint("mostrar_asesores", __name__)


@mostrar_asesores.route("/mostrar_asesores")
def index():
    datos = obtener_asesores()
    return render_template("/asesores/index.html", datos=datos)
