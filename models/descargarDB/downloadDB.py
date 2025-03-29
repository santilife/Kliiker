# import os
# import csv
# import io
# from datetime import datetime, date
# from flask import flash, make_response
# from werkzeug.utils import secure_filename
# from database.config import mysql

# Mapeo de nombres de campos entre CSV y base de datos
# FIELD_MAPPING = {
# "id": "id_kliiker",
# "client_id": "id_kliiker",
# "phone": "celular",
# "mobile": "celular",
# "email": "correo",
# "level": "nivel",
# "fecha_gestion": "fecha",
# "comment": "comentario",
# "next_action": "fechaProximaGestion",
# "user": "nombre_as",
# "tipo_gestion": "tipoGestion",
# "motivo": "motivoNoInteres",
# }


# class CSVProcessor:
# """
# Clase para procesar operaciones con archivos CSV incluyendo:
# - Subida y procesamiento de datos
# - Descarga de reportes
# - Manejo de base de datos MySQL
# """

# def __init__(self, mysql):
# """Inicializa con conexión MySQL"""
# self.mysql = mysql

# def smart_mapping(self, field_name):
# """
# Traduce nombres de columnas del CSV a nombres de campos de la base de datos
# usando el mapeo FIELD_MAPPING como fallback
# """
# return FIELD_MAPPING.get(field_name.lower().strip(), field_name.lower().strip())

# def allowed_file(self, filename):
# """Valida extensiones de archivo permitidas (.csv)"""
# return "." in filename and filename.rsplit(".", 1)[1].lower() in {"csv"}

# def handle_upload(self, request):
# """
# Maneja el proceso completo de subida de archivos CSV:
# 1. Validación de archivo
# 2. Procesamiento en lotes
# 3. Inserción en base de datos
# 4. Manejo de transacciones
# 5. Limpieza de archivos temporales
# """
## Validación inicial de archivo
# if "file" not in request.files:
# return {"status": "error", "message": "No se encontró el archivo"}

# file = request.files["file"]
# if file.filename == "":
# return {"status": "error", "message": "Archivo no seleccionado"}

# if not self.allowed_file(file.filename):
# return {"status": "error", "message": "Tipo de archivo no permitido"}

# try:
# Configuración inicial de archivo
# filename = secure_filename(file.filename)
# filepath = os.path.join("dbUploaded", filename)
# file.save(filepath)

# cursor = self.mysql.connection.cursor()
# batch_size = 1000  # Optimización para inserciones masivas
# batch = []

# Procesamiento del CSV
# with open(filepath, "r", encoding="utf-8") as csvfile:
# csv_reader = csv.DictReader(csvfile)
# Aplicar mapeo inteligente a los nombres de columna
# fieldnames = [
# self.smart_mapping(fn.strip()) for fn in csv_reader.fieldnames
# ]

# for row in csv_reader:
# processed = self.process_row(row)
# if not self.validate_kliiker(processed):
# flash(f"Registro inválido: {processed}", "warning")
# continue

# batch.append(processed)
# Inserta por lotes para mejor performance
# if len(batch) >= batch_size:
# self.insert_batch(cursor, batch)
# batch = []

# Insertar datos restantes
# if batch:
# self.insert_batch(cursor, batch)

# Registrar subida en base de datos
# cursor.execute(
# "INSERT INTO uploaded_db (nombre, date_upload) VALUES (%s, %s)",
# (filename, datetime.now()),
# )
# self.mysql.connection.commit()
# return {"status": "success", "message": "Archivo procesado exitosamente!"}

# except Exception as e:
# self.mysql.connection.rollback()
# return {"status": "error", "message": f"Error procesando archivo: {str(e)}"}
# finally:
# Limpieza de recursos
# if "cursor" in locals():
# cursor.close()
# if os.path.exists(filepath):
# os.remove(filepath)

# def process_row(self, raw_row):
# """
# Procesamiento avanzado de filas:
# - Conversión de tipos de datos
# - Formateo de fechas múltiples
# - Limpieza de espacios
# - Manejo de valores nulos
# """
# processed = {
# self.smart_mapping(k): v.strip() if v else None for k, v in raw_row.items()
# }

# Sistema de conversión de tipos de datos
# conversions = {
# "nivel": int,
# "venta": lambda x: bool(int(x)) if x else False,
# "gestionable": lambda x: bool(int(x)) if x else False,
# "id_estado": lambda x: int(x) if x else None,
# "id_tipificacion": lambda x: int(x) if x else None,
# "diaSinGestion": lambda x: int(x) if x else None,
# }

