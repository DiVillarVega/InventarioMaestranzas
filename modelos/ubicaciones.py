from conexion import get_connection

def obtener_ubicaciones():
    conn = get_connection()
    ubicaciones = []
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM ubicaciones ORDER BY nombre")
        for row in cur.fetchall():
            ubicaciones.append({"id": row[0], "nombre": row[1]})
        conn.close()
    return ubicaciones

def agregar_ubicacion(nombre):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO ubicaciones (nombre) VALUES (%s)", (nombre,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def editar_ubicacion(id_ubicacion, nombre):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE ubicaciones SET nombre=%s WHERE id=%s", (nombre, id_ubicacion))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def eliminar_ubicacion(id_ubicacion):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM ubicaciones WHERE id=%s", (id_ubicacion,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"
