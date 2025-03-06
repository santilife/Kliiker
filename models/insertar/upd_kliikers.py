from flask import Blueprint, Flask, render_template, url_for, request, redirect, flash
from database.config import mysql

app = Flask(__name__)


def insertar_kliiker():
    try:
        id_Kliiker = request.form.get("id")
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
        
        
        
        """
        mysql.connection.commit()
        cursor.close()

        flash("Registro actualizado correctamente", "success")
    except Exception as e:
        flash(f"Error al actualizar: {str(e)}", "danger")

    return redirect(url_for("mostrar_tabla"))
