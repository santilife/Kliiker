# --------------------- Importación de módulos necesarios -------------------- #
from database.config import db_conexion
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session,
    Response,
    jsonify,
    flash,
)
from datetime import datetime
import os
import subprocess
from models.mostrar.view_kliikers import mostrar_tabla
from database.config import mysql
from werkzeug.security import check_password_hash
from auth.decorators import login_required, role_required
from models.descargarDB.downloadDB import CSVProcessor

csv_processor = CSVProcessor(mysql)

# -------------------------- Inicialización de Flask ------------------------- #
app = Flask(__name__)

# ----------------------- Definición de Blueprints -------------------------- #
iniciar_sesion = Blueprint("iniciar_sesion", __name__, template_folder="templates")
administradores = Blueprint("administradores", __name__)
asesores_generales = Blueprint("asesores_generales", __name__)
auth = Blueprint("auth", __name__, template_folder="templates")


# ------------------------- Rutas de Estadísticas --------------------------- #
@administradores.route("/estadisticas")
def ver_estadisticas():
    return render_template("estadisticas/estadisticas.html")


# API endpoints para estadísticas
@administradores.route("/api/estadisticas/estados")
def api_estados():
    return jsonify(
        {
            "timestamp": datetime.now().isoformat(),
        }
    )


@administradores.route("/api/estadisticas/tipificaciones")
def api_tipificaciones():
    return jsonify(
        {
            "timestamp": datetime.now().isoformat(),
        }
    )


# ------------------------- Panel de Administración ------------------------- #
@administradores.route("/admin", methods=["GET", "POST"])
@login_required
@role_required("Administrador")
def admin():
    return mostrar_tabla()


# Rutas para gestión de base de datos
@administradores.route("/admin/downloadDB")
@login_required
@role_required("Administrador")
def downloadDB():
    databases = csv_processor.get_uploaded_files()
    return render_template("descargarDB/downloadDB.html", databases=databases)


# ------------- Rutas para la carga y descarga de bases de datos ------------- #
@administradores.route("/uploadDB", methods=["POST"])
def subir_csv():
    result = csv_processor.handle_upload(request)
    flash(result["message"], result["status"])
    return redirect(url_for("administradores.downloadDB"))


@administradores.route("/descargar/gestion")
def descargar_gestion():
    response = csv_processor.download_gestion()
    if response:
        return response
    flash("Error al generar el archivo de gestión", "error")
    return csv_processor.download_gestion()


@administradores.route("/upload_process_csv", methods=["POST"])
@login_required
@role_required("Administrador")
def upload_and_process_csv():
    try:
        # Validación original
        if "csvFile" not in request.files:
            return (
                jsonify({"success": False, "message": "No se encontró el archivo"}),
                400,
            )

        file = request.files["csvFile"]
        if file.filename == "":
            return (
                jsonify({"success": False, "message": "Archivo no seleccionado"}),
                400,
            )

        if not file.filename.lower().endswith(".csv"):
            return jsonify({"success": False, "message": "Solo archivos CSV"}), 400

        # Guardar CSV temporal
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_csv_path = os.path.join(
            temp_dir, f"upload_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        )
        file.save(temp_csv_path)

        # MODIFICACIÓN 1: Generar nombre del JSON con ruta absoluta
        json_file = os.path.abspath(
            f"Kliiker_{datetime.now().strftime('%d-%m-%Y')}.json"
        )

        # Convertir CSV a JSON
        try:
            conversion_result = subprocess.run(
                ["python", "script_csv-json.py", temp_csv_path],
                capture_output=True,
                text=True,
                check=True,
            )
            app.logger.info(f"Conversión exitosa: {conversion_result.stdout}")

        except subprocess.CalledProcessError as e:
            error_msg = f"Error en conversión: {e.stderr}"
            app.logger.error(error_msg)
            return jsonify({"success": False, "message": error_msg}), 500

        # MODIFICACIÓN 2: Pasar la ruta del JSON al script de importación
        try:
            import_result = subprocess.run(
                ["python", "script_importar.py", json_file],  # <- Ruta dinámica
                capture_output=True,
                text=True,
                check=True,
            )
            app.logger.info(f"Importación exitosa: {import_result.stdout}")

        except subprocess.CalledProcessError as e:
            error_msg = f"Error en importación: {e.stderr}"
            app.logger.error(error_msg)
            return jsonify({"success": False, "message": error_msg}), 500

        # Registrar en base de datos
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO uploaded_db (nombre, date_upload, size) VALUES (%s, %s, %s)",
                (file.filename, datetime.now(), os.path.getsize(temp_csv_path)),
            )
            mysql.connection.commit()

        except Exception as e:
            app.logger.error(f"Error registrando en DB: {str(e)}")
            mysql.connection.rollback()

        # MODIFICACIÓN 3: Limpieza de archivos temporales
        finally:
            if os.path.exists(temp_csv_path):
                os.remove(temp_csv_path)
            if os.path.exists(json_file):  # Eliminar JSON después de importar
                try:
                    os.remove(json_file)
                except Exception as e:
                    app.logger.error(f"Error eliminando JSON: {str(e)}")

        return jsonify(
            {
                "success": True,
                "message": "Datos importados exitosamente",
                "original_filename": file.filename,
            }
        )

    except Exception as e:
        app.logger.error(f"Error inesperado: {str(e)}")
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@administradores.route("/descargar/historial")
def descargar_historial():
    return csv_processor.download_historial()


@administradores.route("/descargar/tarea_del_dia")
def download_today_work():
    return csv_processor.download_work_day()


# ---------------------------- Panel de Asesores ---------------------------- #
@asesores_generales.route("/asesor")
@login_required
@role_required("Asesor")
def asesor():
    return mostrar_tabla()


# ------------------------- Gestión de Sesiones ---------------------------- #
# Ruta para mostrar el formulario de login
@iniciar_sesion.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")


# Ruta para procesar el inicio de sesión
@auth.route("/acceso", methods=["GET", "POST"])
def acceso():
    # Inicializa la conexión a la base de datos
    db_conexion(app)

    # Verifica credenciales del usuario
    if (
        request.method == "POST"
        and "usuario" in request.form
        and "password" in request.form
    ):
        usuario = request.form["usuario"]
        password = request.form["password"]

        # Consulta a la base de datos
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM usuarios WHERE usuario = %s AND password = %s",
            (usuario, password),
        )
        user = cur.fetchone()
        cur.close()
        print(user)
        # Si el usuario existe, establece la sesión
        if user:
            session["logueado"] = True
            session["usuario"] = user["usuario"]
            session["rol"] = user["rol"]
            session["nombre_AS"] = user["nombre_AS"]
            session["estadoUsuario"] = user["estadoUsuario"]

            # Redirección según el rol
            if user["rol"] == "Administrador":
                if user["estadoUsuario"] == 1:
                    return redirect(url_for("administradores.admin"))
                else:
                    return render_template("login.html")

            elif user["rol"] == "Asesor":
                if user["estadoUsuario"] == 1:
                    return redirect(url_for("asesores_generales.asesor"))
                else:
                    return render_template("login.html")

        else:
            return render_template("login.html")
    return render_template("login.html")


# Ruta para cerrar sesión
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("iniciar_sesion.login"))
