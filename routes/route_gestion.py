from flask import Flask, render_template, Blueprint

ruta_gestion = Blueprint("ruta_gestion", __name__)


app = Flask(__name__, template_folder="../templates")


@ruta_gestion.route("/Gestion")
def formGestion():
    return render_template("formGestion/gestion.html")
