# En tu archivo de rutas (ej: estadisticas.py)
from flask import Blueprint, jsonify, render_template
from database.config import mysql
import plotly.express as px
import plotly.io as pio
import MySQLdb

estadisticas_bp = Blueprint('estadisticas', __name__)

def obtener_datos_estadisticas():
    try:
        connection = mysql.connection
        cursor = connection.cursor()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        # Consulta para estados
        cursor.execute("""
            SELECT id_estado, COUNT(*) as cantidad 
            FROM gestiones 
            GROUP BY id_estado
        """)
        datos_estados = cursor.fetchall()
        
        # Consulta para tipificaciones
        cursor.execute("""
            SELECT tipificacion, COUNT(*) as cantidad 
            FROM gestiones 
            WHERE tipificacion IS NOT NULL
            GROUP BY tipificacion
        """)
        datos_tipificaciones = cursor.fetchall()
        
        print(datos_estados)
        print(datos_tipificaciones)
        cursor.close()
        return {
            'estados': datos_estados,
            'tipificaciones': datos_tipificaciones
        }
    except MySQLdb.Error as e:
        print(f"Error de base de datos: {e}")
        return None

@estadisticas_bp.route('/datos_estadisticas')
def obtener_datos():
    datos = obtener_datos_estadisticas()
    return jsonify(datos)

@estadisticas_bp.route('/graficos')
def mostrar_graficos():
    return render_template('estadisticas/estadisticas.html')