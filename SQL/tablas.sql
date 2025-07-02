-- Tabla de trabajadores (usuarios internos)
CREATE TABLE trabajadores (
    id SERIAL PRIMARY KEY,
    correo TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, -- encriptada con bcrypt
    nombre TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN (
        'administrador', 
        'gestor_inventario', 
        'logistica', 
        'produccion', 
        'auditor'
    ))
);

-- Tabla de clientes (usuarios externos como compradores)
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    correo TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, -- encriptada con bcrypt
    nombre TEXT NOT NULL
);

-- Categorías de piezas
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

-- Etiquetas para clasificación personalizada
CREATE TABLE etiquetas (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);


-- Tabla de piezas (productos o componentes individuales)
CREATE TABLE piezas (
    id SERIAL PRIMARY KEY,
    codigo TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    stock_actual INT NOT NULL DEFAULT 0,
    ubicacion TEXT,
    categoria_id INT,
    etiqueta_id INT,
    precio NUMERIC(12,2) NOT NULL,
    CONSTRAINT fk_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    CONSTRAINT fk_etiqueta FOREIGN KEY (etiqueta_id) REFERENCES etiquetas(id)
);

-- Tabla de entradas y salidas
CREATE TABLE movimientos (
    id SERIAL PRIMARY KEY,
    pieza_id INT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'salida')),
    cantidad INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INT,
    observacion TEXT,
    CONSTRAINT fk_pieza FOREIGN KEY (pieza_id) REFERENCES piezas(id),
    CONSTRAINT fk_usuario FOREIGN KEY (usuario_id) REFERENCES trabajadores(id)
);

-- Tabla de lotes
CREATE TABLE lotes (
    id SERIAL PRIMARY KEY,
    pieza_id INT NOT NULL,
    codigo_lote TEXT NOT NULL,
    fecha_vencimiento DATE,
    cantidad INT NOT NULL,
    CONSTRAINT fk_pieza_lote FOREIGN KEY (pieza_id) REFERENCES piezas(id)
);

-- Tabla de kits (agrupación de piezas)
CREATE TABLE kits (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

-- Relación muchos a muchos entre kits y piezas
CREATE TABLE kits_piezas (
    kit_id INT NOT NULL,
    pieza_id INT NOT NULL,
    cantidad INT NOT NULL,
    PRIMARY KEY (kit_id, pieza_id),
    CONSTRAINT fk_kit FOREIGN KEY (kit_id) REFERENCES kits(id),
    CONSTRAINT fk_pieza_en_kit FOREIGN KEY (pieza_id) REFERENCES piezas(id)
);

-- Proveedores
CREATE TABLE proveedores (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    razon_social TEXT,
    rut TEXT,
    direccion TEXT,
    telefono TEXT,
    correo TEXT,
    productos TEXT,
    condiciones_pago TEXT
);

-- Historial de compras
CREATE TABLE historial_compras (
    id SERIAL PRIMARY KEY,
    pieza_id INT NOT NULL,
    proveedor_id INT,
    precio NUMERIC(12,2) NOT NULL,
    fecha DATE NOT NULL,
    CONSTRAINT fk_pieza_compra FOREIGN KEY (pieza_id) REFERENCES piezas(id),
    CONSTRAINT fk_proveedor_compra FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
);

-- Órdenes de compra (automatizadas o manuales)
CREATE TABLE ordenes_compra (
    id SERIAL PRIMARY KEY,
	cliente_id INT NULL,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    estado TEXT NOT NULL CHECK (estado IN ('pendiente', 'enviada', 'recibida', 'cancelada')),
    proveedor_id INT,
    creada_por INT,
    CONSTRAINT fk_proveedor_oc FOREIGN KEY (proveedor_id) REFERENCES proveedores(id),
    CONSTRAINT fk_creador_oc FOREIGN KEY (creada_por) REFERENCES trabajadores(id),
	CONSTRAINT fk_cliente_oc FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Detalle de orden de compra
CREATE TABLE ordenes_compra_detalle (
    orden_id INT,
    pieza_id INT,
    cantidad INT NOT NULL,
    precio_unitario NUMERIC(12,2),
    PRIMARY KEY (orden_id, pieza_id),
    CONSTRAINT fk_oc FOREIGN KEY (orden_id) REFERENCES ordenes_compra(id),
    CONSTRAINT fk_pieza_oc FOREIGN KEY (pieza_id) REFERENCES piezas(id)
);

-- Respaldos (registro de respaldos realizados)
CREATE TABLE respaldos (
    id SERIAL PRIMARY KEY,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    realizado_por INT,
    ruta_archivo TEXT,
    CONSTRAINT fk_respaldo_usuario FOREIGN KEY (realizado_por) REFERENCES trabajadores(id)
);

--Ubicaciones
CREATE TABLE ubicaciones (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);
