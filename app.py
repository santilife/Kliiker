# --------------------- Importación de módulos necesarios -------------------- #
import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_login import LoginManager

# --------------------------- Impotacion blueprints -------------------------- #
# from auth.admin.administrador import admin_bp
# from auth.asesor.asesor import asesor_bp

from models.insertar.upd_kliikers import actualizar_gestion_modal
from models.mostrar.view_kliikers import mostrar_tablas
from database.config import db_conexion
from auth.auth_users import administradores, asesores_generales, auth, iniciar_sesion
from models.mostrar.view_usersAS import asesores_tables

# from models.descargarDB.downloadDB import downloadDB

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

# app.register_blueprint(downloadDB)

app.register_blueprint(mostrar_tablas)

app.register_blueprint(actualizar_gestion_modal)

app.register_blueprint(asesores_tables)

# ---- GRAFICAS-----

if __name__ == "__main__":
    # Inicia el servidor en modo debug en el puerto 5000
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
