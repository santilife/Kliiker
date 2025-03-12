from flask import render_template, Blueprint, Flask, flash, request, redirect, url_for
from database.config import mysql
from datetime import datetime

# Blueprint para mostrar las tablas de gestión
mostrar_tablas = Blueprint("mostrar_tablas", __name__)


def obtener_datos_gestion():
    
    # tipificaciones = {
    #     1: "Buzón de voz",
    #     2: "Equivocado",
    #     3: "Información general",
    #     4: "Interesado a futuro",
    #     5: "Leed ya compro",
    #     6: "No contesta",
    #     7: "Novedad en el registro",
    #     8: "Registro exitoso",
    #     9: "Seguimiento",
    #     10: "Sin interes",
    #     11: "Volver a llamar",
    # }
    
    
    
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
                g.id_tipificacion,
                t.tipificacion AS tipificacion_texto
            FROM kliiker k
            LEFT JOIN gestiones g ON k.celular = g.celular
            LEFT JOIN usuarios u ON g.nombre_AS = u.nombre_AS
            LEFT JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion
            LEFT JOIN estadoKliiker e ON k.id_estado = e.id_estado
            ORDER BY g.fecha DESC
        """
        cursor.execute(consulta)
        datos = cursor.fetchall()
        print(datos)
        column_names = [column[0] for column in cursor.description]
        # print(datos)
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
                h.id_gestion as idGestion,
                h.id_llamada,
                h.fecha,
                h.canal,
                h.tipoGestion,
                h.comentario,
                h.fechaProximaGestion,
                h.nombre_AS as asesor,
                h.id_tipificacion,
                h.celular,
                h.motivoNoInteres,
                k.id_Kliiker AS idKliiker,
                k.nombre,
                k.apellido,
                k.nivel,
                e.estado,
                t.tipificacion
            FROM historial_gestiones h
            LEFT JOIN kliiker k ON h.celular = k.celular
            LEFT JOIN estadokliiker e ON h.id_estado = e.id_estado
            LEFT JOIN tipificacion t ON h.id_tipificacion = t.id_tipificacion
            ORDER BY h.id_historial DESC
        """
        cursor.execute(consulta)
        datos_historial = cursor.fetchall()
        return datos_historial

    except Exception as err:
        print(f"Error en obtener_datos_historial: {str(err)}")
        return []


def total_gestiones():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            SELECT celular, COUNT(*) as total 
            FROM historial_gestiones 
            WHERE celular REGEXP '^[0-9]+$' -- Solo números
            GROUP BY celular
        """
        )
        resultados = cursor.fetchall()

        # print("Resultados crudos de la consulta:", resultados)

        gestiones_por_celular = {}
        for resultado in resultados:
            # Los resultados son diccionarios con las claves 'celular' y 'total'
            celular = str(resultado["celular"]).strip()
            total = resultado["total"]
            gestiones_por_celular[celular] = total
            # print(f"Celular: '{celular}', Total: {total}")

        # print("Diccionario final:", gestiones_por_celular)
        return gestiones_por_celular

    except Exception as err:
        print(f"Error en total_gestiones: {str(err)}")
        return {}
    finally:
        cursor.close()


# Ruta para mostrar las tablas de gestión y historial
@mostrar_tablas.route("/mostrar_tablas")
def mostrar_tabla():
    datos_gestion = obtener_datos_gestion()
    datos_historial = obtener_datos_historial()
    cantidad_gestiones = total_gestiones()
    # print("Diccionario cantidad_gestiones:", cantidad_gestiones)
    # if datos_gestion:
    #     print("Primera fila de datos_gestion:", datos_gestion[0])
    return render_template(
        "/formGestion/gestion.html",
        datos=datos_gestion,
        datos_historial=datos_historial,
        cantidad_gestiones=cantidad_gestiones,
    )
