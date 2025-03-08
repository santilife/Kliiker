from flask import Flask, render_template
import matplotlib

matplotlib.use("Agg")  # Fuerza el uso de un backend sin interfaz gráfica
import matplotlib.pyplot as plt
from database.config import db_conexion, mysql  # Importa la conexión desde config.py
from io import BytesIO
import base64

app = Flask(__name__)
db_conexion(app)  # Inicializa la conexión con MySQL


class GeneradorGraficas:
    def __init__(self, mysql):
        self.mysql = mysql

    def _ejecutar_consulta(self, query):
        """Ejecuta una consulta SQL y devuelve los resultados."""
        cursor = self.mysql.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            resultados = cursor.fetchall()
            print("🔹 Datos obtenidos en Flask:", resultados)  # Depuración
            return resultados
        except Exception as e:
            print(f"❌ Error al ejecutar la consulta: {str(e)}")
            return None
        finally:
            cursor.close()

    def grafico_estados(self):
        """Genera un gráfico de pastel con la distribución de estados."""
        try:
            query = """
                SELECT e.estado, COUNT(k.id_Kliiker) AS cantidad 
                FROM estadoKliiker e
                LEFT JOIN kliiker k ON e.id_estado = k.id_estado
                GROUP BY e.estado
            """
            datos = self._ejecutar_consulta(query)

            if not datos or len(datos) == 0:
                print("⚠️ No se obtuvieron datos de la base de datos.")
                return None

            labels = [item["estado"] for item in datos]
            sizes = [item["cantidad"] for item in datos]

            plt.figure(figsize=(8, 8))
            plt.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                wedgeprops=dict(width=0.3),
                startangle=90,
            )
            plt.title("Distribución de Estados")

            return self._guardar_grafico()
        except Exception as e:
            print(f"❌ Error en gráfico de estados: {str(e)}")
            return None

    def _guardar_grafico(self):
        """Convierte la imagen generada en un string base64 para ser enviada en una respuesta HTML."""
        buffer = BytesIO()
        plt.savefig(buffer, format="png", bbox_inches="tight")
        buffer.seek(0)
        imagen = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        return f"data:image/png;base64,{imagen}"


generador_graficas = GeneradorGraficas(mysql)


@app.route("/")
def index():
    """Ruta principal que renderiza la página con las gráficas."""
    grafico_estados = generador_graficas.grafico_estados()
    return render_template(
        "estadisticas/estadisticas.html", grafico_estados=grafico_estados
    )


if __name__ == "__main__":
    app.run(debug=True)
