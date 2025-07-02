import psycopg2
from config import DB_CONFIG

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_CONFIG['NAME'],
            user=DB_CONFIG['USER'],
            password=DB_CONFIG['PASSWORD'],
            host=DB_CONFIG['HOST'],
            port=DB_CONFIG['PORT']
        )
        # Forzar encoding a UTF8 (importante para evitar errores de decoding)
        conn.set_client_encoding('UTF8')
        return conn
    except Exception as e:
        print(f"[ERROR] No se pudo conectar a la base de datos: {e}")
        return None
