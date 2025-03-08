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
)
from datetime import datetime
from models.mostrar.view_kliikers import mostrar_tabla
from database.config import mysql
from werkzeug.security import check_password_hash
from auth.decorators import login_required, role_required
from models.descargarDB.downloadDB import export_json

# -------------------------- Inicialización de Flask ------------------------- #
app = Flask(__name__)

# ----------------------- Definición de Blueprints -------------------------- #
iniciar_sesion = Blueprint("iniciar_sesion", __name__, template_folder="templates")
administradores = Blueprint("administradores", __name__)
asesores_generales = Blueprint("asesores_generales", __name__)
auth = Blueprint("auth", __name__, template_folder="templates")

# ------------------------- Rutas de Administrador -------------------------- #
@administradores.route("/admin/json")
def json():
    return mostrar_tabla(), export_json()

# ------------------------- Rutas de Estadísticas --------------------------- #
@administradores.route("/estadisticas")
def ver_estadisticas():
    return render_template("estadisticas/estadisticas.html")

# API endpoints para estadísticas
@administradores.route("/api/estadisticas/estados")
def api_estados():
    return jsonify({
        "timestamp": datetime.now().isoformat(),
    })

@administradores.route("/api/estadisticas/tipificaciones")
def api_tipificaciones():
    return jsonify({
        "timestamp": datetime.now().isoformat(),
    })

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
    return render_template("descargarDB/downloadDB.html")

@administradores.route("/admin/listDB")
@login_required
@role_required("Administrador")
def listDB():
    return render_template("descargarDB/listDB.html")

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
    if request.method == "POST" and "usuario" in request.form and "password" in request.form:
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

        # Si el usuario existe, establece la sesión
        if user:
            session["logueado"] = True
            session["usuario"] = user["usuario"]
            session["rol"] = user["rol"]

            # Redirección según el rol
            if user["rol"] == "Administrador":
                return redirect(url_for("administradores.admin"))
            elif user["rol"] == "Asesor":
                return redirect(url_for("asesores_generales.asesor"))

        else:
            return render_template("login.html")
    return render_template("login.html")

# Ruta para cerrar sesión
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("iniciar_sesion.login"))
