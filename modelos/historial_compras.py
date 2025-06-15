from conexion import get_connection

def obtener_historial_compras():
    conn = get_connection()
    historial = []
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT hc.id, p.nombre, pr.nombre, hc.precio, hc.fecha
            FROM historial_compras hc
            JOIN piezas p ON hc.pieza_id = p.id
            JOIN proveedores pr ON hc.proveedor_id = pr.id
            ORDER BY hc.fecha DESC
        """)
        for row in cur.fetchall():
            historial.append({
                "id": row[0],
                "pieza": row[1],
                "proveedor": row[2],
                "precio": float(row[3]),
                "fecha": row[4].strftime('%Y-%m-%d')
            })
        conn.close()
    return historial

def agregar_compra(pieza_id, proveedor_id, precio, fecha):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO historial_compras (pieza_id, proveedor_id, precio, fecha)
                VALUES (%s, %s, %s, %s)
            """, (pieza_id, proveedor_id, precio, fecha))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def eliminar_compra(compra_id):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM historial_compras WHERE id=%s", (compra_id,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"
