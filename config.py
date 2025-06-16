# config.py

DB_CONFIG = {
    'NAME': 'MaestranzasDB',      # <-- Nombre BD
    'USER': 'postgres',          # <-- Usuario
    'PASSWORD': '12345',      # <-- Password
    'HOST': 'localhost',
    'PORT': '5432'
}

RECURSOS_PATH = "recursos/"

# Diccionario para mapear roles a pantallas
ROLES_PANTALLAS = {
    'administrador': [
        'dashboard',
        'piezas',
        'movimientos',
        'lotes',
        'usuarios',
        'clientes',
        'proveedores',
        'etiquetas',
        'categorias',
        'ubicaciones',
        'ordenes_compra',
        'kits',
        'historial_compras',
        'respaldos',
    ],
    # HAY QUE EDITAR ESTO PARA QUE CADA ROL TENGA SUS PROPIAS PANTALLAS
    'gestor_inventario':['dashboard', 'piezas', 'movimientos', 'lotes'],
    'logistica':        ['dashboard', 'movimientos', 'lotes'],
    'produccion':       ['dashboard', 'piezas'],
    'auditor':          ['dashboard', 'movimientos'],
}

AUTOLOGIN = True # Cambia a False si no quieres autologin
AUTOLOGIN_USER = {
    "correo": "admin@maestranzas.cl",
    "password": "admin123"
}
