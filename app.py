# --------------------- Importación de módulos necesarios -------------------- #
import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_login import LoginManager

# --------------------------- Impotacion blueprints -------------------------- #
# from auth.admin.administrador import admin_bp
# from auth.asesor.asesor import asesor_bp

from models.mostrar.view_kliikers import kliiker_table
from database.config import db_conexion, mysql
from auth.auth_users import administradores, asesores_generales, auth, iniciar_sesion

# -------------------------- Inicializacion de Flask ------------------------- #
app = Flask(__name__, template_folder="templates")

# ------------------------------ Login Required ------------------------------ #
'''login_manager = LoginManager(app)
login_manager.login_view = "login"'''

# -------------- Configuración de la conexión a la base de datos ------------- #
db_conexion(app)


app.register_blueprint(iniciar_sesion)

app.register_blueprint(auth)

app.register_blueprint(administradores)

app.register_blueprint(asesores_generales)

app.register_blueprint(kliiker_table)


# ---- GRAFICAS-----
estados = ["Estado A", "Estado B", "Estado C"]
frecuencia_estados = [50, 30, 20]

tipificaciones = ["Tipificación X", "Tipificación Y", "Tipificación Z"]
frecuencia_tipificaciones = [40, 35, 25]


# # Ruta principal para mostrar la página de estadísticas
@app.route("/estadisticas")
def index():
    # Pasar los datos a la plantilla estadisticas.html
    return render_template(
        "estadisticas/estadisticas.html",
        estados=estados,
        frecuencia_estados=frecuencia_estados,
        tipificaciones=tipificaciones,
        frecuencia_tipificaciones=frecuencia_tipificaciones,
    )


# Ruta para proporcionar datos en formato JSON
@app.route("/estadisticas")
def api_estadisticas():
    datos_estadisticas = {
        "estados": [
            {"estado": e, "cantidad": f} for e, f in zip(estados, frecuencia_estados)
        ],
        "tipificaciones": [
            {"tipificacion": t, "cantidad": f}
            for t, f in zip(tipificaciones, frecuencia_tipificaciones)
        ],
    }
    return jsonify(datos_estadisticas)


if __name__ == "__main__":
    # Inicia el servidor en modo debug en el puerto 5000
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
