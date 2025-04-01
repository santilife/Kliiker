import csv
import json
import os
import sys
from datetime import datetime
import traceback


def formatear_encabezado(header):
    return (
        header.strip()
        .lower()
        .replace(" ", "_")
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
    )


def limpiar_valor(valor):
    return valor.strip().strip("'\"") if valor else valor


def limpiar_celular(valor):
    """Limpia números de celular: remueve espacios, guiones y prefijos"""
    return "".join(filter(str.isdigit, str(valor))).lstrip("0") if valor else ""


def main():
    try:
        upload_dir = "temp_uploads"
        timestamp = datetime.now().strftime("%Y%m%d")
        csv_filename = f"upload_{timestamp}.csv"
        csv_file = os.path.join(upload_dir, csv_filename)

        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"Archivo requerido no encontrado: {csv_filename}")

        with open(csv_file, "r", encoding="latin-1") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar="'")
            original_headers = next(reader)
            formatted_headers = [formatear_encabezado(h) for h in original_headers]

            data = []
            for row in reader:
                cleaned_row = {
                    formatted_headers[i]: limpiar_valor(value)
                    for i, value in enumerate(row)
                }

                # Limpieza especial para celular
                if "celular" in cleaned_row:
                    cleaned_row["celular"] = limpiar_celular(cleaned_row["celular"])

                data.append(cleaned_row)

            json_filename = f"Kliiker_{timestamp}.json"
            json_file = os.path.join(upload_dir, json_filename)

            with open(json_file, "w", encoding="utf-8") as jsonfile:
                json.dump(data, jsonfile, indent=4, ensure_ascii=False)

            print("\n[EXITO] Conversion exitosa!")
            print(f"Registros procesados: {len(data)}")
            print(f"Ruta del JSON: {os.path.abspath(json_file)}")

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        print("Detalle del error:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    if not os.path.exists("temp_uploads"):
        os.makedirs("temp_uploads")

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    main()
