# En tu archivo de rutas (ej: estadisticas.py)
from flask import Blueprint, jsonify, render_template
from database.config import mysql

# import plotly.express as px
# import plotly.io as pio
import MySQLdb
from flask import current_app

# from models.mostrar.view_kliikers import total_gestiones

estadisticas_bp = Blueprint("estadisticas", __name__)


def obtener_datos_estadisticas():
    # gestiones_totales = total_gestiones()
    try:
        connection = mysql.connection
        # cursor = connection.cursor()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        # Consulta para estados
        cursor.execute(
            """
            SELECT g.id_estado, e.estado, COUNT(*) as cantidadEstados
            FROM gestiones g
            JOIN estadoKliiker e ON g.id_estado = e.id_estado 
            GROUP BY g.id_estado
        """
        )
        datos_estados = cursor.fetchall()

        # Consulta para tipificaciones
        cursor.execute(
            """
            SELECT t.tipificacion, COUNT(*) as cantidadTipificaciones
            FROM gestiones g
            JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
            GROUP BY t.tipificacion
        """
        )
        datos_tipificaciones = cursor.fetchall()

        # Consulta Sin interes
        cursor.execute(
            """
                SELECT COUNT(*) as cantSinInteres
                FROM gestiones g
                # JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
                WHERE g.id_tipificacion = 10
                
            
            """
        )
        datos_sinInteres = cursor.fetchall()

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

        # Consulta RPC
        cursor.execute(
            """
            SELECT t.rpc, COUNT(*) as cantidadRPC
            FROM gestiones g
            JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
            GROUP BY t.rpc
        """
        )
        datos_rpc = cursor.fetchall()

        # Consulta Contactabilidad
        cursor.execute(
            """
            SELECT t.contactabilidad, COUNT(*) as cantidadContac
            FROM gestiones g
            JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
            GROUP BY t.contactabilidad
        """
        )
        datos_contactabilidad = cursor.fetchall()

        # Consulta total
        cursor.execute(
            """
            SELECT COUNT(*) as total
            FROM kliiker
            """
        )

        datos_total = cursor.fetchall()

        # consulta de gestiones totales
        cursor.execute(
            """
            SELECT COUNT(*) as cantidadGestiones
            FROM historial_gestiones 
            """
        )
        datos_gestiones = cursor.fetchall()

        cursor.execute(
            """
           SELECT COUNT(*) as cantidadSinGestion
            FROM kliiker k
            WHERE NOT EXISTS (
            SELECT 1
                FROM historial_gestiones h
                WHERE h.celular = k.celular
            );
            """
        )
        datos_sinGestion = cursor.fetchall()

        cursor.execute(
            """
            SELECT COUNT(*) AS cantidadGestionados
            FROM kliiker k
            WHERE EXISTS (
            SELECT 1
            FROM historial_gestiones h
            WHERE h.celular = k.celular
            );
            """
        )
        datos_gestionados = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS gestionesTotales FROM historial_gestiones")
        gestionesTotales = cursor.fetchall()

        # consulta gestionados
        # consulta registros
        # consulta codigo fin
        # consulta sin gestión
        # consulta sin interes

        # print(datos_total)
        # print(datos_venta)
        # print(datos_codigo)
        # print(datos_estados)
        # print(datos_tipificaciones)
        # print(datos_rpc)
        # print(datos_contactabilidad)
        # print(datos_gestiones)
        # print(datos_sinInteres)
        # print(gestiones_totales)
        # print(datos_sinGestion)
        # print(datos_gestionados)
        # print(gestionesTotales)
        cursor.close()

        return {
            "estados": datos_estados,
            "tipificaciones": datos_tipificaciones,
            "rpc": datos_rpc,
            "codigos": datos_codigo,
            "ventas": datos_venta,
            "total_kliikers": datos_total,
            "cantidadGestiones": datos_gestiones,
            "cantidadContac": datos_contactabilidad,
            "sinInteres": datos_sinInteres,
            "sinGestion": datos_sinGestion,
            "gestionados": datos_gestionados,
            "gestionesTotales": gestionesTotales,
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
