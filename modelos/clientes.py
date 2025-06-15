from conexion import get_connection

def obtener_clientes():
    conn = get_connection()
    clientes = []
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT id, correo, nombre FROM clientes ORDER BY id")
        for row in cur.fetchall():
            clientes.append({
                "id": row[0],
                "correo": row[1],
                "nombre": row[2]
            })
        conn.close()
    return clientes

def agregar_cliente(correo, password, nombre):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO clientes (correo, password, nombre)
                VALUES (%s, %s, %s)
            """, (correo, password, nombre))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def editar_cliente(id_cliente, correo, nombre):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE clientes SET correo=%s, nombre=%s WHERE id=%s
            """, (correo, nombre, id_cliente))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def cambiar_password(id_cliente, new_password):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE clientes SET password=%s WHERE id=%s
            """, (new_password, id_cliente))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def eliminar_cliente(id_cliente):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM clientes WHERE id=%s", (id_cliente,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"
