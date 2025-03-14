# import os
# import csv
# import json
# from datetime import datetime
# from flask import request, flash, redirect, url_for, send_from_directory
# from database.config import mysql

# # Configuración de directorios
# UPLOAD_FOLDER = "dbUploaded"  # Directorio para guardar CSVs subidos
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear directorio si no existe


# # Helpers para conversión de formatos
# def convertir_fechas(item):
#     """Convierte campos de fecha ISO a formato DD/MM/YYYY."""
#     for key, value in item.items():
#         try:
#             item[key] = datetime.strptime(value, "%Y-%m-%d").strftime("%d/%m/%Y")
#         except (ValueError, TypeError):
#             pass
#     return item


# def formatear_encabezado(header):
#     """Formatea los encabezados del CSV."""
#     return [col.strip().lower().replace(" ", "_") for col in header]


# # Función para subir archivos CSV
# def upload():
#     if request.method == "POST":
#         file = request.files["file"]

#         if file and file.filename.endswith(".csv"):
#             try:
#                 # Guardar CSV en disco
#                 csv_filename = os.path.join(UPLOAD_FOLDER, file.filename)
#                 file.save(csv_filename)

#                 # Convertir CSV a JSON
#                 with open(csv_filename, newline="", encoding="utf-8") as csvfile:
#                     reader = csv.DictReader(csvfile)
#                     data = [convertir_fechas(row) for row in reader]
#                     json_filename = csv_filename.replace(".csv", ".json")
#                     with open(json_filename, "w", encoding="utf-8") as jsonfile:
#                         json.dump(data, jsonfile, ensure_ascii=False, indent=4)

#                 # Insertar en base de datos
#                 cur = mysql.connection.cursor()
#                 cur.execute(
#                     "INSERT INTO uploaded_db (nombre, date_upload) VALUES (%s, %s)",
#                     (file.filename, datetime.now()),
#                 )
#                 mysql.connection.commit()
#                 cur.close()

#                 flash("Archivo subido y procesado exitosamente!", "success")
#             except Exception as e:
#                 flash(f"Error al procesar el archivo: {str(e)}", "danger")

#             return redirect(url_for("administradores.downloadDB"))


