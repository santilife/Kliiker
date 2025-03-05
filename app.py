# Importación de módulos necesarios
import os
from flask import Flask, render_template, request, session, redirect, url_for

# from routes.mostrarKliikler.viewKliiker import mostrar_tabla
from flask_mysqldb import MySQL

# Importación de blueprints desde el módulo de autenticación
from routes.rutas_generales import (
    auth,
    iniciar_sesion,
    administradores,
    asesores_generales,
)
from models.mostrar.view_kliikers import kliiker_table

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

# Punto de entrada de la aplicación
if __name__ == "__main__":
    # Inicia el servidor en modo debug en el puerto 5000
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
