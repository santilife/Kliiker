from flask import Blueprint, Flask, render_template, url_for, request, redirect, flash
from database.config import mysql
from routes.rutas_generales import actualizar

app = Flask(__name__)


@actualizar.route("/update")
def actualizar_kliiker():
    try:
        id_kliiker = request.form.get("id")
        # Obtener todos los datos del formulario
        nuevos_datos = {
            "nombre": request.form.get("nombre"),
            "apellido": request.form.get("apellido"),
            "celular": request.form.get("celular"),
            "correo": request.form.get("correo"),
            "fecha": request.form.get("fecha"),
            "codigo": 1 if request.form.get("codigo") else 0,
            "venta": 1 if request.form.get("venta") else 0,
        }

        # Actualizar en la base de datos
        cursor = mysql.connection.cursor()
        consulta = """
            UPDATE kliiker 
            SET nombre = %s,
                apellido = %s,
                celular = %s,
                correo = %s,
                fecha = %s,
                codigo = %s,
                venta = %s
            WHERE id_kliiker = %s
        """
        cursor.execute(
            consulta,
            (
                nuevos_datos["nombre"],
                nuevos_datos["apellido"],
                nuevos_datos["celular"],
                nuevos_datos["correo"],
                nuevos_datos["fecha"],
                nuevos_datos["codigo"],
                nuevos_datos["venta"],
                id_kliiker,
            ),
        )
        mysql.connection.commit()
        cursor.close()

        flash("Registro actualizado correctamente", "success")
    except Exception as e:
        flash(f"Error al actualizar: {str(e)}", "danger")

    return redirect(url_for("mostrar_tabla"))
