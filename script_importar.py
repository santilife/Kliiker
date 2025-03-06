# Importación de bibliotecas necesarias
from flask import Flask  # Framework web para crear la aplicación
from flask_mysqldb import MySQL  # Extensión Flask para conectar con MySQL
from datetime import datetime  # Para manejar fechas
import json  # Para leer archivos JSON

# Crear instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de la conexión a MySQL
app.config["MYSQL_HOST"] = "localhost"  # Servidor de la base de datos
app.config["MYSQL_USER"] = "root"  # Usuario de MySQL
app.config["MYSQL_PASSWORD"] = ""  # Contraseña de MySQL
app.config["MYSQL_DB"] = "Kliiker1"  # Nombre de la base de datos
app.config["MYSQL_CURSORCLASS"] = (
    "DictCursor"  # Tipo de cursor que retorna resultados como diccionarios
)

# Inicializar la conexión MySQL
mysql = MySQL(app)


def importar_datos_desde_json():
    """
    Función principal que lee un archivo JSON y guarda sus datos en la base de datos MySQL.
    Returns:
        bool: True si la importación fue exitosa, False si hubo algún error
    """
    try:
        # Abrir y leer el archivo JSON con codificación UTF-8
        with open("kliiker30.json", "r", encoding="utf-8") as file:
            datos = json.load(file)

        # Crear un contexto de aplicación Flask para poder usar la conexión MySQL
        with app.app_context():
            cursor = mysql.connection.cursor()

            # Iterar sobre cada registro en el archivo JSON
            for registro in datos:
                # Convertir el formato de fecha de dd/mm/yyyy a yyyy-mm-dd (formato MySQL)
                fecha_original = registro["fecha"]
                try:
                    fecha_mysql = datetime.strptime(
                        fecha_original, "%d/%m/%Y"
                    ).strftime("%Y-%m-%d")
                except ValueError:
                    fecha_mysql = None  # Si la fecha no es válida, se guarda como NULL

                # Manejar casos donde id_kliiker está vacío
                id_kliiker = registro.get("id_kliiker") or None

                # Ejecutar la consulta SQL para insertar el registro
                cursor.execute(
                    """
                    INSERT INTO kliiker (
                        id_Kliiker, 
                        nombre, 
                        apellido, 
                        celular, 
                        nivel, 
                        correo, 
                        fecha
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        id_kliiker,
                        registro["nombre"],
                        registro["apellido"],
                        registro["celular"],
                        registro["nivel"],
                        registro["correo"],
                        fecha_mysql,
                    ),
                )

            # Confirmar los cambios en la base de datos
            mysql.connection.commit()
            # Cerrar el cursor
            cursor.close()
            print("Datos importados exitosamente!")
            return True

    except Exception as e:
        # Capturar y mostrar cualquier error que ocurra durante el proceso
        print(f"Error: {str(e)}")
        return False


# Punto de entrada del script
if __name__ == "__main__":
    importar_datos_desde_json()  # Ejecutar la función de importación cuando se corre el script
