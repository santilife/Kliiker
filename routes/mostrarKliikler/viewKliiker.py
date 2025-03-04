# routes/mostrarKliikler/viewKliiker.py
from flask import render_template, Blueprint
from database.config import mysql

kliiker_table = Blueprint("kliiker_table", __name__)

def obtener_datos():
    try:
        cursor = mysql.connection.cursor()
        
        # Verificar primero si la tabla existe
        cursor.execute("SHOW TABLES LIKE 'kliiker'")
        if not cursor.fetchone():
            raise Exception("La tabla 'kliiker' no existe en la base de datos")
        
        consulta = """
            SELECT 
                id_kliiker,
                nombre,
                apellido,
                celular,
                codigo,
                correo,
                fecha,
                venta
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

@kliiker_table.route("/ver-kliikers")
# @login_required
def mostrar_tabla():
    datos = obtener_datos()
    return render_template("/admin/index.html", datos=datos)