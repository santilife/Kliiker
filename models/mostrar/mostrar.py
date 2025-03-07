# routes/mostrarKliikler/viewKliiker.py
from flask import render_template, Blueprint, current_app
from database.config import mysql

kliiker_table = Blueprint("kliiker_table", __name__)


@kliiker_table.route("/gestion")
def mostrar_tabla():
    try:
        datos = obtener_datos()
        print(f"Datos a enviar a la plantilla: {datos}")
        if not datos:
            print("ADVERTENCIA: No se encontraron datos para mostrar")
        return render_template("formGestion/gestion.html", datos=datos)
    except Exception as e:
        print(f"ERROR al renderizar la plantilla: {str(e)}")
        return f"Error: {str(e)}"


def obtener_datos():
    try:
        cursor = mysql.connection.cursor()

        # Verificación simple - contar registros
        cursor.execute("SELECT COUNT(*) FROM kliiker")
        count = cursor.fetchone()[0]
        print(f"Cantidad de registros en la tabla: {count}")

        if count == 0:
            print("La tabla está vacía")
            return []

        # Verificar estructura de la tabla
        cursor.execute("DESCRIBE kliiker")
        estructura = cursor.fetchall()
        print(f"Estructura de la tabla: {estructura}")

        # Consulta simplificada para depuración
        consulta = """
            SELECT 
                id_kliiker as id_Kliiker,
                nombre,
                apellido,
                celular,
                codigo,
                correo,
                fecha,
                venta
            FROM kliiker
            ORDER BY fecha DESC
        """

        cursor.execute(consulta)

        # Obtener metadatos
        column_names = [column[0] for column in cursor.description]
        print(f"Nombres de columnas: {column_names}")

        datos = cursor.fetchall()
        print(f"Datos obtenidos (primeros 2): {datos[:2] if datos else 'No hay datos'}")

        # Convertir resultados a diccionarios
        resultados = [dict(zip(column_names, row)) for row in datos]
        print(
            f"Resultados formateados (primeros 2): {resultados[:2] if resultados else 'No hay datos'}"
        )

        cursor.close()
        return resultados

    except Exception as err:
        print(f"ERROR al obtener datos: {str(err)}")
        import traceback

        traceback.print_exc()  # Imprime el traceback completo
        return []


def mostrar_tabla():
    datos = obtener_datos()
    return render_template("/formGestion/gestion2.html", datos=datos)
