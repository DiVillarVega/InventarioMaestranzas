# modelos/movimientos.py
from conexion import get_connection

def obtener_movimientos():
    conn = get_connection()
    movimientos = []
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT m.id, p.nombre, m.tipo, m.cantidad, m.fecha, t.nombre
            FROM movimientos m
            JOIN piezas p ON m.pieza_id = p.id
            JOIN trabajadores t ON m.usuario_id = t.id
            ORDER BY m.fecha DESC
        """)
        for row in cur.fetchall():
            movimientos.append({
                "id": row[0],
                "pieza": row[1],
                "tipo": row[2],
                "cantidad": row[3],
                "fecha": row[4].strftime('%Y-%m-%d %H:%M'),
                "usuario": row[5]
            })
        conn.close()
    return movimientos

def registrar_movimiento(pieza_id, tipo, cantidad, usuario_id, observacion=None):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO movimientos (pieza_id, tipo, cantidad, usuario_id, observacion)
            VALUES (%s, %s, %s, %s, %s)
        """, (pieza_id, tipo, cantidad, usuario_id, observacion))
        # Actualizar stock de la pieza
        if tipo == "entrada":
            cur.execute("UPDATE piezas SET stock_actual = stock_actual + %s WHERE id=%s", (cantidad, pieza_id))
        elif tipo == "salida":
            cur.execute("UPDATE piezas SET stock_actual = GREATEST(0, stock_actual - %s) WHERE id=%s", (cantidad, pieza_id))
        conn.commit()
        conn.close()

def obtener_piezas_id_nombre():
    conn = get_connection()
    piezas = []
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM piezas ORDER BY nombre")
        piezas = cur.fetchall()
        conn.close()
    return piezas

def obtener_stock_actual(pieza_id):
    conn = get_connection()
    stock = 0
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT stock_actual FROM piezas WHERE id=%s", (pieza_id,))
        r = cur.fetchone()
        if r:
            stock = r[0]
        conn.close()
    return stock
