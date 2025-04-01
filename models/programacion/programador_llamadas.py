from flask import Blueprint, render_template, jsonify, session
from database.config import mysql
import MySQLdb
from datetime import datetime, timedelta
import calendar

programador_bp = Blueprint("programador", __name__)

# Configuración de días para cada llamada según el flujo
PROGRAMACION_CON_CODIGO = {
    1: 1,  # Primera llamada: día 1
    2: 2,  # Segunda llamada: día 2
    3: 4,  # Tercera llamada: día 4
    4: 8,  # Cuarta llamada: día 8
}

PROGRAMACION_SIN_CODIGO = {
    1: 1,  # Primera llamada: día 1
    2: 3,  # Segunda llamada: día 3
    3: 6,  # Tercera llamada: día 6
    4: 12,  # Cuarta llamada: día 12
}


def calcular_proxima_fecha(fecha_actual, num_llamada, tiene_codigo):
    """
    Calcula la fecha de la próxima llamada según el flujo establecido.

    Args:
        fecha_actual: Fecha de la gestión actual
        num_llamada: Número de llamada actual (1-4)
        tiene_codigo: Boolean que indica si el kliiker tiene código (True) o no (False)

    Returns:
        Fecha de la próxima llamada o None si ya se completaron todas las llamadas
    """
    if not isinstance(fecha_actual, datetime):
        if isinstance(fecha_actual, str):
            fecha_actual = datetime.strptime(fecha_actual, "%Y-%m-%d")
        else:
            fecha_actual = datetime.now()

    # Determinar el siguiente número de llamada
    siguiente_llamada = num_llamada + 1

    # Si ya completó todas las llamadas, no hay próxima fecha
    if siguiente_llamada > 4:
        return None

    # Seleccionar la programación según si tiene código o no
    programacion = PROGRAMACION_CON_CODIGO if tiene_codigo else PROGRAMACION_SIN_CODIGO

    # Calcular días de diferencia entre la llamada actual y la siguiente
    dias_diferencia = programacion[siguiente_llamada] - programacion[num_llamada]

    # Calcular la fecha de la próxima llamada
    proxima_fecha = fecha_actual + timedelta(days=dias_diferencia)

    # Ajustar si cae en fin de semana (opcional)
    dia_semana = proxima_fecha.weekday()
    if dia_semana >= 5:  # 5=Sábado, 6=Domingo
        # Mover al siguiente lunes
        dias_ajuste = 7 - dia_semana
        proxima_fecha = proxima_fecha + timedelta(days=dias_ajuste)

    return proxima_fecha


def obtener_gestiones_pendientes():
    """
    Obtiene las gestiones pendientes para el día actual.

    Returns:
        Dictionary con gestiones pendientes separadas por con_codigo y sin_codigo
    """
    try:
        connection = mysql.connection
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)

        fecha_actual = datetime.now().date()

        # Consulta para obtener gestiones pendientes con código
        query_con_codigo = """
        SELECT k.id_kliiker, k.nombre, k.celular, k.correo, g.id_llamada, g.fechaProximaGestion
        FROM kliiker k
        JOIN gestiones g ON k.celular = g.celular
        WHERE k.nivel = 1
        AND g.fechaProximaGestion = %s
        AND NOT EXISTS (
            SELECT 1 FROM gestiones g2
            WHERE g2.celular = k.celular
            AND g2.fecha = %s
        )
        ORDER BY g.id_llamada
        """

        # Consulta para obtener gestiones pendientes sin código
        query_sin_codigo = """
        SELECT k.id_kliiker, k.nombre, k.celular, k.correo, g.id_llamada, g.fechaProximaGestion
        FROM kliiker k
        JOIN gestiones g ON k.celular = g.celular
        WHERE k.nivel = 0
        AND g.fechaProximaGestion = %s
        AND NOT EXISTS (
            SELECT 1 FROM gestiones g2
            WHERE g2.celular = k.celular
            AND g2.fecha = %s
        )
        ORDER BY g.id_llamada
        """

        # Ejecutar consultas
        cursor.execute(query_con_codigo, (fecha_actual, fecha_actual))
        gestiones_con_codigo = cursor.fetchall()

        cursor.execute(query_sin_codigo, (fecha_actual, fecha_actual))
        gestiones_sin_codigo = cursor.fetchall()

        cursor.close()

        return {
            "con_codigo": gestiones_con_codigo,
            "sin_codigo": gestiones_sin_codigo,
            "fecha_actual": fecha_actual.strftime("%Y-%m-%d"),
        }

    except MySQLdb.Error as e:
        print(f"Error de base de datos: {e}")
        return {
            "con_codigo": [],
            "sin_codigo": [],
            "fecha_actual": datetime.now().strftime("%Y-%m-%d"),
        }


