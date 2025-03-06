from flask import Flask
import matplotlib.pyplot as plt
from database.config import db_conexion, mysql  # Importa la conexión desde config.py

app = Flask(__name__)
db_conexion(app)  # Llama a la función de configuración para inicializar MySQL


def obtener_datos():
    """
    Obtiene los datos de Estado y Tipificación desde la base de datos.
    """
    conexion = mysql.connection
    cursor = conexion.cursor()

    # 🔹 Obtener datos de Estados
    cursor.execute(
        """
        SELECT estado, COUNT(*) 
        FROM kliiker 
        INNER JOIN estado ON kliker.id_estado = estado.id_estado 
        GROUP BY estado
    """
    )
    datos_estados = cursor.fetchall()

    # 🔹 Obtener datos de Tipificación
    cursor.execute(
        """
        SELECT tipificacion, COUNT(*) 
        FROM gestiones 
        GROUP BY tipificacion
    """
    )
    datos_tipificacion = cursor.fetchall()

    cursor.close()
    return datos_estados, datos_tipificacion


def graficar():
    """
    Genera las gráficas de Estados (dona) y Tipificación (barras horizontales).
    """
    datos_estados, datos_tipificacion = obtener_datos()

    # 🔹 Procesar datos para la gráfica de dona
    labels_estados = [fila[0] for fila in datos_estados]
    valores_estados = [fila[1] for fila in datos_estados]

    # 🔹 Crear el diagrama de dona
    plt.figure(figsize=(6, 6))
    plt.pie(
        valores_estados,
        labels=labels_estados,
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops={"edgecolor": "white"},
    )
    plt.gca().add_artist(
        plt.Circle((0, 0), 0.6, color="white")
    )  # Agregar efecto de dona
    plt.title("Distribución de Estados")
    plt.show()

    # 🔹 Procesar datos para la gráfica de barras
    labels_tipificacion = [fila[0] for fila in datos_tipificacion]
    valores_tipificacion = [fila[1] for fila in datos_tipificacion]

    # 🔹 Crear la gráfica de barras horizontal
    plt.figure(figsize=(8, 5))
    plt.barh(labels_tipificacion, valores_tipificacion, color=["blue", "red", "green"])
    plt.xlabel("Cantidad de Gestiones")
    plt.ylabel("Tipificación")
    plt.title("Cantidad de Gestiones por Tipificación")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.show()


if __name__ == "__main__":
    with app.app_context():
        graficar()
