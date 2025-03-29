import csv
import json
import os
import sys
from datetime import datetime


def formatear_encabezado(header):
    return header.strip().lower().replace(" ", "_")


def limpiar_valor(valor):
    """Elimina comillas simples y espacios alrededor del valor"""
    return valor.strip().strip("'") if valor else valor


def convertir_a_entero(valor):
    try:
        return int(valor) if valor else None
    except (ValueError, TypeError):
        return None


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
            # Configurar reader con quotechar para ignorar comillas simples
            reader = csv.DictReader(csvfile, delimiter=";", quotechar="'")

            # Formatear encabezados
            reader.fieldnames = [
                formatear_encabezado(header) for header in reader.fieldnames
            ]

            if not reader.fieldnames:
                raise ValueError("El archivo CSV está vacío o no tiene encabezados")

            data = []
            campos_numericos = ["cod_act", "id_tipificacion", "id_estado"]

            for row_num, row in enumerate(reader, 1):
                # Limpiar todos los valores y eliminar comillas
                cleaned_row = {key: limpiar_valor(value) for key, value in row.items()}

                # Convertir campos numéricos
                for campo in campos_numericos:
                    cleaned_row[campo] = convertir_a_entero(cleaned_row.get(campo))

                data.append(cleaned_row)

            json_file = f"Gestion_{datetime.now().strftime('%d-%m-%Y')}.json"

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
