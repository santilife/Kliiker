import json
import csv
import sys
import os
from datetime import datetime


def convertir_fechas(item):
    """Convierte campos de fecha ISO a formato DD/MM/YYYY"""
    campos_fecha = ["fechaIngreso"]  # Agregar más campos si es necesario

    for campo in campos_fecha:
        if campo in item and item[campo]:
            try:
                # Eliminar componente horario si existe
                fecha_limpia = item[campo].split("T")[0]
                fecha_obj = datetime.strptime(fecha_limpia, "%Y-%m-%d")
                item[campo] = fecha_obj.strftime("%d/%m/%Y")
            except (ValueError, TypeError, AttributeError):
                pass  # Mantener valor original si hay error
    return item


def json_a_csv(archivo_json, archivo_csv):
    """Realiza la conversión JSON a CSV con formato correcto"""
    with open(archivo_json, "r", encoding="utf-8") as f:
        datos = json.load(f)

    # Aplicar conversión de fechas
    datos_convertidos = [convertir_fechas(item) for item in datos]

    # Crear directorio de destino
    os.makedirs(os.path.dirname(archivo_csv), exist_ok=True)

    # Escribir archivo CSV
    with open(archivo_csv, "w", encoding="utf-8", newline="") as f:
        if not datos_convertidos:
            raise ValueError("El archivo JSON está vacío")

        escritor = csv.DictWriter(f, fieldnames=datos_convertidos[0].keys())
        escritor.writeheader()
        escritor.writerows(datos_convertidos)


if __name__ == "__main__":
    # Validar argumentos
    if len(sys.argv) != 2:
        print("Uso: python script.py <archivo.json>")
        sys.exit(1)

    ruta_json = sys.argv[1]

    # Verificar existencia del archivo
    if not os.path.exists(ruta_json):
        print(f"Error: El archivo {ruta_json} no existe")
        sys.exit(1)

    # Generar rutas
    año_actual = datetime.now().year
    nombre_archivo = os.path.basename(ruta_json).replace(".json", ".csv")
    directorio_destino = f"Bases de datos ({año_actual})"
    ruta_csv = os.path.join(directorio_destino, nombre_archivo)

    try:
        json_a_csv(ruta_json, ruta_csv)
        print(f"Archivo generado exitosamente en:\n{ruta_csv}")

    except json.JSONDecodeError:
        print("Error: Archivo JSON corrupto o formato inválido")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
