from flask import (
    Blueprint,
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    flash,
    session,
)
from database.config import mysql
import MySQLdb
from datetime import datetime

app = Flask(__name__)
# Blueprint para manejar las actualizaciones de gestión
actualizar_gestion_modal = Blueprint("actualizar_gestion_modal", __name__)


@actualizar_gestion_modal.route("/actualizar", methods=["POST"])
def actualizar_gestion():

    tipificaciones = {
        1: "Buzón de voz",
        2: "Equivocado",
        3: "Información general",
        4: "Interesado a futuro",
        5: "Leed ya compro",
        6: "No contesta",
        7: "Novedad en el registro",
        8: "Registro exitoso",
        9: "Seguimiento",
        10: "Sin interes",
        11: "Volver a llamar",
    }
    try:
        print("\n--- Inicio de actualización ---")

        # Definición de campos obligatorios para la actualización
        campos_requeridos = {
            "id_llamada": "ID de llamada",
            "id_estado": "Estado",
            "id_tipificacion": "Tipificación",
            "canal": "Canal",
            "Descripcion": "Descripción",
            "id_gestion": "ID de gestión",
        }

        # Validación de campos requeridos
        for campo, nombre in campos_requeridos.items():
            if not request.form.get(campo):
                flash(f"Error: El campo {nombre} es obligatorio", "danger")
                return redirect(url_for("mostrar_tablas.mostrar_tabla"))

        # Conversión y validación del ID de estado
        try:
            id_estado = int(request.form["id_estado"])
        except ValueError:
            flash("Formato inválido para ID de estado", "danger")
            return redirect(url_for("mostrar_tablas.mostrar_tabla"))

        # Preparación de datos para la actualización
        id_tipificacion = int(request.form["id_tipificacion"])

        datos = {
            "id_gestion": request.form["id_gestion"],
            "id_llamada": request.form["id_llamada"],
            "id_estado": id_estado,
            "celular": request.form["celular"],
            "id_tipificacion": id_tipificacion,
            "canal": request.form["canal"],
            "tipoGestion": request.form["tipoGestion"],
            "fecha_gestion_actual": datetime.now(),
            "fecha_proxima_gestion": (
                datetime.strptime(
                    request.form["fecha_proxima_gestion"], "%Y-%m-%d"
                ).date()
                if request.form["fecha_proxima_gestion"]
                else None
            ),
            "comentario": request.form["Descripcion"],
            "motivoNoInteres": (
                request.form.get("motivo_no_interes")
                if tipificaciones[id_tipificacion] == "Sin interes"
                else None
            ),
            "asesor": session.get("nombre_AS"),
        }

        print("Datos procesados:", datos)

        # Validación específica para tipificación "Sin interes"
        if (
            tipificaciones[id_tipificacion] == "Sin interes"
            and not datos["motivoNoInteres"]
        ):
            flash(
                "Debe seleccionar un motivo cuando la tipificación es 'Sin interés'",
                "danger",
            )
            return redirect(url_for("mostrar_tablas.mostrar_tabla"))

        if datos["id_gestion"] == "None":
            with mysql.connection.cursor() as cursor:
                consulta = """
                INSERT INTO gestiones 
                SET 
                    id_llamada = %s,
                    id_estado = %s,
                    celular = %s,
                    fecha = %s,
                    id_tipificacion = %s,
                    canal = %s,
                    tipoGestion = %s,
                    motivoNoInteres = %s,
                    fechaProximaGestion = %s,
                    comentario = %s,
                    nombre_AS = %s
                """
                parametros = (
                    datos["id_llamada"],
                    datos["id_estado"],
                    datos["celular"],
                    datos["fecha_gestion_actual"],
                    datos["id_tipificacion"],
                    datos["canal"],
                    datos["tipoGestion"],
                    datos["motivoNoInteres"],
                    datos["fecha_proxima_gestion"],
                    datos["comentario"],
                    datos["asesor"],
                )
                print("\nConsulta SQL:", cursor.mogrify(consulta, parametros))
                cursor.execute(consulta, parametros)
                affected = cursor.rowcount
                mysql.connection.commit()

                # Verificación del resultado de la actualización
                if affected == 0:
                    flash("Advertencia: No se insertó ningún registro", "warning")
                else:
                    flash("Insertación exitosa", "success")

            print("Datos procesados:", datos)

        else:
            # Actualización en la base de datos
            with mysql.connection.cursor() as cursor:
                consulta = """
                UPDATE gestiones 
                SET 
                    id_llamada = %s,
                    id_estado = %s,
                    fecha = %s,
                    id_tipificacion = %s,
                    canal = %s,
                    tipoGestion = %s,
                    motivoNoInteres = %s,
                    fechaProximaGestion = %s,
                    comentario = %s,
                    nombre_AS = %s
                WHERE id_gestion = %s
                """
                parametros = (
                    datos["id_llamada"],
                    datos["id_estado"],
                    datos["fecha_gestion_actual"],
                    datos["id_tipificacion"],
                    datos["canal"],
                    datos["tipoGestion"],
                    datos["motivoNoInteres"],
                    datos["fecha_proxima_gestion"],
                    datos["comentario"],
                    datos["asesor"],
                    datos["id_gestion"],
                )

                print("\nConsulta SQL:", cursor.mogrify(consulta, parametros))
                cursor.execute(consulta, parametros)
                affected = cursor.rowcount
                mysql.connection.commit()

                # Verificación del resultado de la actualización
                if affected == 0:
                    flash("Advertencia: No se actualizó ningún registro", "warning")
                else:
                    flash("Actualización exitosa", "success")

    except Exception as e:
        mysql.connection.rollback()
        print(f"\nError crítico: {str(e)}")
        flash(f"Error inesperado: {str(e)}", "danger")
    finally:
        print("\n--- Fin de actualización ---\n")

    return redirect(url_for("mostrar_tablas.mostrar_tabla"))
