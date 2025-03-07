from flask import render_template, Blueprint, Flask
from database.config import mysql
from datetime import datetime


def obtener_datos_gestion():
    try:
        cursor = mysql.connection.cursor()

        # Verificar primero si la tabla existe
        cursor.execute("SHOW TABLES LIKE 'kliiker'")
        if not cursor.fetchone():
            raise Exception("La tabla 'kliiker' no existe en la base de datos")

        consulta = """
            SELECT
                k.id_Kliiker AS idKliiker,
                k.nombre,
                k.apellido,
                k.celular,
                k.id_Kliiker AS codigo,
                K.nivel,
                e.estado,
                g.tipoGestion,
                g.canal,
                g.tipoGestion AS tipo_gestor,
                g.fecha,
                g.comentario,
                u.nombre_AS AS asesor,
                t.tipificacion
                FROM kliiker k
                LEFT JOIN gestiones g ON k.celular = g.celular
                LEFT JOIN usuarios u ON g.nombre_AS = u.nombre_AS
                LEFT JOIN tipificacion t ON g.tipificacion = t.tipificacion
                LEFT JOIN estado e ON e.estado = id_kliiker
                ORDER BY g.fecha DESC
        """
        cursor.execute(consulta)

        # Obtener metadatos ANTES de cerrar el cursor
        column_names = [column[0] for column in cursor.description]
        datos = cursor.fetchall()

        # Convertir resultados a diccionarios
        # resultados = [dict(zip(column_names, row)) for row in datos]

        cursor.close()
        return datos

    except Exception as err:
        print(f"Error al obtener datos: {str(err)}")
        return []


def obtener_datos_historial():
    try:
        cursor = mysql.connection.cursor()

        # Verificar primero si la tabla existe
        cursor.execute("SHOW TABLES LIKE 'kliiker'")
        if not cursor.fetchone():
            raise Exception("La tabla 'kliiker' no existe en la base de datos")

        consulta = """
            SELECT
            
        """
        cursor.execute(consulta)

        # Obtener metadatos ANTES de cerrar el cursor
        column_names = [column[0] for column in cursor.description]
        datos2 = cursor.fetchall()

        # Convertir resultados a diccionarios
        # resultados = [dict(zip(column_names, row)) for row in datos]

        cursor.close()
        return datos2

    except Exception as err:
        print(f"Error al obtener datos: {str(err)}")
        return []


# @login_required
def mostrar_tabla():
    datos = obtener_datos_gestion()
    return render_template("/formGestion/gestion.html", datos=datos)
