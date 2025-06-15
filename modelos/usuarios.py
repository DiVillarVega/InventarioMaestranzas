from conexion import get_connection

def obtener_usuarios():
    conn = get_connection()
    usuarios = []
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT id, correo, nombre, rol FROM trabajadores ORDER BY id")
        for row in cur.fetchall():
            usuarios.append({
                "id": row[0],
                "correo": row[1],
                "nombre": row[2],
                "rol": row[3]
            })
        conn.close()
    return usuarios

def agregar_usuario(correo, password, nombre, rol):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO trabajadores (correo, password, nombre, rol)
                VALUES (%s, %s, %s, %s)
            """, (correo, password, nombre, rol))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def editar_usuario(id_usuario, correo, nombre, rol):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE trabajadores SET correo=%s, nombre=%s, rol=%s WHERE id=%s
            """, (correo, nombre, rol, id_usuario))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def cambiar_password(id_usuario, new_password):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE trabajadores SET password=%s WHERE id=%s
            """, (new_password, id_usuario))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def eliminar_usuario(id_usuario):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM trabajadores WHERE id=%s", (id_usuario,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"
