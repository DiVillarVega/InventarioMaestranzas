from conexion import get_connection

def obtener_detalle_orden(orden_id):
    conn = get_connection()
    detalles = []
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT d.pieza_id, p.nombre, d.cantidad, d.precio_unitario
            FROM ordenes_compra_detalle d
            JOIN piezas p ON d.pieza_id = p.id
            WHERE d.orden_id = %s
        """, (orden_id,))
        for row in cur.fetchall():
            detalles.append({
                "pieza_id": row[0],
                "pieza": row[1],
                "cantidad": row[2],
                "precio_unitario": float(row[3])
            })
        conn.close()
    return detalles

def agregar_item_orden(orden_id, pieza_id, cantidad, precio_unitario):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO ordenes_compra_detalle
                (orden_id, pieza_id, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
            """, (orden_id, pieza_id, cantidad, precio_unitario))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def eliminar_item_orden(orden_id, pieza_id):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                DELETE FROM ordenes_compra_detalle
                WHERE orden_id=%s AND pieza_id=%s
            """, (orden_id, pieza_id))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"
