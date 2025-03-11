from flask import Blueprint, Flask, render_template, url_for, request, redirect, flash
from database.config import mysql
import MySQLdb
from datetime import datetime

app = Flask(__name__)
# Blueprint para manejar las actualizaciones de gestión
actualizar_gestion_modal = Blueprint("actualizar_gestion_modal", __name__)


@actualizar_gestion_modal.route("/actualizar", methods=["POST"])
def actualizar_gestion():
    try:
        print("\n--- Inicio de actualización ---")

        # Definición de campos obligatorios para la actualización
        campos_requeridos = {
            "id_llamada": "ID de llamada",
            "id_estado": "Estado",
            "tipificacion": "Tipificación",
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

        datos = {
            "id_gestion": request.form["id_gestion"],
            "id_llamada": request.form["id_llamada"],
            "id_estado": id_estado,
            "tipificacion": request.form["tipificacion"],
            "canal": request.form["canal"],
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
                if request.form["tipificacion"] == "Sin interes"
                else None
            ),
        }

        # Validación específica para tipificación "Sin interes"
        if datos["tipificacion"] == "Sin interes" and not datos["motivoNoInteres"]:
            flash(
                "Debe seleccionar un motivo cuando la tipificación es 'Sin interés'",
                "danger",
            )
            return redirect(url_for("mostrar_tablas.mostrar_tabla"))

        print("Datos procesados:", datos)

        # Actualización en la base de datos
        with mysql.connection.cursor() as cursor:
            consulta = """
                UPDATE gestiones 
                SET 
                    id_llamada = %s,
                    id_estado = %s,
                    id_fecha = %s,
                    tipificacion = %s,
                    canal = %s,
                    motivoNoInteres = %s,
                    fechaProximaGestion = %s,
                    comentario = %s
                WHERE id_gestion = %s
            """
            parametros = (
                datos["id_llamada"],
                datos["id_estado"],
                datos["fecha_actual"],
                datos["tipificacion"],
                datos["canal"],
                datos["motivoNoInteres"],
                datos["fecha_proxima_gestion"],
                datos["comentario"],
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
