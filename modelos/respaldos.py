from conexion import get_connection

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