def actualizar_proxima_gestion(id_gestion, id_llamada, tiene_codigo):
    """
    Actualiza la fecha de próxima gestión después de registrar una gestión.

    Args:
        id_gestion: ID de la gestión actual
        id_llamada: Número de llamada actual
        tiene_codigo: Boolean que indica si el kliiker tiene código

    Returns:
        Boolean indicando si la actualización fue exitosa
    """
    try:
        connection = mysql.connection
        cursor = connection.cursor()

        # Obtener la fecha de la gestión actual
        query_fecha = "SELECT fecha FROM gestiones WHERE id_gestion = %s"
        cursor.execute(query_fecha, (id_gestion,))
        resultado = cursor.fetchone()

        if not resultado:
            return False

        fecha_actual = resultado[0]

        # Calcular la próxima fecha de gestión
        proxima_fecha = calcular_proxima_fecha(
            fecha_actual, int(id_llamada), tiene_codigo
        )

        if proxima_fecha:
            # Actualizar la fecha de próxima gestión
            query_update = (
                "UPDATE gestiones SET fechaProximaGestion = %s WHERE id_gestion = %s"
            )
            cursor.execute(query_update, (proxima_fecha, id_gestion))
            connection.commit()

        cursor.close()
        return True

    except MySQLdb.Error as e:
        print(f"Error de base de datos: {e}")
        return False


def registrar_nueva_gestion(
    celular, id_llamada, id_estado, id_tipificacion, canal, comentario, tiene_codigo
):
    """
    Registra una nueva gestión y programa la próxima llamada.

    Args:
        celular: Número de celular del kliiker
        id_llamada: Número de llamada actual
        id_estado: ID del estado de la llamada
        id_tipificacion: ID de la tipificación
        canal: Canal de comunicación
        comentario: Comentario de la gestión
        tiene_codigo: Boolean que indica si el kliiker tiene código

    Returns:
        ID de la gestión creada o None si hubo un error
    """
    try:
        connection = mysql.connection
        cursor = connection.cursor()

        fecha_actual = datetime.now()
        proxima_fecha = calcular_proxima_fecha(
            fecha_actual, int(id_llamada), tiene_codigo
        )

        # Insertar nueva gestión
        query_insert = """
        INSERT INTO gestiones
        (celular, id_llamada, id_estado, id_tipificacion, canal, fecha, fechaProximaGestion, comentario, nombre_AS, tipoGestion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query_insert,
            (
                celular,
                id_llamada,
                id_estado,
                id_tipificacion,
                canal,
                fecha_actual,
                proxima_fecha,
                comentario,
                session.get("nombre_AS", "Sistema"),
                "Llamada",
            ),
        )

        id_gestion = cursor.lastrowid
        connection.commit()

        cursor.close()
        return id_gestion

    except MySQLdb.Error as e:
        print(f"Error de base de datos: {e}")
        connection.rollback()
        return None


@programador_bp.route("/gestiones_pendientes")
def mostrar_gestiones_pendientes():
    """
    Ruta para mostrar las gestiones pendientes del día.
    """
    gestiones = obtener_gestiones_pendientes()
    return render_template("gestiones/pendientes.html", gestiones=gestiones)


@programador_bp.route("/api/gestiones_pendientes")
def api_gestiones_pendientes():
    """
    API para obtener las gestiones pendientes del día en formato JSON.
    """
    gestiones = obtener_gestiones_pendientes()
    return jsonify(gestiones)


@programador_bp.route("/api/alertas_gestiones")
def api_alertas_gestiones():
    """
    API para obtener el conteo de alertas de gestiones pendientes.
    """
    gestiones = obtener_gestiones_pendientes()
    total_pendientes = len(gestiones["con_codigo"]) + len(gestiones["sin_codigo"])

    return jsonify(
        {
            "total_pendientes": total_pendientes,
            "con_codigo": len(gestiones["con_codigo"]),
            "sin_codigo": len(gestiones["sin_codigo"]),
        }
    )
