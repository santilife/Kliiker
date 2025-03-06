from flask import Blueprint, session, redirect, url_for, render_template
from routes.rutas_generales import asesor_bp

asesor_bp = Blueprint("asesor", __name__, template_folder="../templates/asesor")


@asesor_bp.route("/")
def dashboard():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    elif session["rol"] == "Administrador":
        return redirect(url_for("admin/index.html"))
    return render_template("asesor/index.html")
