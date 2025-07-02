from conexion import get_connection
import json
from datetime import date, datetime

import json
from datetime import date, datetime
from decimal import Decimal
from conexion import get_connection

def generar_respaldo_json():
    conn = get_connection()
    if not conn:
        return None, "No se pudo conectar a la base de datos"

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE' AND table_name <> 'respaldos';
        """)
        tablas = [t[0] for t in cur.fetchall()]

        respaldo = {}
        for tabla in tablas:
            cur.execute(f"SELECT * FROM {tabla}")
            columnas = [desc[0] for desc in cur.description]
            filas = cur.fetchall()

            datos_tabla = []
            for fila in filas:
                fila_dict = {}
                for i, valor in enumerate(fila):
                    if isinstance(valor, (datetime, date)):
                        fila_dict[columnas[i]] = valor.isoformat()
                    elif isinstance(valor, Decimal):
                        fila_dict[columnas[i]] = float(valor)  # o str(valor) si prefieres
                    else:
                        fila_dict[columnas[i]] = valor
                datos_tabla.append(fila_dict)

            respaldo[tabla] = datos_tabla

        cur.close()
        conn.close()
        return respaldo, None

    except Exception as e:
        conn.close()
        return None, f"Error al generar respaldo: {str(e)}"



def obtener_respaldos():
    conn = get_connection()
    respaldos = []
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT r.id, r.fecha, t.nombre, r.ruta_archivo
            FROM respaldos r
            LEFT JOIN trabajadores t ON r.realizado_por = t.id
            ORDER BY r.fecha DESC
        """)
        for row in cur.fetchall():
            respaldos.append({
                "id": row[0],
                "fecha": row[1].strftime('%Y-%m-%d %H:%M'),
                "realizado_por": row[2] or "-",
                "ruta_archivo": row[3]
            })
        conn.close()
    return respaldos

def agregar_respaldo(realizado_por, ruta_archivo):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO respaldos (realizado_por, ruta_archivo)
                VALUES (%s, %s)
            """, (realizado_por, ruta_archivo))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def eliminar_respaldo(respaldo_id):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM respaldos WHERE id=%s", (respaldo_id,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"
