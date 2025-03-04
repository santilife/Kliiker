# Importación de módulos necesarios
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
)

# Importación de la conexión a la base de datos
from database.config import mysql

# Importación de la función de seguridad para verificar contraseñas
from werkzeug.security import check_password_hash

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Definición de Blueprints para diferentes rutas
iniciar_sesion = Blueprint("iniciar_sesion", __name__)
administradores = Blueprint("administradores", __name__)
asesores_generales = Blueprint("asesores_generales", __name__)


# Ruta para el panel de administradores
@administradores.route("/admin")
def admin():
    return render_template("admin/index.html")


# Ruta para el panel de asesores generales
@asesores_generales.route("/asesor")
def asesor():
    return render_template("asesor/index.html")


# Ruta para mostrar el formulario de inicio de sesión
@iniciar_sesion.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")


# Blueprint para la autenticación
auth = Blueprint("auth", __name__)


# Ruta para procesar el inicio de sesión
@auth.route("/acceso", methods=["GET", "POST"])
def acceso():
    # Inicializa la conexión a la base de datos
    db_conexion(app)

    # Verifica si se recibió una solicitud POST con usuario y contraseña
    if (
        request.method == "POST"
        and "usuario" in request.form
        and "password" in request.form
    ):
        usuario = request.form["usuario"]
        password = request.form["password"]

        # Consulta a la base de datos para verificar las credenciales
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM usuarios WHERE usuario = %s AND password = %s",
            (usuario, password),
        )
        user = cur.fetchone()
        cur.close()

        # Si se encuentra el usuario
        if user:
            # Establece las variables de sesión
            session["logueado"] = True
            session["usuario"] = user["usuario"]
            session["rol"] = user["rol"]

            # Redirecciona según el rol del usuario
            if user["rol"] == "Administrador":
                return redirect(url_for("administradores.admin"))
            elif user["rol"] == "Asesor":
                return redirect(url_for("asesores_generales.asesor"))

        else:
            # Si las credenciales son inválidas, vuelve al formulario de login
            return render_template("login.html")
    # Para solicitudes GET, muestra el formulario de login
    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("iniciar_sesion.login"))
