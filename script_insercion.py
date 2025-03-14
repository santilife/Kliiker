import json
import mysql.connector
import sys
from datetime import datetime
from typing import List, Dict

# Configuración de la base de datos
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "kliiker1",
}

# Mapeo de campos y validaciones
FIELD_MAPPING = {
    "nombres": ("nombre", str),
    "apellidos": ("apellido", str),
    "correo_electronico": ("correo", str),
    "celular": ("celular", str),
    "fecha_de_registro": (
        "fecha",
        lambda x: datetime.strptime(x, "%d/%m/%Y").date() if x else None,
    ),
    "codigo": ("nivel", int),
    "id_kliiker": ("id_Kliiker", str),
    "ventas": ("venta", int),
}

REQUIRED_FIELDS = ["celular", "nivel"]


def procesar_registro(registro: Dict) -> Dict:
    """Transforma y valida un registro individual"""
    processed = {}

    try:
        for json_key, (db_field, converter) in FIELD_MAPPING.items():
            raw_value = registro.get(json_key, "")
            processed[db_field] = converter(raw_value) if raw_value else None

        # Validar campos obligatorios
        if not all(processed.get(field) is not None for field in REQUIRED_FIELDS):
            return None

        # Asignar valores por defecto para campos opcionales
        processed.update(
            {
                "fechaIngreso": None,
                "diaSinGestion": None,
                "gestionable": None,
                "id_estado": None,
                "fechaSinGestion": None,
            }
        )

        return processed

    except (ValueError, TypeError, KeyError) as e:
        print(f"Error procesando registro: {e}")
        return None


def insertar_lotes(registros: List[Dict]):
    """Inserta registros en la base de datos en lotes"""
    if not registros:
        return

    query = """
    INSERT INTO kliiker (
        id_Kliiker, nombre, apellido, celular, nivel, correo,
        fecha, venta, fechaIngreso, diaSinGestion, gestionable,
        id_estado, fechaSinGestion
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Preparar datos
        datos = [
            (
                r["id_Kliiker"],
                r["nombre"],
                r["apellido"],
                r["celular"],
                r["nivel"],
                r["correo"],
                r["fecha"],
                r["venta"],
                r["fechaIngreso"],
                r["diaSinGestion"],
                r["gestionable"],
                r["id_estado"],
                r["fechaSinGestion"],
            )
            for r in registros
            if r is not None
        ]

        cursor.executemany(query, datos)
        conn.commit()
        return cursor.rowcount

    except mysql.connector.Error as e:
        print(f"Error de base de datos: {e}")
        conn.rollback()
        return 0
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def main(archivo_json: str):
    try:
        with open(archivo_json, "r") as f:
            datos = json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_json} no existe")
        return
    except json.JSONDecodeError:
        print(f"Error: El archivo {archivo_json} no es un JSON válido")
        return

    registros_procesados = [procesar_registro(r) for r in datos]
    registros_validos = [r for r in registros_procesados if r is not None]

    if not registros_validos:
        print("No hay registros válidos para insertar")
        return

    total_insertados = insertar_lotes(registros_validos)
    print(f"\nResumen:")
    print(f"- Registros procesados: {len(datos)}")
    print(f"- Registros válidos:    {len(registros_validos)}")
    print(f"- Registros insertados: {total_insertados}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script_insercion.py <archivo.json>")
        sys.exit(1)

    archivo = sys.argv[1]
    main(archivo)
