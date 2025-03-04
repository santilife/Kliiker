# Importación de módulos necesarios
import os
from flask import Flask, render_template, request, session, redirect, url_for

# from routes.mostrarKliikler.viewKliiker import mostrar_tabla
from flask_mysqldb import MySQL

# Importación de blueprints desde el módulo de autenticación
from routes.auth_users import auth, iniciar_sesion, administradores, asesores_generales
from routes.mostrarKliikler.viewKliiker import kliiker_table
from routes.route_gestion import ruta_gestion

# from .routes.mostrarKliikler.viewKliiker import obtener_datos

# from routes.admin.admin import admin_bp
# from routes.asesor.asesor import asesor_bp
# from routes.auth_routes import routes_auth
from database.config import db_conexion, mysql

# Inicialización de la aplicación Flask
# Se especifica la carpeta de templates
app = Flask(__name__, template_folder="templates")

# Configuración de la conexión a la base de datos
db_conexion(app)

# Registro de los blueprints para las diferentes rutas de la aplicación
# Blueprint para la página de inicio de sesión
app.register_blueprint(iniciar_sesion)

# Blueprint para la autenticación
app.register_blueprint(auth)

# Blueprint para el panel de administradores
app.register_blueprint(administradores)

# Blueprint para el panel de asesores generales
app.register_blueprint(asesores_generales)

# Mostrar tablas
app.register_blueprint(kliiker_table)
# app.register_blueprint(obtener_datos)

# ruta form gestion
app.register_blueprint(ruta_gestion)

# Blueprint para verificaciones de roles
# app.register_blueprint(admin_bp, url_prefix="/admin")
# app.register_blueprint(asesor_bp, url_prefix="/asesor")


# Punto de entrada de la aplicación
if __name__ == "__main__":
    # Inicia el servidor en modo debug en el puerto 5000
    app.run(debug=True, port=5000, host="0.0.0.0")


# Ruta para mostrar la tabla
# app.route("/")(obtener_datos)
