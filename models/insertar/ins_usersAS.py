from flask import Blueprint, flash, redirect, url_for, request
from database.config import mysql
from werkzeug.security import generate_password_hash
import MySQLdb

insertar_asesor = Blueprint("insertar_asesor", __name__)

@insertar_asesor.route("/insertar_asesor", methods=["POST"])
def insertar():
    try:
        print("\n--- Inicio de inserción ---")
        
        # Validación de campos requeridos
        campos_requeridos = {
            "nombre": "Nombre completo",
            "documento": "Documento",
            "usuario": "Usuario",
            "rol": "Rol"
        }

        for campo_form, nombre in campos_requeridos.items():
            if not request.form.get(campo_form):
                flash(f"Error: El campo {nombre} es obligatorio", "danger")
                return redirect(url_for("mostrar_asesores_tables.mostrar_asesores"))

        # Convertir documento a entero
        try:
            documento = int(request.form["documento"])
        except ValueError:
            flash("El documento debe ser un número válido", "danger")
            return redirect(url_for("mostrar_asesores_tables.mostrar_asesores"))

        # Verificar duplicados
        with mysql.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM usuarios WHERE documento = %s OR usuario = %s",
                (documento, request.form["usuario"])
            )
            if cursor.fetchone():
                flash("Documento o usuario ya existen en el sistema", "danger")
                return redirect(url_for("mostrar_asesores_tables.mostrar_asesores"))

        # Hashear contraseña
        # hashed_pw = generate_password_hash(request.form["password"])

        # Preparar datos
        datos = {
            "nombre_AS": request.form["nombre"],
            "documento": documento,
            "usuario": request.form["usuario"],
            "rol": request.form["rol"],
            "password": documento
        }

        print("Datos procesados:", datos)

        # Ejecutar inserción
        with mysql.connection.cursor() as cursor:
            consulta = """
                INSERT INTO usuarios (
                    nombre_AS,
                    documento,
                    usuario,
                    rol,
                    password
                ) VALUES (%s, %s, %s, %s, %s)
            """
            parametros = (
                datos["nombre_AS"],
                datos["documento"],
                datos["usuario"],
                datos["rol"],
                datos["password"]
            )

            print("\nConsulta SQL:", cursor.mogrify(consulta, parametros))
            cursor.execute(consulta, parametros)
            mysql.connection.commit()

            flash("Asesor creado exitosamente", "success")

    except MySQLdb.IntegrityError as e:
        mysql.connection.rollback()
        flash("Error: Datos duplicados en la base de datos", "danger")
    except MySQLdb.Error as e:
        mysql.connection.rollback()
        flash(f"Error de base de datos: {e.args[1]}", "danger")
    except Exception as e:
        mysql.connection.rollback()
        print(f"\nError crítico: {str(e)}")
        flash(f"Error inesperado: {str(e)}", "danger")
    finally:
        print("\n--- Fin de inserción ---\n")

    return redirect(url_for("mostrar_asesores_tables.mostrar_asesores"))