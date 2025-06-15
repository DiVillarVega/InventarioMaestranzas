# Manual de Estructura de Código y Arquitectura

## Software Maestranzas Unidos S.A.

---

## Índice

1. [Visión General](#vision-general)
2. [Estructura de Carpetas y Archivos](#estructura-de-carpetas)
3. [Principales Componentes](#componentes-principales)
   - [1. Arranque y Login](#arranque-y-login)
   - [2. Dashboard](#dashboard)
   - [3. Vistas de Módulos](#vistas-de-modulos)
   - [4. Modelos de Base de Datos](#modelos-de-bd)
   - [5. Estilos y Colores](#estilos-y-colores)
   - [6. Widgets Personalizados](#widgets-personalizados)
4. [Manejo de Roles y Permisos](#roles-y-permisos)
5. [Navegación y Flujo General](#flujo-general)
6. [Manejo de Base de Datos y Conexiones](#conexion-bd)
7. [Buenas Prácticas y Extensibilidad](#buenas-practicas)
8. [Resumen y Sugerencias de Edición](#resumen-y-sugerencias)

---

## 1. **Visión General**

El sistema está estructurado siguiendo una arquitectura modular tipo **MVC simplificado** para aplicaciones de escritorio en PyQt6:

- **Vistas**: Componentes gráficos y pantallas (dashboard, forms, tablas, etc.).
- **Modelos**: Funciones de acceso y manipulación de la base de datos PostgreSQL.
- **Control**: Lógica de navegación y activación de vistas según roles y eventos.

Cada módulo (Inventario, Movimientos, Lotes, etc.) es **autónomo y reutilizable**, facilitando la edición, el testing y el crecimiento del sistema.

---

## 2. **Estructura de Carpetas y Archivos**

```
/ProyectoRaiz/
│
├── main.py
├── config.py
├── estilos.py
├── conexion.py
│
├── modelos/
│   ├── piezas.py
│   ├── movimientos.py
│   ├── lotes.py
│   ├── usuarios.py
│   ├── clientes.py
│   ├── proveedores.py
│   ├── etiquetas.py
│   ├── categorias.py
│   ├── ubicaciones.py
│   ├── ordenes_compra.py
│   ├── historial_compras.py
│   ├── kits.py
│   └── respaldos.py
│
├── vistas/
│   ├── dashboard.py
│   ├── login.py
│   ├── piezas.py
│   ├── movimientos.py
│   ├── lotes.py
│   ├── usuarios.py
│   ├── clientes.py
│   ├── proveedores.py
│   ├── etiquetas.py
│   ├── categorias.py
│   ├── ubicaciones.py
│   ├── ordenes_compra.py
│   ├── historial_compras.py
│   ├── kits.py
│   ├── respaldos.py
│   ├── tabla_estilizada.py
│   └── cards.py (opcional para widgets visuales tipo dashboard)
│
├── requirements.txt
├── db.sql
└── README.md
```

---

## 3. **Principales Componentes**

### **1. Arranque y Login**

- El punto de entrada es `main.py`.
- Muestra la ventana de login (`vistas/login.py`).
- Si el usuario y contraseña son válidos, abre el **dashboard** pasando el id, nombre y rol del usuario logueado.

### **2. Dashboard**

- El archivo central de navegación es `vistas/dashboard.py`.
- Muestra:
  - **Barra superior:** Amarilla, logo y búsqueda.
  - **Menú lateral:** Opciones dinámicas según el rol (provenientes de `config.py`).
  - **Área central:** Espacio donde se cargan los módulos activos como “pestañas” usando un `QStackedWidget`.

### **3. Vistas de Módulos**

- Cada archivo de `vistas/` representa un módulo funcional (por ejemplo, `piezas.py` para el inventario).
- Cada vista contiene:
  - **Widgets de formulario** (alta/edición/baja).
  - **Tablas** (usando siempre `TablaEstilizada` para look uniforme).
  - **Botones** y lógica de interacción local.
  - **Importa el modelo respectivo** de la carpeta `/modelos/` para acceder a la base de datos.
- Se recomienda una sola clase principal por módulo (ejemplo: `class PiezasWidget(QWidget): ...`).

### **4. Modelos de Base de Datos**

- Cada archivo en `/modelos/` agrupa las funciones CRUD para una entidad.
- Ejemplo: `modelos/piezas.py` tiene funciones como `obtener_todas_piezas`, `agregar_pieza`, etc.
- **No contienen lógica visual, solo lógica de datos.**
- Todas las conexiones a la base pasan por el helper `get_connection()` de `conexion.py`.

### **5. Estilos y Colores**

- El archivo `estilos.py` centraliza la paleta de colores y fuentes.
- Cambia aquí los colores para afectarlos globalmente.
- Los widgets y layouts usan estas constantes para una apariencia uniforme.

### **6. Widgets Personalizados**

- **TablaEstilizada:**\
  En `vistas/tabla_estilizada.py`. Hereda de `QTableWidget` y aplica un style sheet para todas las tablas, fondo blanco y headers amarillos.
- **CardWidget:**\
  En `vistas/cards.py`. Para mostrar cards visuales en dashboard con datos resumidos.

---

## 4. **Manejo de Roles y Permisos**

- Los roles y los permisos de menú se definen en `config.py` usando el diccionario `ROLES_PANTALLAS`.
- Cada rol tiene una lista de módulos que puede ver y navegar desde el dashboard.
- El menú lateral se genera dinámicamente según el rol del usuario.

---

## 5. **Navegación y Flujo General**

1. **Login:**

   - El usuario se autentica.
   - El sistema recupera datos de usuario y su rol.

2. **Dashboard:**

   - Se carga el menú según el rol.
   - El usuario puede navegar entre módulos.
   - Cada módulo es autónomo y se carga en el área central.

3. **Módulos funcionales:**

   - Pueden ser formularios (alta, edición, eliminación) y tablas.
   - Usan los modelos para manipular datos reales en la BD.
   - Se comunican con la base solo a través de los modelos.

---

## 6. **Manejo de Base de Datos y Conexiones**

- El archivo `conexion.py` contiene la función `get_connection()` que usa la configuración de `config.py` para conectarse a PostgreSQL.
- **Todas las operaciones de base** en los modelos abren la conexión, ejecutan la consulta y la cierran inmediatamente.
- Los errores de conexión y de SQL se manejan mostrando mensajes amigables en la interfaz.

---

## 7. **Buenas Prácticas y Extensibilidad**

- **Modularidad:** Cada funcionalidad es un archivo/carpeta separado.
- **Estilo unificado:** Usando `estilos.py` y widgets personalizados.
- **Fácil de escalar:** Para agregar un nuevo módulo solo creas:
  1. Un modelo en `/modelos/`.
  2. Una vista en `/vistas/`.
  3. Lo agregas en el dashboard y en el diccionario de roles.
- **Reutilización:**
  - Todas las tablas usan la misma clase estilizada.
  - Todos los colores y fuentes están centralizados.
- **Separación:**
  - Ningún modelo tiene lógica visual ni widgets.
  - Las vistas no contienen SQL directo, solo llaman a funciones del modelo.

---

## 8. **Resumen y Sugerencias de Edición**

- **Para modificar el menú o los permisos:**\
  Edita `ROLES_PANTALLAS` en `config.py`.

- **Para cambiar la paleta de colores:**\
  Edita los valores de `estilos.py`.

- **Para agregar un nuevo módulo:**

  - Crea el modelo y la vista, sigue el patrón actual.
  - Añade el import y el `if` respectivo en `dashboard.py`.
  - Añade la opción en `ROLES_PANTALLAS` para los roles que deban verla.

- **Para cambiar cómo se conecta la base de datos:**\
  Modifica solo `conexion.py` y/o los parámetros en `config.py`.

- **Para modificar la estética de todas las tablas:**\
  Edita solo el style sheet en `tabla_estilizada.py`.

---

## **Conclusión**

La estructura está pensada para que cualquier programador con conocimientos básicos de Python y PyQt pueda:

- **Agregar, editar o quitar módulos** fácilmente,
- **Actualizar la estética** de forma global,
- **Adaptar la base de datos** cambiando una sola función,
- **Entender el flujo del usuario** desde login a dashboard y a cada módulo.

Cada archivo es **independiente** y **autodocumentado** gracias a los nombres claros y la separación lógica.