# # Función para descargar archivos CSV
# def download(id_db):
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute(
#             "SELECT nombre, date_upload FROM uploaded_db WHERE id_db = %s", (id_db,)
#         )
#         result = cur.fetchone()
#         cur.close()

#         if not result:
#             flash("Registro no encontrado", "danger")
#             return redirect(url_for("administradores.downloadDB"))

#         nombre_archivo, fecha_subida = result
#         archivo_path = os.path.join(UPLOAD_FOLDER, nombre_archivo)

#         if not os.path.exists(archivo_path):
#             flash("El archivo no existe en el servidor", "danger")
#             return redirect(url_for("administradores.downloadDB"))

#         return send_from_directory(
#             directory=UPLOAD_FOLDER,
#             path=nombre_archivo,
#             as_attachment=True,
#             download_name=f"Bases de datos Kliiker ({fecha_subida.strftime('%d-%m-%Y')}).csv",
#         )
#     except Exception as e:
#         flash(f"Error al descargar el archivo: {str(e)}", "danger")
#         return redirect(url_for("administradores.downloadDB"))

import os
import csv
from datetime import datetime
from flask import request, flash, redirect, url_for, send_from_directory, abort
from werkzeug.utils import secure_filename
from database.config import mysql

UPLOAD_FOLDER = "dbUploaded"
ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_kliiker_data(record):
    required_fields = ["id_kliiker", "nombre", "celular"]
    return all(record.get(field) for field in required_fields)


def parse_date(date_str):
    date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except (ValueError, TypeError):
            continue
    return None


def handle_upload():
    if "file" not in request.files:
        flash("No se encontró el archivo en la solicitud", "error")
        return redirect(url_for("administradores.downloadDB"))

    file = request.files["file"]

    if file.filename == "":
        flash("Archivo no seleccionado", "error")
        return redirect(url_for("administradores.downloadDB"))

    if not allowed_file(file.filename):
        flash("Tipo de archivo no permitido", "error")
        return redirect(url_for("administradores.downloadDB"))

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        with open(filepath, "r", encoding="utf-8") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            fieldnames = [fn.strip().lower() for fn in csv_reader.fieldnames]

            cursor = mysql.connection.cursor()

            for row in csv_reader:
                record = {
                    k.lower().strip(): v.strip() if v else None for k, v in row.items()
                }

                if not validate_kliiker_data(record):
                    flash(f"Registro inválido: {record}", "warning")
                    continue

                processed = {
                    "id_Kliiker": record.get("id_kliiker"),
                    "nombre": record.get("nombre"),
                    "apellido": record.get("apellido"),
                    "celular": record.get("celular"),
                    "nivel": int(record.get("nivel", 0)) if record.get("nivel") else 0,
                    "correo": record.get("correo"),
                    "fecha": parse_date(record.get("fecha")),
                    "venta": bool(int(record.get("venta", 0))),
                    "fechaIngreso": parse_date(record.get("fechaingreso")),
                    "diaSinGestion": (
                        int(record.get("diasingestion", 0))
                        if record.get("diasingestion")
                        else None
                    ),
                    "gestionable": bool(int(record.get("gestionable", 0))),
                    "id_estado": (
                        int(record.get("id_estado"))
                        if record.get("id_estado")
                        else None
                    ),
                    "fechaSinGestion": parse_date(record.get("fechasingestion")),
                }

                cursor.execute(
                    """
                    INSERT INTO kliiker (
                        id_Kliiker, nombre, apellido, celular, nivel, correo,
                        fecha, venta, fechaIngreso, diaSinGestion,
                        gestionable, id_estado, fechaSinGestion
                    ) VALUES (
                        %(id_Kliiker)s, %(nombre)s, %(apellido)s, %(celular)s,
                        %(nivel)s, %(correo)s, %(fecha)s, %(venta)s,
                        %(fechaIngreso)s, %(diaSinGestion)s, %(gestionable)s,
                        %(id_estado)s, %(fechaSinGestion)s
                    )
                    ON DUPLICATE KEY UPDATE
                        nombre = VALUES(nombre),
                        apellido = VALUES(apellido),
                        correo = VALUES(correo),
                        id_estado = VALUES(id_estado)
                """,
                    processed,
                )

                if record.get("id_gestion"):
                    gestion_data = {
                        "id_gestion": int(record["id_gestion"]),
                        "id_llamada": (
                            int(record["id_llamada"])
                            if record.get("id_llamada")
                            else None
                        ),
                        "fecha": parse_date(record.get("fecha")),
                        "canal": record.get("canal"),
                        "tipoGestion": record.get("tipogestion"),
                        "comentario": record.get("comentario"),
                        "fechaProximaGestion": parse_date(
                            record.get("fechaproximagestion")
                        ),
                        "nombre_AS": record.get("nombre_as"),
                        "id_tipificacion": (
                            int(record["id_tipificacion"])
                            if record.get("id_tipificacion")
                            else None
                        ),
                        "motivoNoInteres": record.get("motivonointeres"),
                        "id_estado": (
                            int(record.get("id_estado"))
                            if record.get("id_estado")
                            else None
                        ),
                        "celular": record.get("celular"),
                    }

                    cursor.execute(
                        """
                        INSERT INTO gestiones (
                            id_gestion, id_llamada, fecha, canal, tipoGestion,
                            comentario, fechaProximaGestion, nombre_AS,
                            id_tipificacion, motivoNoInteres, id_estado, celular
                        ) VALUES (
                            %(id_gestion)s, %(id_llamada)s, %(fecha)s, %(canal)s,
                            %(tipoGestion)s, %(comentario)s, %(fechaProximaGestion)s,
                            %(nombre_AS)s, %(id_tipificacion)s, %(motivoNoInteres)s,
                            %(id_estado)s, %(celular)s
                        )
                    """,
                        gestion_data,
                    )

            cursor.execute(
                """
                INSERT INTO uploaded_db (nombre, date_upload)
                VALUES (%s, %s)
            """,
                (filename, datetime.now()),
            )

            mysql.connection.commit()
            flash("Archivo procesado exitosamente!", "success")

    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error procesando archivo: {str(e)}", "error")

    finally:
        if "cursor" in locals():
            cursor.close()
        if os.path.exists(filepath):
            os.remove(filepath)

    return redirect(url_for("administradores.downloadDB"))


def handle_download(id_db):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            SELECT nombre, date_upload 
            FROM uploaded_db 
            WHERE id_db = %s
        """,
            (id_db,),
        )

        db_record = cursor.fetchone()
        cursor.close()

        if not db_record:
            flash("Registro no encontrado", "error")
            return redirect(url_for("administradores.downloadDB"))

        original_filename, upload_date = db_record
        safe_filename = secure_filename(original_filename)
        file_path = os.path.join(UPLOAD_FOLDER, safe_filename)

        if not os.path.isfile(file_path):
            flash("Archivo no encontrado en el servidor", "error")
            return redirect(url_for("administradores.downloadDB"))

        download_name = f"backup_{upload_date.strftime('%Y%m%d')}_{safe_filename}"

        return send_from_directory(
            directory=UPLOAD_FOLDER,
            path=safe_filename,
            as_attachment=True,
            download_name=download_name,
            mimetype="text/csv",
        )

    except Exception as e:
        flash(f"Error en descarga: {str(e)}", "error")
        return redirect(url_for("administradores.downloadDB"))
