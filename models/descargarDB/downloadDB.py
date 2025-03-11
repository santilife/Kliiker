import os
import csv
import json
from datetime import datetime
from flask import request, flash, redirect, url_for, send_file
from database.config import mysql

# Configuración de directorios
UPLOAD_FOLDER = "dbUploaded"  # Directorio para guardar CSVs subidos
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear directorio si no existe


# Helpers para conversión de formatos
# ---------------------------------------------------
def convertir_fechas(item):
    """Convierte campos de fecha ISO a formato DD/MM/YYYY."""
    # (Mantener igual tu implementación actual)
    return item


def formatear_encabezado(header):
    """Formatea los encabezados del CSV."""
    # (Mantener igual tu implementación actual)
    return header


# Función para subir archivos CSV
# ---------------------------------------------------
def upload():
    if request.method == "POST":
        file = request.files["file"]

        if file and file.filename.endswith(".csv"):
            try:
                # Guardar CSV original
                csv_filename = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(csv_filename)  # Guardar el CSV en disco

                # Convertir CSV a JSON (opcional, según tu lógica)
                # ... (tu código actual de conversión a JSON) ...

                # Insertar en base de datos
                cur = mysql.connection.cursor()
                cur.execute(
                    "INSERT INTO uploaded_db (nombre, date_upload) VALUES (%s, %s)",
                    (file.filename, datetime.now()),
                )
                mysql.connection.commit()
                cur.close()

                flash("Archivo subido y procesado exitosamente!", "success")

            except Exception as e:
                flash(f"Error al procesar el archivo: {str(e)}", "danger")

            return redirect(url_for("administradores.downloadDB"))


# Función para descargar archivos CSV
# ---------------------------------------------------
def download(db_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT nombre, date_upload FROM uploaded_db WHERE id_db = %s", (db_id,)
        )
        result = cur.fetchone()
        cur.close()

        if not result:
            flash("Registro no encontrado", "danger")
            return redirect(url_for("administradores.downloadDB"))

        nombre_archivo, fecha_subida = result

        # Ruta del archivo CSV guardado
        csv_path = os.path.join(UPLOAD_FOLDER, nombre_archivo)

        if not os.path.exists(csv_path):
            flash("El archivo no existe en el servidor", "danger")
            return redirect(url_for("administradores.downloadDB"))

        # Descargar el archivo original
        return send_file(
            csv_path,
            as_attachment=True,
            download_name=f"Bases de datos Kliiker ({fecha_subida.strftime('%d/%m/%Y')}).csv",
        )

    except Exception as e:
        flash(f"Error al descargar: {str(e)}", "danger")
        return redirect(url_for("administradores.downloadDB"))