# Aplicar conversiones
# for field, converter in conversions.items():
# if field in processed:
# try:
# processed[field] = (
# converter(processed[field]) if processed[field] else None
# )
# except (ValueError, TypeError):
# processed[field] = None

# Sistema de parseo de fechas con múltiples formatos
# date_fields = [
# "fecha",
# "fechaIngreso",
# "fechaSinGestion",
# "fechaProximaGestion",
# ]
# date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]

# for field in date_fields:
# if processed.get(field):
# for fmt in date_formats:
# try:
# processed[field] = datetime.strptime(
# processed[field], fmt
# ).date()
# break
# except (ValueError, TypeError):
# continue
# else:
# processed[field] = None

# return processed

# def validate_kliiker(self, row):
# """Valida campos obligatorios para inserción en base de datos"""
# required_fields = ["id_kliiker", "nombre", "celular"]
# return all(row.get(field) for field in required_fields)

# def insert_batch(self, cursor, batch):
# """
# Inserta lotes de datos con actualización de duplicados
# Usa transacciones para mejor performance
# """
# cursor.executemany(
# """
# INSERT INTO kliiker (
# id_Kliiker, nombre, apellido, celular, nivel, correo,
# fecha, venta, fechaIngreso, diaSinGestion,
# gestionable, id_estado, fechaSinGestion
# ) VALUES (
# %(id_Kliiker)s, %(nombre)s, %(apellido)s, %(celular)s,
# %(nivel)s, %(correo)s, %(fecha)s, %(venta)s,
# %(fechaIngreso)s, %(diaSinGestion)s, %(gestionable)s,
# %(id_estado)s, %(fechaSinGestion)s
# )
# ON DUPLICATE KEY UPDATE
# nombre = VALUES(nombre),
# apellido = VALUES(apellido),
# correo = VALUES(correo),
# id_estado = VALUES(id_estado)
# """,
# batch,
# )
# self.mysql.connection.commit()

# def download_gestion(self):
# """
# Genera reporte CSV completo de gestiones con:
# - Datos de tablas relacionadas
# - Formato consistente
# - Manejo de errores
# """
# try:
# cursor = self.mysql.connection.cursor()
# cursor.execute(
# """
# SELECT g.*, e.estado, t.tipificacion
# FROM gestiones g
# LEFT JOIN estadoKliiker e ON g.id_estado = e.id_estado
# LEFT JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion
# """
# )

# Configuración de CSV
# column_names = [i[0] for i in cursor.description]
# rows = cursor.fetchall()
# output = io.StringIO()
# writer = csv.writer(output, delimiter=";")

# Escritura de datos
# writer.writerow(column_names)
# for row in rows:
# writer.writerow(
# [
# str(row[column]) if row[column] is not None else ""
# for column in column_names
# ]
# )

# output.seek(0)
# response = make_response(output.getvalue())
# response.headers["Content-Disposition"] = (
#'attachment; filename="gestiones_completo.csv"'
# )
# response.headers["Content-type"] = "text/csv"
# return response

# except Exception as e:
# return make_response("Error al generar el CSV", 500)
# finally:
# if "cursor" in locals():
# cursor.close()

# def download_historial(self):
# """
# Genera reporte CSV del historial de gestiones con:
# - Datos de múltiples tablas relacionadas
# - Formato compatible con Excel
# - Codificación UTF-8
# """
# try:
# cursor = self.mysql.connection.cursor()
# cursor.execute(
# """
# SELECT h.*, e.estado
# FROM historial_gestiones h
# LEFT JOIN kliiker k ON h.celular = k.celular
# LEFT JOIN usuarios u ON h.nombre_AS = u.nombre_AS
# LEFT JOIN estadoKliiker e ON h.id_estado = e.id_estado
# LEFT JOIN tipificacion t ON h.id_tipificacion = t.id_tipificacion
# """
# )

# Configuración de CSV
# column_names = [i[0] for i in cursor.description]
# rows = cursor.fetchall()
# output = io.StringIO()
# writer = csv.writer(output, delimiter=";")

# Escritura de datos
# writer.writerow(column_names)
# for row in rows:
# writer.writerow(
# [
# str(row[column]) if row[column] is not None else ""
# for column in column_names
# ]
# )

# Generación de respuesta
# output.seek(0)
# filename = f"Historial_{datetime.now().strftime('%Y-%m-%d')}.csv"
# response = make_response(output.getvalue())
# response.headers["Content-Disposition"] = (
# f'attachment; filename="{filename}"'
# )
# response.headers["Content-type"] = "text/csv"
# return response

# except Exception as e:
# return make_response("Error al generar el historial", 500)
# finally:
# if "cursor" in locals():
# cursor.close()

