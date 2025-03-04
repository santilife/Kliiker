from flask import Blueprint, session, redirect, url_for, render_template

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")


@admin_bp.route("/")
def dashboard():
    if "username" not in session or session["rol"] != "Administrador":
        return redirect(url_for("auth.login"))
    return render_template("admin/index.html")
