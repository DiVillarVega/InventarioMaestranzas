from conexion import get_connection

def obtener_kits():
    conn = get_connection()
    kits = []
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM kits ORDER BY id")
        for row in cur.fetchall():
            kits.append({"id": row[0], "nombre": row[1]})
        conn.close()
    return kits

def agregar_kit(nombre):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO kits (nombre) VALUES (%s)", (nombre,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def editar_kit(kit_id, nombre):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE kits SET nombre=%s WHERE id=%s", (nombre, kit_id))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def eliminar_kit(kit_id):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM kits WHERE id=%s", (kit_id,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def obtener_piezas_kit(kit_id):
    conn = get_connection()
    piezas = []
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT kp.pieza_id, p.nombre, kp.cantidad
            FROM kits_piezas kp
            JOIN piezas p ON kp.pieza_id = p.id
            WHERE kp.kit_id = %s
        """, (kit_id,))
        for row in cur.fetchall():
            piezas.append({"pieza_id": row[0], "nombre": row[1], "cantidad": row[2]})
        conn.close()
    return piezas

def agregar_pieza_a_kit(kit_id, pieza_id, cantidad):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO kits_piezas (kit_id, pieza_id, cantidad)
                VALUES (%s, %s, %s)
                ON CONFLICT (kit_id, pieza_id) DO UPDATE SET cantidad = EXCLUDED.cantidad
            """, (kit_id, pieza_id, cantidad))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def eliminar_pieza_de_kit(kit_id, pieza_id):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                DELETE FROM kits_piezas WHERE kit_id=%s AND pieza_id=%s
            """, (kit_id, pieza_id))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"
