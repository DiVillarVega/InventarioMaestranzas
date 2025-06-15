from conexion import get_connection

def obtener_ordenes():
    conn = get_connection()
    ordenes = []
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT o.id, c.nombre AS cliente, p.nombre AS proveedor, o.fecha_creacion, o.estado, t.nombre AS creado_por
            FROM ordenes_compra o
            LEFT JOIN clientes c ON o.cliente_id = c.id
            LEFT JOIN proveedores p ON o.proveedor_id = p.id
            LEFT JOIN trabajadores t ON o.creada_por = t.id
            ORDER BY o.fecha_creacion DESC
        """)
        for row in cur.fetchall():
            ordenes.append({
                "id": row[0],
                "cliente": row[1] or "-",
                "proveedor": row[2] or "-",
                "fecha": row[3].strftime('%Y-%m-%d'),
                "estado": row[4],
                "creado_por": row[5] or "-"
            })
        conn.close()
    return ordenes

def agregar_orden(cliente_id, proveedor_id, creada_por, estado='pendiente'):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO ordenes_compra (cliente_id, proveedor_id, creada_por, estado)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (cliente_id, proveedor_id, creada_por, estado))
            orden_id = cur.fetchone()[0]
            conn.commit()
            conn.close()
            return True, orden_id
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def editar_estado_orden(orden_id, estado):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE ordenes_compra SET estado=%s WHERE id=%s
            """, (estado, orden_id))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"

def eliminar_orden(orden_id):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM ordenes_compra WHERE id=%s", (orden_id,))
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"
