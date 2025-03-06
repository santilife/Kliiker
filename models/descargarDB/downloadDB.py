from flask import Flask, request, render_template, redirect, url_for, send_file
from database.config import mysql
from dotenv import load_dotenv
import os
import io
import MySQLdb

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "archivo" not in request.files:
        return "No se seleccionó ningún archivo", 400

    file = request.files["archivo"]

    if file.filename == "":
        return "Nombre de archivo inválido", 400

    try:
        # Leer datos del archivo
        file_data = file.read()
        filename = file.filename
        mime_type = file.mimetype
        file_size = len(file_data)

        # Generar nombre único para el archivo
        unique_name = f"{os.urandom(16).hex()}_{filename}"

        # Insertar en base de datos
        cur = mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO archivos (
                nombre_original,
                nombre_servidor,
                tipo_mime,
                tamano,
                contenido
            ) VALUES (%s, %s, %s, %s, %s)
        """,
            (filename, unique_name, mime_type, file_size, file_data),
        )

        mysql.connection.commit()
        cur.close()

        return redirect(url_for("lista_archivos"))

    except MySQLdb.Error as e:
        mysql.connection.rollback()
        return f"Error de base de datos: {str(e)}", 500
    except Exception as e:
        return f"Error inesperado: {str(e)}", 500


@app.route("/archivos")
def lista_archivos():
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT id, nombre_original, tipo_mime, tamano, fecha_subida
            FROM archivos
            ORDER BY fecha_subida DESC
        """
        )
        archivos = cur.fetchall()
        cur.close()
        return render_template("lista.html", archivos=archivos)
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route("/download/<int:file_id>")
def download_file(file_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT nombre_original, tipo_mime, contenido
            FROM archivos
            WHERE id = %s
        """,
            (file_id,),
        )
        archivo = cur.fetchone()
        cur.close()

        if not archivo:
            return "Archivo no encontrado", 404

        return send_file(
            io.BytesIO(archivo["contenido"]),
            mimetype=archivo["tipo_mime"],
            as_attachment=True,
            download_name=archivo["nombre_original"],
        )

    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
