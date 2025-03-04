from flask import Blueprint, session, redirect, url_for, render_template

asesor_bp = Blueprint("asesor", __name__, template_folder="../templates/asesor")


@asesor_bp.route("/")
def dashboard():
    if "username" not in session or session["rol"] != "Asesor":
        return redirect(url_for("auth.login"))
    return render_template("asesor/index.html")
