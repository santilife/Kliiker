# En tu archivo de rutas (ej: estadisticas.py)
from flask import Blueprint, jsonify, render_template, request
from database.config import mysql

# import plotly.express as px
# import plotly.io as pio
import MySQLdb
from flask import current_app

# from models.mostrar.view_kliikers import total_gestiones

estadisticas_bp = Blueprint("estadisticas", __name__)


def obtener_datos_estadisticas(
    fecha_inicio=None, fecha_final=None, nivel=None, estado=None, tipificacion=None
):
    # gestiones_totales = total_gestiones()
    try:
        connection = mysql.connection
        # cursor = connection.cursor()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)

        # Construir condiciones de filtro
        where_conditions = []
        params = []

        # Filtro por fecha para gestiones
        date_condition_gestiones = ""
        if fecha_inicio and fecha_final:
            date_condition_gestiones = " WHERE g.fecha BETWEEN %s AND %s "
            params.extend([fecha_inicio, fecha_final])
        elif fecha_inicio:
            date_condition_gestiones = " WHERE g.fecha >= %s "
            params.append(fecha_inicio)
        elif fecha_final:
            date_condition_gestiones = " WHERE g.fecha <= %s "
            params.append(fecha_final)

        # Filtro por estado
        estado_condition = ""
        if estado and estado != "Todo":
            if date_condition_gestiones:
                estado_condition = " AND g.id_estado = %s "
            else:
                estado_condition = " WHERE g.id_estado = %s "
            params.append(estado)

        # Filtro por tipificación
        tipificacion_condition = ""
        if tipificacion and tipificacion != "Todo":
            if date_condition_gestiones or estado_condition:
                tipificacion_condition = " AND g.id_tipificacion = %s "
            else:
                tipificacion_condition = " WHERE g.id_tipificacion = %s "
            params.append(tipificacion)

        # Filtro por nivel (con código/sin código) para kliiker
        nivel_condition = ""
        nivel_params = []
        if nivel:
            # Adjust the nivel value for the query
            # In the select, nivel=1 is "Con codigo" and nivel=0 is "Sin codigo"
            # But in the dropdown, value 1 is "Con codigo" and value 2 is "Sin codigo"
            nivel_value = 0 if nivel == "2" else 1
            nivel_condition = " WHERE nivel = %s "
            nivel_params.append(nivel_value)

        # Consulta para estados
        query_estados = (
            """
            SELECT g.id_estado, e.estado, COUNT(*) as cantidadEstados
            FROM gestiones g
            JOIN estadoKliiker e ON g.id_estado = e.id_estado 
            """
            + date_condition_gestiones
            + estado_condition
            + tipificacion_condition
            + """
            GROUP BY g.id_estado
        """
        )
        cursor.execute(query_estados, params[:])
        datos_estados = cursor.fetchall()

        # Consulta para tipificaciones
        query_tipificaciones = (
            """
            SELECT t.tipificacion, COUNT(*) as cantidadTipificaciones
            FROM gestiones g
            JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
            """
            + date_condition_gestiones
            + estado_condition
            + tipificacion_condition
            + """
            GROUP BY t.tipificacion
        """
        )
        cursor.execute(query_tipificaciones, params[:])
        datos_tipificaciones = cursor.fetchall()

        # Consulta Sin interes
        query_sin_interes = """
            SELECT COUNT(*) as cantSinInteres
            FROM gestiones g
            # JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
            WHERE g.id_tipificacion = 10
            """
        if date_condition_gestiones or estado_condition or tipificacion_condition:
            query_sin_interes = query_sin_interes.replace("WHERE", "AND")
            query_sin_interes = (
                """
                SELECT COUNT(*) as cantSinInteres
                FROM gestiones g
                """
                + date_condition_gestiones
                + estado_condition
                + tipificacion_condition
                + """
                AND g.id_tipificacion = 10
                """
            )
        cursor.execute(query_sin_interes, params[:])
        datos_sinInteres = cursor.fetchall()

        # Consulta Codigo
        query_codigo = """
            SELECT 
            SUM(CASE WHEN nivel = 1 THEN 1 ELSE 0 END) as con_codigo,
            SUM(CASE WHEN nivel = 0 THEN 1 ELSE 0 END) as sin_codigo
            FROM kliiker
            """ + (
            nivel_condition if nivel else ""
        )
        cursor.execute(query_codigo, nivel_params)
        datos_codigo = cursor.fetchone()

        # Resto de consultas con filtros similares
        # ... (aplicar los filtros a las demás consultas)

        # Consulta venta
        query_venta = (
            """
            SELECT 
            SUM(venta) as total_ventas,
            COUNT(CASE WHEN venta = 1 THEN 1 END) as ventasExitosas,
            COUNT(CASE WHEN venta = 0 THEN 1 END) as sinVenta
            FROM kliiker
            """
            + nivel_condition
        )
        cursor.execute(query_venta, nivel_params)
        datos_venta = cursor.fetchall()

        # Consulta RPC
        query_rpc = """
            SELECT COUNT(*) as rpc_exitosos
            FROM gestiones g
            JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
            WHERE t.rpc = 1
        """
        if date_condition_gestiones or estado_condition or tipificacion_condition:
            query_rpc = query_rpc.replace("WHERE", "AND")
            query_rpc = (
                """
                SELECT COUNT(*) as rpc_exitosos
                FROM gestiones g
                JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
                """
                + date_condition_gestiones
                + estado_condition
                + tipificacion_condition
                + """
                AND t.rpc = 1
                """
            )
        cursor.execute(query_rpc, params[:])
        datos_rpc = cursor.fetchone()

        # Consulta Contactabilidad
        query_contactabilidad = """
            SELECT COUNT(*) as cantidadContac
            FROM gestiones g
            JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
            WHERE t.contactabilidad = 1
        """
        if date_condition_gestiones or estado_condition or tipificacion_condition:
            query_contactabilidad = query_contactabilidad.replace("WHERE", "AND")
            query_contactabilidad = (
                """
                SELECT COUNT(*) as cantidadContac
                FROM gestiones g
                JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
                """
                + date_condition_gestiones
                + estado_condition
                + tipificacion_condition
                + """
                AND t.contactabilidad = 1
                """
            )
        cursor.execute(query_contactabilidad, params[:])
        datos_contactabilidad = cursor.fetchone()

        # Consulta total
        query_total = (
            """
            SELECT COUNT(*) as total
            FROM kliiker
            """
            + nivel_condition
        )
        cursor.execute(query_total, nivel_params)
        datos_total = cursor.fetchall()

        # consulta de gestiones totales
        query_gestiones = """
            SELECT COUNT(*) as cantidadGestiones
            FROM historial_gestiones 
            """
        if fecha_inicio and fecha_final:
            query_gestiones += " WHERE fecha BETWEEN %s AND %s "
            cursor.execute(query_gestiones, [fecha_inicio, fecha_final])
        elif fecha_inicio:
            query_gestiones += " WHERE fecha >= %s "
            cursor.execute(query_gestiones, [fecha_inicio])
        elif fecha_final:
            query_gestiones += " WHERE fecha <= %s "
            cursor.execute(query_gestiones, [fecha_final])
        else:
            cursor.execute(query_gestiones)
        datos_gestiones = cursor.fetchall()

        # Resto de consultas con filtros aplicados
        # ... (aplicar los filtros a las demás consultas)

        # Sin Gestion
        query_sin_gestion = """
           SELECT COUNT(*) as cantidadSinGestion
            FROM kliiker k
            WHERE NOT EXISTS (
            SELECT 1
                FROM historial_gestiones h
                WHERE h.celular = k.celular
            )
            """
        if nivel:
            query_sin_gestion = query_sin_gestion.replace("WHERE", "AND")
            query_sin_gestion = (
                """
               SELECT COUNT(*) as cantidadSinGestion
                FROM kliiker k
                """
                + nivel_condition
                + """
                AND NOT EXISTS (
                SELECT 1
                    FROM historial_gestiones h
                    WHERE h.celular = k.celular
                )
                """
            )
        cursor.execute(query_sin_gestion, nivel_params)
        datos_sinGestion = cursor.fetchall()

        # Cantidad Gestionados
        query_gestionados = """
            SELECT COUNT(*) AS cantidadGestionados
            FROM kliiker k
            WHERE EXISTS (
            SELECT 1
            FROM historial_gestiones h
            WHERE h.celular = k.celular
            )
            """
        if nivel:
            query_gestionados = query_gestionados.replace("WHERE", "AND")
            query_gestionados = (
                """
                SELECT COUNT(*) AS cantidadGestionados
                FROM kliiker k
                """
                + nivel_condition
                + """
                AND EXISTS (
                SELECT 1
                FROM historial_gestiones h
                WHERE h.celular = k.celular
                )
                """
            )
        cursor.execute(query_gestionados, nivel_params)
        datos_gestionados = cursor.fetchall()

        # Gestiones Totales
        query_gestiones_totales = (
            "SELECT COUNT(*) AS gestionesTotales FROM historial_gestiones"
        )
        if fecha_inicio and fecha_final:
            query_gestiones_totales += " WHERE fecha BETWEEN %s AND %s "
            cursor.execute(query_gestiones_totales, [fecha_inicio, fecha_final])
        elif fecha_inicio:
            query_gestiones_totales += " WHERE fecha >= %s "
            cursor.execute(query_gestiones_totales, [fecha_inicio])
        elif fecha_final:
            query_gestiones_totales += " WHERE fecha <= %s "
            cursor.execute(query_gestiones_totales, [fecha_final])
        else:
            cursor.execute(query_gestiones_totales)
        gestionesTotales = cursor.fetchall()

        # Cierre Flujo
        query_cierre_flujo = """
            SELECT COUNT(*) AS cantCierreFlujo
            FROM gestiones g              
            JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
            JOIN estadoKliiker e ON g.id_estado = e.id_estado
            WHERE t.cierre_flujo = 1
            """
        if date_condition_gestiones or estado_condition or tipificacion_condition:
            query_cierre_flujo = query_cierre_flujo.replace("WHERE", "AND")
            query_cierre_flujo = (
                """
                SELECT COUNT(*) AS cantCierreFlujo
                FROM gestiones g              
                JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion 
                JOIN estadoKliiker e ON g.id_estado = e.id_estado
                """
                + date_condition_gestiones
                + estado_condition
                + tipificacion_condition
                + """
                AND t.cierre_flujo = 1
                """
            )
        cursor.execute(query_cierre_flujo, params[:])
        datos_cierreFlujo = cursor.fetchall()

        # Gestionables
        query_gestionables = """
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
        if nivel:
            query_gestionables = query_gestionables.replace("WHERE", "AND")
            query_gestionables = (
                """
                SELECT COUNT(*) as gestionables
                FROM kliiker k
                """
                + nivel_condition
                + """
                AND NOT EXISTS (
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
        cursor.execute(query_gestionables, nivel_params)
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
    # Obtener parámetros de filtro de la solicitud
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_final = request.args.get("fecha_final")
    nivel = request.args.get("nivel")
    estado = request.args.get("estado")
    tipificacion = request.args.get("tipificacion")

    # Convertir "Todo" a None para que no se aplique el filtro
    if estado == "Todo":
        estado = None
    if tipificacion == "Todo":
        tipificacion = None

    datos = obtener_datos_estadisticas(
        fecha_inicio, fecha_final, nivel, estado, tipificacion
    )
    # Provide default empty data structure if datos is None
    if datos is None:
        datos = {
            "estados": [],
            "tipificaciones": [],
            "rpc": {"rpc_exitosos": 0},
            "codigos": {"con_codigo": 0, "sin_codigo": 0},
            "ventas": [],
            "total_kliikers": [],
            "cantidadGestiones": [],
            "contactabilidad": 0,
            "sinInteres": [],
            "sinGestion": [],
            "gestionados": [],
            "gestionesTotales": [],
            "cierreFlujo": [],
            "gestionables": [],
            "efectividad": 0,
            "conversion": 0,
            "ventas_exitosas": 0,
            "rpc_exitosos": 0,
            "gestionados_total": 0,
            "contactabilidad_porcentaje": 0,
            "rpc_porcentaje": 0,
            "gestiones_totales": 0,
        }
    return jsonify(datos)


@estadisticas_bp.route("/graficos")
def mostrar_graficos():
    datos = obtener_datos_estadisticas()
    # Provide default empty data structure if datos is None
    if datos is None:
        datos = {
            "estados": [],
            "tipificaciones": [],
            "rpc": {"rpc_exitosos": 0},
            "codigos": {"con_codigo": 0, "sin_codigo": 0},
            "ventas": [],
            "total_kliikers": [],
            "cantidadGestiones": [],
            "contactabilidad": 0,
            "sinInteres": [],
            "sinGestion": [],
            "gestionados": [],
            "gestionesTotales": [],
            "cierreFlujo": [],
            "gestionables": [],
            "efectividad": 0,
            "conversion": 0,
            "ventas_exitosas": 0,
            "rpc_exitosos": 0,
            "gestionados_total": 0,
            "contactabilidad_porcentaje": 0,
            "rpc_porcentaje": 0,
            "gestiones_totales": 0,
        }
    return render_template("estadisticas/estadisticas.html", datos=datos)
