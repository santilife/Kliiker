from flask import Flask, jsonify
from datetime import datetime, date
import json
from database.config import mysql, db_conexion


def get_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM kliiker")
    resultados = cursor.fetchall()
    cursor.close()

    datos = []
    for fila in resultados:
        # Convertir campos datetime/date a strings
        fecha_ingreso = fila["fechaIngreso"]
        if isinstance(
            fecha_ingreso, (datetime, date)
        ):  # Asegura importar 'date' de datetime
            fecha_ingreso = fecha_ingreso.isoformat()

        datos.append(
            {
                "id_kliiker": fila["id_Kliiker"],
                "nombre": fila["nombre"],
                "apellido": fila["apellido"],
                "celular": fila["celular"],
                "nivel": fila["nivel"],
                "correo": fila["correo"],
                "fechaIngreso": fecha_ingreso,  # Usar el valor convertido
                "diaSinGestion": fila["diaSinGestion"],
                "gestionable": fila["gestionable"],
                "id_estado": fila["id_estado"],
            }
        )
    return datos


def export_json():
    datos = get_data()

    # Generar nombre del archivo con fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"Base de datos {fecha_actual}.json"

    # Crear y guardar el archivo JSON
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

    return jsonify({"mensaje": f"Archivo {nombre_archivo} generado exitosamente"})
