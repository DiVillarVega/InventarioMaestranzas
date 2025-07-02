# modelos/piezas.py
from conexion import get_connection

def obtener_todas_piezas():
    conn = get_connection()
    piezas = []
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT p.id, p.codigo, p.nombre, p.descripcion, p.stock_actual, p.ubicacion,
                       p.precio, c.nombre AS categoria, e.nombre AS etiqueta
                FROM piezas p
                LEFT JOIN categorias c ON p.categoria_id = c.id
                LEFT JOIN etiquetas e ON p.etiqueta_id = e.id
                ORDER BY p.id DESC
            """)
            rows = cur.fetchall()
            for row in rows:
                try:
                    piezas.append({
                        "id": row[0],
                        "codigo": row[1],
                        "nombre": row[2],
                        "descripcion": row[3],
                        "stock": row[4],
                        "ubicacion": row[5],
                        "precio": row[6],
                        "categoria": row[7],
                        "etiqueta": row[8]
                    })
                except UnicodeDecodeError as e:
                    print(f"Error al decodificar fila id={row[0]}: {e}")
        except Exception as e:
            print(f"Error ejecutando consulta: {e}")
        finally:
            conn.close()
    return piezas


def agregar_pieza(codigo, nombre, desc, stock, ubicacion, precio, categoria_id, etiqueta_id):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO piezas (codigo, nombre, descripcion, stock_actual, ubicacion, precio, categoria_id, etiqueta_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (codigo, nombre, desc, stock, ubicacion, precio, categoria_id, etiqueta_id)
            )
            conn.commit()
            conn.close()
            return True, ""
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)
    return False, "No se pudo conectar a la base de datos"


def editar_pieza(id, codigo, nombre, descripcion, stock, ubicacion, precio, categoria_id, etiqueta_id):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE piezas
            SET codigo = %s,
                nombre = %s,
                descripcion = %s,
                stock_actual = %s,
                ubicacion = %s,
                precio = %s,
                categoria_id = %s,
                etiqueta_id = %s
            WHERE id = %s
        """, (codigo, nombre, descripcion, stock, ubicacion, precio, categoria_id, etiqueta_id, id))
        conn.commit()
        conn.close()

def eliminar_pieza(id_pieza):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM piezas WHERE id=%s", (id_pieza,))
        conn.commit()
        conn.close()

        


