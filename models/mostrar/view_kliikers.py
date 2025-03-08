from flask import render_template, Blueprint, Flask, flash, request, redirect, url_for
from database.config import mysql
from datetime import datetime

mostrar_tablas = Blueprint("mostrar_tablas", __name__)


def obtener_datos_gestion():
    try:
        cursor = mysql.connection.cursor()

        cursor.execute("SHOW TABLES LIKE 'kliiker'")
        if not cursor.fetchone():
            raise Exception("Tabla 'kliiker' no existe")

        consulta = """
            SELECT
                g.id_gestion AS idGestion,
                k.id_Kliiker AS idKliiker,
                k.nombre,
                k.apellido,
                k.celular,
                k.nivel AS codigo,  -- Cambiado alias conflictivo
                e.estado,
                g.canal,
                g.tipoGestion,
                g.fecha,
                g.comentario,
                u.nombre_AS AS asesor,
                t.tipificacion,
                g.motivoNoInteres
            FROM kliiker k
            LEFT JOIN gestiones g ON k.celular = g.celular
            LEFT JOIN usuarios u ON g.nombre_AS = u.nombre_AS
            LEFT JOIN tipificacion t ON g.tipificacion = t.tipificacion
            LEFT JOIN estadoKliiker e ON k.id_estado = e.id_estado  -- JOIN corregido
            ORDER BY g.fecha DESC
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


@mostrar_tablas.route("/mostrar_tablas")
def mostrar_tabla():
    datos = obtener_datos_gestion()
    return render_template("/formGestion/gestion.html", datos=datos)
