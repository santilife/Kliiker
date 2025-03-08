from flask import Blueprint, url_for, render_template
from database.config import mysql



# @asesores_tables.route("/asesores_tables")
# def index():  #     return render_template("mostrar/view_usersAS.html")
#     return render_template("/asesores/index.html")


# Función para obtener la lista de asesores desde la base de datos
def obtener_asesores():
    try:
        cursor = mysql.connection.cursor()

        # Verifica si existe la tabla usuarios
        cursor.execute("SHOW TABLES LIKE 'usuarios'")
        if not cursor.fetchone():
            raise Exception("Tabla 'usuarios' no existe")

        # Consulta para obtener información básica de los asesores
        consulta = """
            SELECT
                nombre_AS,
                documento,
                usuario,
                rol
            FROM usuarios
            
        """
        cursor.execute(consulta)

        column_names = [column[0] for column in cursor.description]
        datos = cursor.fetchall()
        print(datos)
        # Convertir a diccionarios (HABILITAR)
        # resultados = [dict(zip(column_names, row)) for row in datos]

        cursor.close()
        # return resultados
        return datos
    except Exception as err:
        print(f"Error en obtener_datos_gestion: {str(err)}")
        return []


# Creación del Blueprint para las rutas de asesores
mostrar_asesores_tables = Blueprint("mostrar_asesores_tables", __name__)


# Ruta para mostrar la tabla de asesores
@mostrar_asesores_tables.route("/mostrar_asesores_tables")
def mostrar_asesores():
    datos = obtener_asesores()
    return render_template("/asesores/index.html", datos=datos)
