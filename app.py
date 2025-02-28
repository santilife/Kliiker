from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from flask_mysqldb import MySQL
from config import config

# Models
from models.ModelUser import ModelUser

# Entities
from models.entities.User import User


app = Flask(__name__)

# db = MySQL(app)


# ---------------------------------------------------------------------------- #
#                                Conexion MySQL                                #
# ---------------------------------------------------------------------------- #
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'Kliiker'

# conexion = MySQL(app)


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.run(debug=True, port=5000)
