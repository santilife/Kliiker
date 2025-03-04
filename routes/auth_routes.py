# Se importan los modulos necesarios
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

# Se inicia la app con flask
app = Flask(__name__)

# Blueprints for routes
routes_auth = Blueprint("auth", __name__, template_folder="../templates")


@routes_auth.route("/login", methods=["GET", "POST"])
def login():
    if "logueado" in session:
        return redirect(url_for(f"{session['rol'].lower()}.dashboard"))

    if (
        request.method == "POST"
        and "usuario" in request.form
        and "password" in request.form
    ):
        # Obtenemos la conexión a la base de datos configurada
        try:
            cursor = mysql.connection.cursor()

            usuario = request.form["usuario"]
            password = request.form["password"]

            # Consulta usando parámetros seguros
            cursor.execute(
                "SELECT * FROM usuarios WHERE usuario = %s AND password = %s",
                (usuario, password),
            )
            user = cursor.fetchone()

            if user:
                session["logueado"] = True
                session["usuario"] = user["usuario"]
                session["rol"] = user["rol"]

                return redirect(url_for(f"{user['rol'].lower()}.dashboard"))

            return render_template("auth/login.html", error="Credenciales inválidas")

        except Exception as e:
            # Manejo de errores de base de datos
            print(f"Error de base de datos: {str(e)}")
            return render_template(
                "auth/login.html", error="Error de conexión con la base de datos"
            )

        finally:
            if "cursor" in locals():
                cursor.close()

    return render_template("login.html")
