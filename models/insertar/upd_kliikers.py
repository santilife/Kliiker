from flask import Blueprint, Flask, render_template, url_for, request, redirect, flash
from database.config import mysql
import MySQLdb
from datetime import datetime

app = Flask(__name__)
actualizar_gestion_modal = Blueprint("actualizar_gestion_modal", __name__)


@actualizar_gestion_modal.route("/actualizar", methods=["POST"])
def actualizar_gestion():
    try:
        print("\n--- Inicio de actualización ---")
        print("Datos recibidos:", dict(request.form))

        datos = {
            "id_gestion": request.form.get("id_gestion"),
            "id_llamada": request.form.get("id_llamada"),
            "estado": request.form.get("estado"),
            "tipificacion": request.form.get("tipificacion"),
            "canal": request.form.get("canal"),
            "motivoNoInteres": request.form.get("motivo_no_interes"),
            "fecha_proxima_gestion": request.form.get("fecha_proxima_gestion"),
            "comentario": request.form.get("Descripcion"),
        }

        print("\nDatos procesados:", datos)

        # Validación crítica
        if not datos["id_gestion"]:
            flash("Error: ID de gestión no proporcionado", "danger")
            return redirect(url_for("mostrar_tabla"))

        with mysql.connection.cursor() as cursor:
            consulta = """
                UPDATE gestiones 
                    SET 
                    id_llamada = %s,
                    estado = %s,
                    tipificacion = %s,
                    canal = %s,
                    motivoNoInteres = %s,
                    fechaProximaGestion = %s,
                    comentario = %s
                    WHERE id_gestion = %s  -- Usar columna correcta
                    """
            parametros = (
                datos["id_llamada"],
                datos["estado"],
                datos["tipificacion"],
                datos["canal"],
                datos["motivo_no_interes"],
                datos["fecha_proxima_gestion"],
                datos["comentario"],
                datos["id_gestion"],
            )

            print("\nConsulta SQL:", cursor.mogrify(consulta, parametros))

            cursor.execute(consulta, parametros)
            affected = cursor.rowcount
            mysql.connection.commit()

            print(f"Registros afectados: {affected}")

            if affected == 0:
                flash("Advertencia: No se actualizó ningún registro", "warning")
            else:
                flash("Actualización exitosa", "success")

    except Exception as e:
        mysql.connection.rollback()
        print(f"\nError: {str(e)}")
        flash(f"Error crítico: {str(e)}", "danger")

    finally:
        print("\n--- Fin de actualización ---\n")

    return redirect(url_for("mostrar_tablas.mostrar_tabla"))
