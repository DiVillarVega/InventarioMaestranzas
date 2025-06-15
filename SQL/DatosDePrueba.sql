-- LIMPIEZA Y REINICIO DE IDS (¡CUIDADO: Borra todos los datos!)
TRUNCATE TABLE 
    movimientos, 
    lotes, 
    kits_piezas, 
    piezas, 
    categorias, 
    etiquetas, 
    proveedores, 
    clientes, 
    trabajadores, 
    kits, 
    historial_compras, 
    ordenes_compra_detalle, 
    ordenes_compra, 
    respaldos,
	ubicaciones
RESTART IDENTITY CASCADE;

-- CATEGORÍAS (IDs: 1,2,3,4)
INSERT INTO categorias (nombre) VALUES
('Maquinaria'),      
('Electricidad'),    
('Ferretería'),      
('Automotriz');      

-- ETIQUETAS (IDs: 1,2,3,4)
INSERT INTO etiquetas (nombre) VALUES
('Importado'),       
('Nacional'),        
('Reparado'),        
('Nuevo');           

-- TRABAJADORES (IDs: 1..5)
INSERT INTO trabajadores (correo, password, nombre, rol) VALUES
('admin@maestranzas.cl', 'admin123', 'Admin Principal', 'administrador'),
('inventario@maestranzas.cl', 'inv123', 'Gestor Inventario', 'gestor_inventario'),
('logistica@maestranzas.cl', 'log123', 'Logística Uno', 'logistica'),
('prod@maestranzas.cl', 'prod123', 'Operario Producción', 'produccion'),
('auditor@maestranzas.cl', 'audit123', 'Auditor Uno', 'auditor');

-- CLIENTES (IDs: 1,2)
INSERT INTO clientes (correo, password, nombre) VALUES
('cliente1@ejemplo.com', 'cliente1', 'Cliente Uno'),
('cliente2@ejemplo.com', 'cliente2', 'Cliente Dos');

-- PROVEEDORES (IDs: 1,2)
INSERT INTO proveedores (nombre, razon_social, rut, direccion, telefono, correo, productos, condiciones_pago) VALUES
('Industrias Metal SA', 'Industrias Metalúrgicas SA', '76.123.456-7', 'Calle Falsa 123', '987654321', 'contacto@metal.com', 'Ruedas, Engranajes', '30 días'),
('Proveedor Eléctrico Ltda', 'Proveedor Eléctrico Ltda', '77.987.654-3', 'Av. Corrientes 456', '998877665', 'ventas@electric.com', 'Cables, Bombillas', 'Contado');

-- PIEZAS (IDs: 1..4)
INSERT INTO piezas (codigo, nombre, descripcion, stock_actual, ubicacion, categoria_id, etiqueta_id) VALUES
('PZ001', 'Rodamiento Z', 'Rodamiento alta carga', 50, 'Bodega 1, Estante A', 1, 1),
('PZ002', 'Cilindro hidráulico', 'Cilindro estándar', 20, 'Bodega 2, Estante B', 1, 2),
('PZ003', 'Bombilla LED', 'Bombilla de bajo consumo', 100, 'Bodega 3, Estante C', 2, 2),
('PZ004', 'Llave inglesa', 'Herramienta manual', 35, 'Bodega 1, Estante D', 3, 3);

-- LOTES (IDs: 1..3)
INSERT INTO lotes (pieza_id, codigo_lote, fecha_vencimiento, cantidad) VALUES
(1, 'LT001', '2026-07-09', 10),
(2, 'LT002', '2026-08-15', 5),
(3, 'LT003', '2027-01-30', 50);

-- KITS (IDs: 1,2)
INSERT INTO kits (nombre) VALUES
('Kit de Reparación A'),
('Kit de Electricidad');

-- KITS-PIEZAS
INSERT INTO kits_piezas (kit_id, pieza_id, cantidad) VALUES
(1, 1, 2),
(1, 4, 1),
(2, 3, 3);

-- HISTORIAL DE COMPRAS (IDs: 1,2)
INSERT INTO historial_compras (pieza_id, proveedor_id, precio, fecha) VALUES
(1, 1, 15000, '2024-05-01'),
(3, 2, 1200, '2024-06-10');

-- ÓRDENES DE COMPRA (IDs: 1,2)
INSERT INTO ordenes_compra (cliente_id, fecha_creacion, estado, proveedor_id, creada_por) VALUES
(1, '2024-06-01', 'pendiente', 1, 1),
(2, '2024-06-05', 'recibida', 2, 2);

-- DETALLE DE ÓRDENES DE COMPRA
INSERT INTO ordenes_compra_detalle (orden_id, pieza_id, cantidad, precio_unitario) VALUES
(1, 1, 5, 14000),
(1, 2, 2, 16000),
(2, 3, 10, 1100);

-- RESPALDOS
INSERT INTO respaldos (fecha, realizado_por, ruta_archivo) VALUES
(NOW(), 1, '/respaldos/backup_junio.sql'),
(NOW(), 2, '/respaldos/backup_julio.sql');

-- MOVIMIENTOS DE INVENTARIO (IDs: 1..5)
INSERT INTO movimientos (pieza_id, tipo, cantidad, usuario_id, observacion) VALUES
(1, 'entrada', 10, 1, 'Ingreso por compra'),
(1, 'salida', 3, 2, 'Entrega a producción'),
(2, 'entrada', 5, 2, 'Compra repuesto'),
(3, 'entrada', 30, 3, 'Llegada importación'),
(3, 'salida', 5, 4, 'Uso en mantención');

-- UBICACIONES
INSERT INTO ubicaciones (nombre) VALUES
('Bodega 1, Estante A'),
('Bodega 2, Estante B'),
('Bodega 3, Estante C'),
('Depósito Central'),
('Estante D, Zona Sur');
