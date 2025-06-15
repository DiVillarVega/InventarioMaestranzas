from conexion import get_connection

def obtener_etiquetas():
    conn = get_connection()
    etiquetas = []
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM etiquetas ORDER BY nombre")
        for row in cur.fetchall():
            etiquetas.append({"id": row[0], "nombre": row[1]})
        conn.close()
    return etiquetas

def agregar_etiqueta(nombre):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO etiquetas (nombre) VALUES (%s)", (nombre,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def editar_etiqueta(id_etiqueta, nombre):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE etiquetas SET nombre=%s WHERE id=%s", (nombre, id_etiqueta))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def eliminar_etiqueta(id_etiqueta):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM etiquetas WHERE id=%s", (id_etiqueta,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"
