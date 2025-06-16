# modelos/piezas.py
from conexion import get_connection

def obtener_todas_piezas():
    conn = get_connection()
    piezas = []
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, codigo, nombre, descripcion, stock_actual, ubicacion
            FROM piezas
            ORDER BY id DESC
        """)
        for row in cur.fetchall():
            piezas.append({
                "id": row[0],
                "codigo": row[1],
                "nombre": row[2],
                "descripcion": row[3],
                "stock": row[4],
                "ubicacion": row[5],
            })
        conn.close()
    return piezas

def agregar_pieza(codigo, nombre, desc, stock, ubicacion):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO piezas (codigo, nombre, descripcion, stock_actual, ubicacion) VALUES (%s, %s, %s, %s, %s)",
                (codigo, nombre, desc, stock, ubicacion)
            )
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"


def editar_pieza(id_pieza, codigo, nombre, descripcion, stock, ubicacion):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE piezas
            SET codigo=%s, nombre=%s, descripcion=%s, stock_actual=%s, ubicacion=%s
            WHERE id=%s
        """, (codigo, nombre, descripcion, stock, ubicacion, id_pieza))
        conn.commit()
        conn.close()

def eliminar_pieza(id_pieza):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM piezas WHERE id=%s", (id_pieza,))
        conn.commit()
        conn.close()


