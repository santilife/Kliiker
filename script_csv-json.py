import csv
import json
import random
import os
import sys


def generar_numero_unico():
    while True:
        numero = random.randint(1000, 999999)
        if not os.path.exists(f"{numero}.json"):
            return numero


def formatear_encabezado(header):
    return header.strip().lower().replace(" ", "_")


def main():
    if len(sys.argv) < 2:
        print("Error: Debes especificar el archivo CSV como parámetro")
        print("Ejemplo: python app.py Base.csv")
        sys.exit(1)

    csv_file = sys.argv[1]

    try:
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"Archivo '{csv_file}' no encontrado")

        with open(csv_file, "r", encoding="latin-1") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")

            # Convertir encabezados a formato snake_case
            reader.fieldnames = [
                formatear_encabezado(header) for header in reader.fieldnames
            ]

            if not reader.fieldnames:
                raise ValueError("El archivo CSV está vacío o no tiene encabezados")

            data = []
            for row in reader:
                # Crear nuevo diccionario con claves formateadas
                formatted_row = {key: value.strip() for key, value in row.items()}
                data.append(formatted_row)

            numero = generar_numero_unico()
            json_file = f"{numero}.json"

            with open(json_file, "w", encoding="utf-8") as jsonfile:
                json.dump(data, jsonfile, indent=4, ensure_ascii=False)

            print(f"\n✅ Conversión exitosa!")
            print(f"CSV original: {csv_file}")
            print(f"JSON generado: {json_file}")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
