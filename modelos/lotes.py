from conexion import get_connection

def obtener_lotes():
    conn = get_connection()
    lotes = []
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT l.id, p.nombre, l.codigo_lote, l.fecha_vencimiento, l.cantidad
            FROM lotes l
            JOIN piezas p ON l.pieza_id = p.id
            ORDER BY l.fecha_vencimiento
        """)
        for row in cur.fetchall():
            lotes.append({
                "id": row[0],
                "pieza": row[1],
                "codigo": row[2],
                "vencimiento": row[3].strftime('%Y-%m-%d') if row[3] else "",
                "cantidad": row[4]
            })
        conn.close()
    return lotes

def agregar_lote(pieza_id, codigo_lote, fecha_vencimiento, cantidad):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO lotes (pieza_id, codigo_lote, fecha_vencimiento, cantidad)
            VALUES (%s, %s, %s, %s)
        """, (pieza_id, codigo_lote, fecha_vencimiento, cantidad))
        conn.commit()
        conn.close()

def editar_lote(lote_id, pieza_id, codigo_lote, fecha_vencimiento, cantidad):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE lotes
            SET pieza_id=%s, codigo_lote=%s, fecha_vencimiento=%s, cantidad=%s
            WHERE id=%s
        """, (pieza_id, codigo_lote, fecha_vencimiento, cantidad, lote_id))
        conn.commit()
        conn.close()

def eliminar_lote(lote_id):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM lotes WHERE id=%s", (lote_id,))
        conn.commit()
        conn.close()