# def get_uploaded_files(self):
# """Obtiene listado de archivos subidos desde la base de datos"""
# try:
# cursor = self.mysql.connection.cursor()
# cursor.execute("SELECT * FROM uploaded_db ORDER BY date_upload DESC")
# return cursor.fetchall()
# except Exception as e:
# return []
# finally:
# if "cursor" in locals():
# cursor.close()

# def download_work_day(self):
# """
# Descargar la tarea del dia
# - Datos de múltiples tablas relacionadas
# - Formato compatible con Excel
# - Codificación UTF-8
# """
# try:
# cursor = self.mysql.connection.cursor()
# cursor.execute(
# """
# SELECT k.*, g.fechaProximaGestion, t.cierre_flujo
# FROM kliiker k
# LEFT JOIN (
# SELECT celular, MAX(fecha) as ultima_fecha
# FROM gestiones
# GROUP BY celular
# ) ult_g ON k.celular = ult_g.celular
# LEFT JOIN gestiones g ON ult_g.celular = g.celular AND ult_g.ultima_fecha = g.fecha
# LEFT JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion
# """
# )

# Configuración de CSV
# column_names = [i[0] for i in cursor.description]
# rows = cursor.fetchall()
# output = io.StringIO()
# writer = csv.writer(output, delimiter=";")

# Escritura de datos
# writer.writerow(column_names)
# for row in rows:
# writer.writerow(
# [
# str(row[column]) if row[column] is not None else ""
# for column in column_names
# ]
# )

# Generación de respuesta
# output.seek(0)
# filename = f"Tarea_Para_El_{datetime.now().strftime('%Y-%m-%d')}.csv"
# response = make_response(output.getvalue())
# response.headers["Content-Disposition"] = (
# f'attachment; filename="{filename}"'
# )
# response.headers["Content-type"] = "text/csv"
# return response

# except Exception as e:
# return make_response("Error al generar la tarea del dia", 500)
# finally:
# if "cursor" in locals():
# cursor.close()

# def validar_logica_kliiker(self):
# """
# Lógica de validación para Kliiker:
# 1. Si gestionable es 0, no se validan los otros puntos.
# 2. Si cierre_flujo es 1, retorna False.
# 3. Si diasSinGestion >= diasParaGestion, retorna True.
# 4. Si fechaProximaGestion es None o igual a hoy, retorna True.
# """
# try:
# cursor = self.mysql.connection.cursor(dictionary=True)
#
## Obtener todos los registros de kliiker con sus relaciones
# cursor.execute(
# """
# SELECT k.*, f.diasParaGestion, g.fechaProximaGestion, t.cierre_flujo
# FROM kliiker k
# LEFT JOIN flujotrabajo f ON k.id_estado = f.id_estado
# LEFT JOIN (
# SELECT celular, MAX(fecha) as ultima_fecha
# FROM gestiones
# GROUP BY celular
# ) ult_g ON k.celular = ult_g.celular
# LEFT JOIN gestiones g ON ult_g.celular = g.celular AND ult_g.ultima_fecha = g.fecha
# LEFT JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion
# """
# )

# resultados = []

# for registro in cursor.fetchall():
# Punto 1: Validar gestiónable
# if registro.get("gestionable") == 0:
# resultados.append(False)
# continue

# Punto 2: Validar cierre de flujo
# if registro.get("cierre_flujo") == 1:
# resultados.append(False)
# continue

# Punto 3: Validar días sin gestión
# dias_sin_gestion = registro.get("diaSinGestion") or 0
# dias_requeridos = registro.get("diasParaGestion") or 0

# if dias_sin_gestion < dias_requeridos:
# resultados.append(False)
# continue

# Punto 4: Validar fecha próxima gestión
# fecha_proxima = registro.get("fechaProximaGestion")
# hoy = date.today()

# if not fecha_proxima:
# resultados.append(True)
# else:
# resultados.append(fecha_proxima == hoy)

# return resultados

# except Exception as e:
# print(f"Error al validar la lógica: {e}")
# return []
# finally:
# if "cursor" in locals():
# cursor.close()

import os
import csv
import io
from datetime import datetime, date
from flask import flash, make_response
from werkzeug.utils import secure_filename
from database.config import mysql

FIELD_MAPPING = {
    "id": "id_kliiker",
    "client_id": "id_kliiker",
    "phone": "celular",
    "mobile": "celular",
    "email": "correo",
    "level": "nivel",
    "fecha_gestion": "fecha",
    "comment": "comentario",
    "next_action": "fechaProximaGestion",
    "user": "nombre_as",
    "tipo_gestion": "tipoGestion",
    "motivo": "motivoNoInteres",
}


