from flask import Blueprint, Flask

app = Flask(__name__)


# ---------------------------------------------------------------------------- #
#                  Blueprints relacionados al inicio de sesion                 #
# ---------------------------------------------------------------------------- #
iniciar_sesion = Blueprint("iniciar_sesion", __name__, template_folder="templates")
administradores = Blueprint("administradores", __name__)
asesores_generales = Blueprint("asesores_generales", __name__)
# Blueprint para la autenticación
auth = Blueprint("auth", __name__, template_folder="templates")
admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")
asesor_bp = Blueprint("asesor", __name__, template_folder="../templates/asesor")


# ---------------------------------------------------------------------------- #
#    Blueprints relacionados a las consultas, modificaciones, eliminaciones    #
# ---------------------------------------------------------------------------- #
actualizar = Blueprint("updates", __name__)
kliiker_table = Blueprint("kliiker_table", __name__)
