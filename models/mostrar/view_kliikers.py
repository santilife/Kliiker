from flask import render_template, Blueprint, request, session
from flask_paginate import Pagination, get_page_parameter
from database.config import mysql

mostrar_tablas = Blueprint("mostrar_tablas", __name__)


def obtener_datos_gestion(search_query=None, page=1, per_page=10):
    try:
        cursor = mysql.connection.cursor()

        base_query = """
            SELECT
                g.id_gestion AS idGestion,
                k.id_Kliiker AS idKliiker,
                k.nombre,
                k.apellido,
                k.celular,
                k.nivel AS codigo,
                e.estado,
                g.canal,
                g.tipoGestion,
                g.fecha,
                g.comentario,
                u.nombre_AS AS asesor,
                t.tipificacion,
                g.motivoNoInteres,
                g.id_tipificacion
            FROM kliiker k
            LEFT JOIN gestiones g ON k.celular = g.celular
            LEFT JOIN usuarios u ON g.nombre_AS = u.nombre_AS
            LEFT JOIN tipificacion t ON g.id_tipificacion = t.id_tipificacion
            LEFT JOIN estadoKliiker e ON g.id_estado = e.id_estado
        """

        count_query = "SELECT COUNT(*) AS total FROM kliiker k LEFT JOIN gestiones g ON k.celular = g.celular"
        data_query = base_query + " ORDER BY k.nombre ASC LIMIT %s OFFSET %s"

        params = []
        where_clauses = []

        if search_query:
            where_clauses.append(
                "(k.nombre LIKE %s OR k.apellido LIKE %s OR k.celular LIKE %s OR k.id_Kliiker LIKE %s)"
            )
            params.extend([f"%{search_query}%"] * 4)
            count_query += " WHERE " + " AND ".join(where_clauses)
            data_query = (
                base_query
                + " WHERE "
                + " AND ".join(where_clauses)
                + " ORDER BY k.nombre ASC LIMIT %s OFFSET %s"
            )

        cursor.execute(count_query, params)
        total = int(cursor.fetchone()["total"])

        offset = (page - 1) * per_page
        cursor.execute(data_query, params + [per_page, offset])
        datos = cursor.fetchall()

        return {"datos": datos, "total": total, "page": page, "per_page": per_page}

    except Exception as err:
        print(f"Error en obtener_datos_gestion: {str(err)}")
        return {"datos": [], "total": 0}
    finally:
        cursor.close()


def obtener_datos_historial(search_query=None, page=1, per_page=10):
    try:
        cursor = mysql.connection.cursor()

        base_query = """
            SELECT 
                h.id_historial,
                h.id_gestion,
                h.id_llamada,
                h.fecha,
                h.canal,
                h.tipoGestion,
                h.comentario,
                h.fechaProximaGestion,
                h.nombre_AS AS asesor,
                h.id_tipificacion,
                h.celular,
                h.motivoNoInteres,
                k.id_Kliiker,
                k.nombre,
                k.apellido,
                k.nivel,
                t.tipificacion
            FROM historial_gestiones h
            LEFT JOIN kliiker k ON h.celular = k.celular
            LEFT JOIN tipificacion t ON h.id_tipificacion = t.id_tipificacion
        """

        count_query = "SELECT COUNT(*) AS total FROM historial_gestiones h"
        data_query = base_query + " ORDER BY h.id_historial DESC LIMIT %s OFFSET %s"

        params = []
        where_clauses = []

        if search_query:
            where_clauses.append(
                """
                (k.nombre LIKE %s OR 
                k.apellido LIKE %s OR 
                h.celular LIKE %s OR
                t.tipificacion LIKE %s OR
                h.canal LIKE %s OR
                h.comentario LIKE %s OR
                h.nombre_AS LIKE %s OR
                DATE_FORMAT(h.fecha, '%%Y-%%m-%%d') LIKE %s)
            """
            )

            count_query += """
                LEFT JOIN kliiker k ON h.celular = k.celular
                LEFT JOIN tipificacion t ON h.id_tipificacion = t.id_tipificacion
                WHERE """ + " OR ".join(
                where_clauses
            )

            data_query = (
                base_query
                + " WHERE "
                + " OR ".join(where_clauses)
                + " ORDER BY h.id_historial DESC LIMIT %s OFFSET %s"
            )

            params.extend([f"%{search_query}%"] * 8)

        cursor.execute(count_query, params)
        total = int(cursor.fetchone()["total"])

        offset = (page - 1) * per_page
        cursor.execute(data_query, params + [per_page, offset])
        datos = cursor.fetchall()

        return {"datos": datos, "total": total, "page": page, "per_page": per_page}

    except Exception as err:
        print(f"Error en obtener_datos_historial: {str(err)}")
        return {"datos": [], "total": 0}
    finally:
        cursor.close()


def total_gestiones():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT celular, COUNT(*) as total FROM historial_gestiones GROUP BY celular"
        )
        return {str(row["celular"]): row["total"] for row in cursor.fetchall()}
    except Exception as err:
        print(f"Error en total_gestiones: {str(err)}")
        return {}
    finally:
        cursor.close()


@mostrar_tablas.route("/mostrar_tablas")
def mostrar_tabla():
    search_query = request.args.get("q", "")
    active_tab = request.args.get("active_tab", "gestion")
    page_gestion = request.args.get("page_gestion", 1, type=int)
    page_historial = request.args.get("page_historial", 1, type=int)
    per_page = 10

    gestion_data = obtener_datos_gestion(search_query, page_gestion, per_page)
    historial_data = obtener_datos_historial(search_query, page_historial, per_page)

    paginacion_gestion = Pagination(
        page=page_gestion,
        per_page=per_page,
        total=gestion_data["total"],
        css_framework="bootstrap4",
        href=f"?q={search_query}&active_tab=gestion&page_gestion={{0}}",
        bs_version=4,
    )

    paginacion_historial = Pagination(
        page=page_historial,
        per_page=per_page,
        total=historial_data["total"],
        css_framework="bootstrap4",
        href=f"?q={search_query}&active_tab=historial&page_historial={{0}}",
        bs_version=4,
    )

    return render_template(
        "/formGestion/gestion.html",
        datos=gestion_data["datos"],
        datos_historial=historial_data["datos"],
        cantidad_gestiones=total_gestiones(),
        paginacion_gestion=paginacion_gestion,
        paginacion_historial=paginacion_historial,
        active_tab=active_tab,
        per_page=per_page,
    )
