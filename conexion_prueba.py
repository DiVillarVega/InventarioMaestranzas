import psycopg2

try:
    conn = psycopg2.connect(
        dbname='MaestranzasDB',
        user='postgres',
        password='12345',
        host='localhost',
        port='5432'
    )
    print("¡Conexión exitosa!")
    conn.close()
except Exception as e:
    print("Error:", repr(e))
