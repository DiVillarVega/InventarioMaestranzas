from conexion import get_connection

def obtener_proveedores():
    conn = get_connection()
    proveedores = []
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nombre, razon_social, rut, direccion, telefono, correo, productos, condiciones_pago
            FROM proveedores
            ORDER BY id
        """)
        for row in cur.fetchall():
            proveedores.append({
                "id": row[0],
                "nombre": row[1],
                "razon_social": row[2],
                "rut": row[3],
                "direccion": row[4],
                "telefono": row[5],
                "correo": row[6],
                "productos": row[7],
                "condiciones_pago": row[8]
            })
        conn.close()
    return proveedores

def agregar_proveedor(nombre, razon_social, rut, direccion, telefono, correo, productos, condiciones_pago):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO proveedores
                (nombre, razon_social, rut, direccion, telefono, correo, productos, condiciones_pago)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre, razon_social, rut, direccion, telefono, correo, productos, condiciones_pago))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def editar_proveedor(id_proveedor, nombre, razon_social, rut, direccion, telefono, correo, productos, condiciones_pago):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE proveedores SET
                nombre=%s, razon_social=%s, rut=%s, direccion=%s, telefono=%s, correo=%s, productos=%s, condiciones_pago=%s
                WHERE id=%s
            """, (nombre, razon_social, rut, direccion, telefono, correo, productos, condiciones_pago, id_proveedor))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def eliminar_proveedor(id_proveedor):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM proveedores WHERE id=%s", (id_proveedor,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"