class CSVProcessor:
    def __init__(self, mysql):
        self.mysql = mysql

    def smart_mapping(self, field_name):
        return FIELD_MAPPING.get(field_name.lower().strip(), field_name.lower().strip())

    def allowed_file(self, filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in {"csv"}

    def handle_upload(self, request):
        if "file" not in request.files:
            return {"status": "error", "message": "No se encontró el archivo"}

        file = request.files["file"]
        if file.filename == "":
            return {"status": "error", "message": "Archivo no seleccionado"}

        if not self.allowed_file(file.filename):
            return {"status": "error", "message": "Tipo de archivo no permitido"}

        try:
            # Conservar nombre original y crear versión segura
            original_filename = file.filename
            safe_filename = secure_filename(original_filename)

            # Configurar directorio de subida
            upload_folder = "dbUploaded"
            os.makedirs(upload_folder, exist_ok=True)

            filepath = os.path.join(upload_folder, safe_filename)
            file.save(filepath)

            cursor = self.mysql.connection.cursor()
            batch_size = 1000
            batch = []

            with open(filepath, "r", encoding="utf-8") as csvfile:
                csv_reader = csv.DictReader(csvfile)
                fieldnames = [
                    self.smart_mapping(fn.strip()) for fn in csv_reader.fieldnames
                ]

                for row in csv_reader:
                    processed = self.process_row(row)
                    if not self.validate_kliiker(processed):
                        flash(f"Registro inválido: {processed}", "warning")
                        continue

                    batch.append(processed)
                    if len(batch) >= batch_size:
                        self.insert_batch(cursor, batch)
                        batch = []

                if batch:
                    self.insert_batch(cursor, batch)

            # Guardar nombre original en la base de datos
            cursor.execute(
                "INSERT INTO uploaded_db (nombre, date_upload) VALUES (%s, %s)",
                (original_filename, datetime.now()),
            )
            self.mysql.connection.commit()
            return {"status": "success", "message": "Archivo procesado exitosamente!"}

        except Exception as e:
            self.mysql.connection.rollback()
            return {"status": "error", "message": f"Error procesando archivo: {str(e)}"}
        finally:
            if "cursor" in locals():
                cursor.close()
            if os.path.exists(filepath):
                os.remove(filepath)

    def process_row(self, raw_row):
        processed = {
            self.smart_mapping(k): v.strip() if v else None for k, v in raw_row.items()
        }

        conversions = {
            "nivel": int,
            "venta": lambda x: bool(int(x)) if x else False,
            "gestionable": lambda x: bool(int(x)) if x else False,
            "id_estado": lambda x: int(x) if x else None,
            "id_tipificacion": lambda x: int(x) if x else None,
            "diaSinGestion": lambda x: int(x) if x else None,
        }

        for field, converter in conversions.items():
            if field in processed:
                try:
                    processed[field] = (
                        converter(processed[field]) if processed[field] else None
                    )
                except (ValueError, TypeError):
                    processed[field] = None

        date_fields = [
            "fecha",
            "fechaIngreso",
            "fechaSinGestion",
            "fechaProximaGestion",
        ]
        date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]

        for field in date_fields:
            if processed.get(field):
                for fmt in date_formats:
                    try:
                        processed[field] = datetime.strptime(
                            processed[field], fmt
                        ).date()
                        break
                    except (ValueError, TypeError):
                        continue
                else:
                    processed[field] = None

        return processed

    def validate_kliiker(self, row):
        required_fields = ["id_kliiker", "nombre", "celular"]
        return all(row.get(field) for field in required_fields)

    def insert_batch(self, cursor, batch):
        cursor.executemany(
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
            batch,
        )
        self.mysql.connection.commit()

    def download_gestion(self):
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute(
                """
                SELECT g.*, e.estado, t.tipificacion 
                FROM gestiones g
                LEFT JOIN estadoKliiker e ON g.id_estado = e.id_estado
                LEFT JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion
                """
            )

            column_names = [i[0] for i in cursor.description]
            rows = cursor.fetchall()
            output = io.StringIO()
            writer = csv.writer(output, delimiter=";")

            writer.writerow(column_names)
            for row in rows:
                writer.writerow(
                    [
                        str(row[column]) if row[column] is not None else ""
                        for column in column_names
                    ]
                )

            output.seek(0)
            filename = f"Gestion_{datetime.now().strftime('%Y-%m-%d')}.csv"
            response = make_response(output.getvalue())
            response.headers["Content-Disposition"] = (
                f'attachment; filename="{filename}"'
            )
            response.headers["Content-type"] = "text/csv"
            return response

        except Exception as e:
            return make_response("Error al generar el CSV", 500)
        finally:
            if "cursor" in locals():
                cursor.close()

    def download_historial(self):
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute(
                """
                SELECT h.*, e.estado
                FROM historial_gestiones h
                LEFT JOIN kliiker k ON h.celular = k.celular
                LEFT JOIN usuarios u ON h.nombre_AS = u.nombre_AS
                LEFT JOIN estadoKliiker e ON h.id_estado = e.id_estado
                LEFT JOIN tipificacion t ON h.id_tipificacion = t.id_tipificacion
                """
            )

            column_names = [i[0] for i in cursor.description]
            rows = cursor.fetchall()
            output = io.StringIO()
            writer = csv.writer(output, delimiter=";")

            writer.writerow(column_names)
            for row in rows:
                writer.writerow(
                    [
                        str(row[column]) if row[column] is not None else ""
                        for column in column_names
                    ]
                )

            output.seek(0)
            filename = f"Historial_{datetime.now().strftime('%Y-%m-%d')}.csv"
            response = make_response(output.getvalue())
            response.headers["Content-Disposition"] = (
                f'attachment; filename="{filename}"'
            )
            response.headers["Content-type"] = "text/csv"
            return response

        except Exception as e:
            return make_response("Error al generar el historial", 500)
        finally:
            if "cursor" in locals():
                cursor.close()

    def get_uploaded_files(self):
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute("SELECT * FROM uploaded_db ORDER BY date_upload DESC")
            return cursor.fetchall()
        except Exception as e:
            return []
        finally:
            if "cursor" in locals():
                cursor.close()

    def download_work_day(self):
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute(
                """
                   SELECT k.*, g.fechaProximaGestion, t.cierre_flujo 
                   FROM kliiker k
                   LEFT JOIN (
                       SELECT celular, MAX(fecha) as ultima_fecha 
                       FROM gestiones 
                       GROUP BY celular
                   ) ult_g ON k.celular = ult_g.celular
                   LEFT JOIN gestiones g ON ult_g.celular = g.celular AND ult_g.ultima_fecha = g.fecha
                   LEFT JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion
                """
            )

            column_names = [i[0] for i in cursor.description]
            rows = cursor.fetchall()
            output = io.StringIO()
            writer = csv.writer(output, delimiter=";")

            writer.writerow(column_names)
            for row in rows:
                writer.writerow(
                    [
                        str(row[column]) if row[column] is not None else ""
                        for column in column_names
                    ]
                )

            output.seek(0)
            filename = f"Tarea_Del_{datetime.now().strftime('%d-%m-%Y')}.csv"
            response = make_response(output.getvalue())
            response.headers["Content-Disposition"] = (
                f'attachment; filename="{filename}"'
            )
            response.headers["Content-type"] = "text/csv"
            return response

        except Exception as e:
            return make_response("Error al generar la tarea del dia", 500)
        finally:
            if "cursor" in locals():
                cursor.close()

    def validar_logica_kliiker(self):
        try:
            cursor = self.mysql.connection.cursor(dictionary=True)

            cursor.execute(
                """
                   SELECT k.*, f.diasParaGestion, g.fechaProximaGestion, t.cierre_flujo 
                   FROM kliiker k
                   LEFT JOIN flujotrabajo f ON k.id_estado = f.id_estado
                   LEFT JOIN (
                       SELECT celular, MAX(fecha) as ultima_fecha 
                       FROM gestiones 
                       GROUP BY celular
                   ) ult_g ON k.celular = ult_g.celular
                   LEFT JOIN gestiones g ON ult_g.celular = g.celular AND ult_g.ultima_fecha = g.fecha
                   LEFT JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion
               """
            )

            resultados = []

            for registro in cursor.fetchall():
                if registro.get("gestionable") == 0:
                    resultados.append(False)
                    continue

                if registro.get("cierre_flujo") == 1:
                    resultados.append(False)
                    continue

                dias_sin_gestion = registro.get("diaSinGestion") or 0
                dias_requeridos = registro.get("diasParaGestion") or 0

                if dias_sin_gestion < dias_requeridos:
                    resultados.append(False)
                    continue

                fecha_proxima = registro.get("fechaProximaGestion")
                hoy = date.today()

                if not fecha_proxima:
                    resultados.append(True)
                else:
                    resultados.append(fecha_proxima == hoy)

            return resultados

        except Exception as e:
            print(f"Error al validar la lógica: {e}")
            return []
        finally:
            if "cursor" in locals():
                cursor.close()
