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
            SELECT 
            SUM(CASE WHEN nivel = 1 THEN 1 ELSE 0 END) as con_codigo,
            SUM(CASE WHEN nivel = 0 THEN 1 ELSE 0 END) as sin_codigo
            FROM kliiker
            """
        )
        datos_codigo = cursor.fetchone()

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
            SELECT COUNT(*) as rpc_exitosos
            FROM gestiones g
            JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
            WHERE t.rpc = 1
        """
        )
        datos_rpc = cursor.fetchone()

        # Consulta Contactabilidad
        cursor.execute(
            """
            SELECT COUNT(*) as cantidadContac
            FROM gestiones g
            JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
            WHERE t.contactabilidad = 1
        """
        )
        datos_contactabilidad = cursor.fetchone()

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

        # Sin Gestion
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

        # Cantidad Gestionados
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

        # Gestiones Totales
        cursor.execute("SELECT COUNT(*) AS gestionesTotales FROM historial_gestiones")
        gestionesTotales = cursor.fetchall()

        # Cierre Flujo
        cursor.execute(
            """
            SELECT t.cierre_flujo, COUNT(*) AS cantCierreFlujo
            FROM gestiones g              
            JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
            JOIN estadoKliiker e ON g.id_estado = e.id_estado
            WHERE e.cierre_flujo = 1 OR t.cierre_flujo = 1;
            """
        )
        datos_cierreFlujo = cursor.fetchall()

        # Gestionables

        cursor.execute(
            """
            SELECT COUNT(*) as gestionables
            FROM kliiker k
            WHERE NOT EXISTS (
                SELECT 1
                FROM gestiones g
                JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion
                WHERE g.celular = k.celular
                AND t.tipificacion IN (
                    'Sin interes', 
                    'Equivocado', 
                    'Interesado a futuro', 
                    'Lead ya compro'
                )
            )
            """
        )
        datos_gestionables = cursor.fetchall()

        ventas_exitosas = (
            datos_venta[0]["ventasExitosas"] if datos_venta and datos_venta[0] else 0
        )
        gestionados = (
            datos_gestionados[0]["cantidadGestionados"]
            if datos_gestionados and datos_gestionados[0]
            else 0
        )
        rpc_exitosos = datos_rpc["rpc_exitosos"] if datos_rpc else 0

        # Cálculos seguros
        conversion = (ventas_exitosas / rpc_exitosos * 100) if rpc_exitosos > 0 else 0

        efectividad = (ventas_exitosas / gestionados * 100) if gestionados > 0 else 0

        gestiones_totales = (
            gestionesTotales[0]["gestionesTotales"]
            if gestionesTotales and gestionesTotales[0]
            else 0
        )

        contactabilidad = (
            datos_contactabilidad["cantidadContac"] if datos_contactabilidad else 0
        )

        contactabilidad_porcentaje = (
            (contactabilidad / gestiones_totales * 100) if gestiones_totales > 0 else 0
        )

        rpc_porcentaje = (
            (rpc_exitosos / gestiones_totales * 100) if gestiones_totales > 0 else 0
        )

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
        # print(datos_cierreFlujo)
        # print(datos_gestionables)
        cursor.close()

        return {
            "estados": datos_estados,
            "tipificaciones": datos_tipificaciones,
            "rpc": datos_rpc,
            "codigos": datos_codigo,
            "ventas": datos_venta,
            "total_kliikers": datos_total,
            "cantidadGestiones": datos_gestiones,
            "contactabilidad": (
                datos_contactabilidad["cantidadContac"] if datos_contactabilidad else 0
            ),
            "sinInteres": datos_sinInteres,
            "sinGestion": datos_sinGestion,
            "gestionados": datos_gestionados,
            "gestionesTotales": gestionesTotales,
            "cierreFlujo": datos_cierreFlujo,
            "gestionables": datos_gestionables,
            "efectividad": round(efectividad, 3),
            "conversion": round(conversion, 3),
            "ventas_exitosas": ventas_exitosas,
            "rpc_exitosos": rpc_exitosos,
            "gestionados_total": gestionados,
            "contactabilidad_porcentaje": round(contactabilidad_porcentaje, 3),
            "rpc_porcentaje": round(rpc_porcentaje, 3),
            "gestiones_totales": gestiones_totales,
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


# ------------------------------------------------------------------------------------------------------
