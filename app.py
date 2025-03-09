# --------------------- Importación de módulos necesarios -------------------- #
import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_login import LoginManager
from flask_cors import CORS

# --------------------------- Importación blueprints -------------------------- #
# from auth.admin.administrador import admin_bp
# from auth.asesor.asesor import asesor_bp

from models.actualizar.upd_kliikers import actualizar_gestion_modal
from models.mostrar.view_kliikers import mostrar_tablas
from database.config import db_conexion
from auth.auth_users import administradores, asesores_generales, auth, iniciar_sesion
from models.mostrar.view_usersAS import mostrar_asesores_tables
from models.insertar.ins_usersAS import insertar_asesor
from models.estadisticas.estadisticas import estadisticas_bp

# from models.descargarDB.downloadDB import downloadDB

# -------------------------- Inicialización de Flask ------------------------- #
app = Flask(__name__, template_folder="templates")
CORS(app)
# ------------------------------ Login Required ------------------------------ #
'''login_manager = LoginManager(app)
login_manager.login_view = "login"'''

# -------------- Configuración de la conexión a la base de datos ------------- #
db_conexion(app)

# ------------------------ Registro de Blueprints ---------------------------- #
# Autenticación y manejo de sesiones
app.register_blueprint(iniciar_sesion)
app.register_blueprint(auth)

# Rutas de administración
app.register_blueprint(administradores)
app.register_blueprint(asesores_generales)

# Rutas de gestión y visualización
app.register_blueprint(mostrar_tablas)
app.register_blueprint(actualizar_gestion_modal)
app.register_blueprint(mostrar_asesores_tables)
app.register_blueprint(insertar_asesor)

# ---- GRAFICAS-----
app.register_blueprint(estadisticas_bp)

if __name__ == "__main__":
    # Inicia el servidor en modo debug en el puerto 5000
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
