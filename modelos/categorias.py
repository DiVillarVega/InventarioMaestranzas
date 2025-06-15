from conexion import get_connection

def obtener_categorias():
    conn = get_connection()
    categorias = []
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
        for row in cur.fetchall():
            categorias.append({"id": row[0], "nombre": row[1]})
        conn.close()
    return categorias

def agregar_categoria(nombre):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def editar_categoria(id_categoria, nombre):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE categorias SET nombre=%s WHERE id=%s", (nombre, id_categoria))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def eliminar_categoria(id_categoria):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM categorias WHERE id=%s", (id_categoria,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"
