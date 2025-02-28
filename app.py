from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from flask_mysqldb import MySQL
from config import config

# Models
from models.ModelUser import ModelUser

# Entities
from models.entities.User import User


app = Flask(__name__)

db = MySQL(app)


# ---------------------------------------------------------------------------- #
#                                  Peticiones                                  #
# ---------------------------------------------------------------------------- #
# @app.before_request
# def before_request():
#     print("Antes de la petición...")


# @app.after_request
# def after_request(response):
#     print("Después de la petición")
#     return response


# ---------------------------------------------------------------------------- #
#                                Conexion MySQL                                #
# ---------------------------------------------------------------------------- #
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'Kliiker'

# conexion = MySQL(app)


@app.route("/")
def index():
    return redirect(
        url_for("login")
    )  # al ingresar al la raíz se redirige a la ruta login


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # print(request.form['user'])
        # print(request.form['pass'])
        user = User(0, request.form["user"], request.form["pass"])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for("home"))
            else:
                flash("Invalid...")
                return render_template("/")
        else:
            flash("User no encontrado...")
            return render_template("/")

    else:
        return render_template("login.html")


@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.run(debug=True, port=5000)
