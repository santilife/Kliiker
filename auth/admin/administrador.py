from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    Blueprint,
)

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")


###############
@admin_bp.route("/")
def dashboard():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    elif session["rol"] == "Asesor":
        return redirect(url_for("asesor/index.html"))
    return render_template("admin/index.html")
