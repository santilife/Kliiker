# En tu archivo de rutas (ej: estadisticas.py)
from flask import Blueprint, jsonify, render_template
from database.config import mysql
import plotly.express as px
import plotly.io as pio
import MySQLdb

estadisticas_bp = Blueprint("estadisticas", __name__)


def obtener_datos_estadisticas():
    try:
        connection = mysql.connection
        cursor = connection.cursor()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        # Consulta para estados
        cursor.execute(
            """
            SELECT id_estado, COUNT(*) as cantidadEstados
            FROM kliiker 
            GROUP BY id_estado
        """
        )
        datos_estados = cursor.fetchall()

        # Consulta para tipificaciones
        cursor.execute(
            """
            SELECT tipificacion, COUNT(*) as cantidadTipificaciones
            FROM gestiones 
            GROUP BY tipificacion
        """
        )
        datos_tipificaciones = cursor.fetchall()

        # Consulta Codigo
        cursor.execute(
            """
            SELECT nivel, COUNT(*) as cantidadCodigos
            FROM kliiker
            GROUP BY nivel
            """
        )
        datos_codigo = cursor.fetchall()

        # Consulta venta
        cursor.execute(
            """
            SELECT 
            SUM(venta) as total_ventas,
            COUNT(CASE WHEN venta = 1 THEN 1 END) as ventasExitosas,
            COUNT(CASE WHEN venta = 0 THEN 1 END) as sinVenta
            FROM kliiker
            """
        )
        datos_venta = cursor.fetchall()

        # Consulta total
        cursor.execute(
            """
            SELECT COUNT(*) as total
            FROM kliiker
            """
        )
        datos_total = cursor.fetchall()

        print(datos_total)
        print(datos_venta)
        print(datos_codigo)
        print(datos_estados)
        print(datos_tipificaciones)

        cursor.close()

        return {
            "estados": datos_estados,
            "tipificaciones": datos_tipificaciones,
            "codigos": datos_codigo,
            "ventas": datos_venta,
            "total_kliikers": datos_total,
        }
    except MySQLdb.Error as e:
        print(f"Error de base de datos: {e}")
        return None


@estadisticas_bp.route("/datos_estadisticas")
def obtener_datos():
    datos = obtener_datos_estadisticas()
    return jsonify(datos)


@estadisticas_bp.route("/graficos")
def mostrar_graficos():
    datos = obtener_datos_estadisticas()
    return render_template("estadisticas/estadisticas.html", datos=datos)
