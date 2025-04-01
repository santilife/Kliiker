import io
import os
import csv
import json
import random
from datetime import datetime, date
from flask import flash, make_response
from werkzeug.utils import secure_filename
from database.config import mysql

# Mapeo de nombres de campos
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

UPLOAD_FOLDER = "dbUploaded"
ALLOWED_EXTENSIONS = {"csv"}


class CSVProcessor:
    def __init__(self, mysql):
        self.mysql = mysql
        # Asegurar que el directorio de upload existe
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    def smart_mapping(self, field_name):
        return FIELD_MAPPING.get(field_name.lower().strip(), field_name.lower().strip())

    def allowed_file(self, filename):
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    def csv_to_json(self, csv_path):
        """Convierte un archivo CSV a JSON con limpieza de datos"""
        try:
            with open(csv_path, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile, delimiter=";")
                # Normalizar nombres de columnas
                fieldnames = [
                    self.smart_mapping(fn.strip()) for fn in reader.fieldnames
                ]
                reader.fieldnames = fieldnames

                data = [row for row in reader]

                json_filename = f"temp_{random.randint(1000,9999)}.json"
                json_path = os.path.join(UPLOAD_FOLDER, json_filename)

                with open(json_path, "w", encoding="utf-8") as jsonfile:
                    json.dump(data, jsonfile, indent=4, ensure_ascii=False)

                return json_path
        except Exception as e:
            raise Exception(f"Error en conversión CSV a JSON: {str(e)}")

    def handle_csv_upload(self, request):
        """Maneja todo el proceso de carga: CSV -> JSON -> MySQL"""
        if "file" not in request.files:
            return {"status": "error", "message": "No se encontró el archivo"}

        file = request.files["file"]
        if file.filename == "":
            return {"status": "error", "message": "Archivo no seleccionado"}

        if not self.allowed_file(file.filename):
            return {
                "status": "error",
                "message": "Solo se permiten archivos CSV (.csv)",
            }

        csv_path = None
        json_path = None
        cursor = None

        try:
            # 1. Guardar CSV temporalmente
            filename = secure_filename(file.filename)
            csv_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(csv_path)

            # 2. Convertir a JSON
            json_path = self.csv_to_json(csv_path)

            # 3. Procesar JSON e insertar en MySQL
            with open(json_path, "r", encoding="utf-8") as jsonfile:
                data = json.load(jsonfile)

                cursor = self.mysql.connection.cursor()
                batch_size = 1000
                batch = []
                total_registros = 0

                for row in data:
                    processed = self.process_row(row)
                    if not self.validate_kliiker(processed):
                        continue

                    batch.append(processed)
                    if len(batch) >= batch_size:
                        self.insert_batch(cursor, batch)
                        total_registros += len(batch)
                        batch = []

                if batch:
                    self.insert_batch(cursor, batch)
                    total_registros += len(batch)

                # Registrar en uploaded_db
                cursor.execute(
                    "INSERT INTO uploaded_db (nombre, date_upload) VALUES (%s, %s)",
                    (filename, datetime.now()),
                )
                self.mysql.connection.commit()

            return {
                "status": "success",
                "message": f"Archivo procesado correctamente. {total_registros} registros insertados/actualizados",
            }

        except Exception as e:
            if cursor and self.mysql.connection:
                self.mysql.connection.rollback()
            return {"status": "error", "message": f"Error en procesamiento: {str(e)}"}
        finally:
            if cursor:
                cursor.close()
            # Limpieza de archivos temporales
            if csv_path and os.path.exists(csv_path):
                os.remove(csv_path)
            if json_path and os.path.exists(json_path):
                os.remove(json_path)

    def process_row(self, raw_row):
        """Procesamiento avanzado de filas con conversión de tipos"""
        processed = {
            self.smart_mapping(k): v.strip() if isinstance(v, str) else v
            for k, v in raw_row.items()
        }

        # Conversión de tipos de datos
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
                        converter(processed[field])
                        if processed[field] is not None
                        else None
                    )
                except (ValueError, TypeError):
                    processed[field] = None

        # Formateo de fechas
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
                            str(processed[field]), fmt
                        ).date()
                        break
                    except (ValueError, TypeError):
                        continue
                else:
                    processed[field] = None

        return processed

    def validate_kliiker(self, row):
        """Valida campos obligatorios para inserción"""
        required_fields = ["id_kliiker", "nombre", "celular"]
        return all(row.get(field) for field in required_fields)

    def insert_batch(self, cursor, batch):
        """Inserta lotes de datos con manejo de duplicados"""
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
        """Genera reporte CSV de gestiones"""
        cursor = None
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
            return make_response(f"Error al generar el reporte: {str(e)}", 500)
        finally:
            if cursor:
                cursor.close()

    def download_historial(self):
        """Genera reporte CSV del historial"""
        cursor = None
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute(
                """
                SELECT h.*, e.estado, t.tipificacion
                FROM historial_gestiones h
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
            return make_response(f"Error al generar el historial: {str(e)}", 500)
        finally:
            if cursor:
                cursor.close()

    def get_uploaded_files(self):
        """Obtiene listado de archivos subidos"""
        cursor = None
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute("SELECT * FROM uploaded_db ORDER BY date_upload DESC")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener archivos subidos: {str(e)}")
            return []
        finally:
            if cursor:
                cursor.close()

    def download_work_day(self):
        """Genera CSV con la tarea del día"""
        cursor = None
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute(
                """
                SELECT 
                    k.id_Kliiker AS id_cliente,
                    k.nombre,
                    k.apellido,
                    k.celular,
                    k.correo,
                    k.nivel,
                    g.fechaProximaGestion,
                    t.tipificacion
                FROM kliiker k
                LEFT JOIN (
                    SELECT celular, MAX(fecha) as ultima_fecha 
                    FROM gestiones 
                    GROUP BY celular
                ) ult_g ON k.celular = ult_g.celular
                LEFT JOIN gestiones g ON ult_g.celular = g.celular AND ult_g.ultima_fecha = g.fecha
                LEFT JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion
                WHERE 
                    (k.venta = 0 OR k.venta IS NULL)
                    AND (k.gestionable = 1 OR k.gestionable IS NULL)
                    AND (
                        g.id_gestion IS NULL
                        OR (
                            COALESCE(t.cierre_flujo, 0) = 0
                            AND (
                                g.fechaProximaGestion = CURDATE()
                                OR (
                                    k.diaSinGestion IS NOT NULL 
                                    AND k.fechaSinGestion IS NOT NULL
                                    AND DATEDIFF(CURDATE(), k.fechaSinGestion) >= k.diaSinGestion
                                )
                            )
                        )
                    )
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
            return make_response(f"Error al generar la tarea: {str(e)}", 500)
        finally:
            if cursor:
                cursor.close()

    def validar_logica_kliiker(self):
        """Valida la lógica de gestión para cada registro"""
        cursor = None
        try:
            cursor = self.mysql.connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT 
                    k.*, 
                    f.diasParaGestion, 
                    g.fechaProximaGestion, 
                    t.cierre_flujo
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
            hoy = date.today()

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
                if not fecha_proxima:
                    resultados.append(True)
                else:
                    resultados.append(fecha_proxima == hoy)

            return resultados

        except Exception as e:
            print(f"Error en validación: {str(e)}")
            return []
        finally:
            if cursor:
                cursor.close()
