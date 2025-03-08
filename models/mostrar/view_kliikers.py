from flask import render_template, Blueprint, Flask, flash, request, redirect, url_for
from database.config import mysql
from datetime import datetime

# Blueprint para mostrar las tablas de gestión
mostrar_tablas = Blueprint("mostrar_tablas", __name__)

def obtener_datos_gestion():
    try:
        cursor = mysql.connection.cursor()

        # Verifica si existe la tabla kliiker
        cursor.execute("SHOW TABLES LIKE 'kliiker'")
        if not cursor.fetchone():
            raise Exception("Tabla 'kliiker' no existe")

        # Consulta principal que une las tablas kliiker, gestiones, usuarios, tipificacion y estadoKliiker
        consulta = """
            SELECT
                g.id_gestion AS idGestion,
                k.id_Kliiker AS idKliiker,
                k.nombre,
                k.apellido,
                k.celular,
                k.nivel AS codigo,
                e.estado,
                g.canal,
                g.tipoGestion,
                g.fecha,
                g.comentario,
                u.nombre_AS AS asesor,
                t.tipificacion,
                g.motivoNoInteres,
                g.tipificacion AS tipGestion
            FROM kliiker k
            LEFT JOIN gestiones g ON k.celular = g.celular
            LEFT JOIN usuarios u ON g.nombre_AS = u.nombre_AS
            LEFT JOIN tipificacion t ON g.tipificacion = t.tipificacion
            LEFT JOIN estadoKliiker e ON k.id_estado = e.id_estado
            ORDER BY g.fecha DESC
        """
        cursor.execute(consulta)

        column_names = [column[0] for column in cursor.description]
        datos = cursor.fetchall()
        print(datos)
        cursor.close()
        return datos
    except Exception as err:
        print(f"Error en obtener_datos_gestion: {str(err)}")
        return []


def obtener_datos_historial():
    try:
        cursor = mysql.connection.cursor()
        
        # Consulta para obtener el historial de gestiones con información relacionada
        consulta = """
            SELECT 
                h.id_historial,
                h.id_gestion,
                h.id_llamada,
                h.fecha,
                h.canal,
                h.tipoGestion,
                h.comentario,
                h.fechaProximaGestion,
                h.nombre_AS as asesor,
                h.tipificacion,
                h.celular,
                h.motivoNoInteres,
                k.id_Kliiker AS idKliiker,
                k.nombre,
                k.apellido,
                k.nivel,
                e.estado
            FROM historial_gestiones h
            LEFT JOIN kliiker k ON h.celular = k.celular
            LEFT JOIN estadokliiker e ON h.id_estado = e.id_estado
            ORDER BY h.fecha DESC
        """
        cursor.execute(consulta)
        datos_historial = cursor.fetchall()
        return datos_historial
        
    except Exception as err:
        print(f"Error en obtener_datos_historial: {str(err)}")
        return []


# Ruta para mostrar las tablas de gestión y historial
@mostrar_tablas.route("/mostrar_tablas")
def mostrar_tabla():
    datos_gestion = obtener_datos_gestion()
    datos_historial = obtener_datos_historial()
    return render_template(
        "/formGestion/gestion.html", 
        datos=datos_gestion,
        datos_historial=datos_historial
    )