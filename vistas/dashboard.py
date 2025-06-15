from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QFrame, QLineEdit, QStackedWidget
)
from PyQt6.QtCore import Qt
from estilos import COLOR_BARRA, COLOR_FONDO, COLOR_MENU, FUENTE
from config import ROLES_PANTALLAS
from vistas.piezas import PiezasWidget
from vistas.movimientos import MovimientosWidget
from vistas.lotes import LotesWidget
from vistas.usuarios import UsuariosWidget
from vistas.clientes import ClientesWidget
from vistas.proveedores import ProveedoresWidget
from vistas.etiquetas import EtiquetasWidget
from vistas.categorias import CategoriasWidget
from vistas.ubicaciones import UbicacionesWidget
from vistas.ordenes_compra import OrdenesCompraWidget
from vistas.kits import KitsWidget
from vistas.historial_compras import HistorialComprasWidget
from vistas.respaldos import RespaldosWidget

class DashboardWindow(QWidget):
    def __init__(self, user_id, user_name, user_rol):
        super().__init__()
        self.setWindowTitle("Dashboard - Maestranzas Unidos S.A.")
        self.resize(1200, 800)
        self.user_id = user_id
        self.user_name = user_name
        self.user_rol = user_rol
        self.setup_ui()

    def setup_ui(self):
        # Barra superior (amarilla)
        barra = QFrame()
        barra.setFixedHeight(64)
        barra.setStyleSheet(f"background-color: {COLOR_BARRA};")
        barra_layout = QHBoxLayout(barra)
        barra_layout.setContentsMargins(32, 0, 32, 0)
        barra_layout.setSpacing(15)

        label_logo = QLabel("🛠️  MAESTRANZAS UNIDOS S.A.")
        label_logo.setStyleSheet(f"font-size: 23px; font-weight: bold; font-family: {FUENTE}; color: #16202B;")
        barra_layout.addWidget(label_logo)
        barra_layout.addStretch()
        busqueda = QLineEdit()
        busqueda.setPlaceholderText("Buscar...")
        busqueda.setFixedWidth(280)
        busqueda.setStyleSheet(
            f"background: white; border-radius: 7px; padding: 10px 16px; font-family: {FUENTE}; font-size: 16px;"
        )
        barra_layout.addWidget(busqueda)

        # Menú lateral (gris claro)
        menu = QListWidget()
        menu.setFixedWidth(220)
        menu.setStyleSheet(f"""
            QListWidget {{
                background: {COLOR_MENU};
                border: none;
                font-family: {FUENTE};
                font-size: 17px;
                padding-top: 26px;
            }}
            QListWidget::item {{
                height: 46px;
                margin-bottom: 7px;
                border-radius: 9px;
                padding-left: 16px;
            }}
            QListWidget::item:selected {{
                background: white;
                color: #2152FF;
                font-weight: bold;
                border: 2px solid #2152FF;
            }}
        """)

        # Opciones de menú según rol
        opciones = ROLES_PANTALLAS.get(self.user_rol, [])
        # Mapea a nombres legibles
        TITULOS = {
            "dashboard": "Inicio",
            "piezas": "Inventario",
            "movimientos": "Movimientos",
            "lotes": "Lotes",
            "usuarios": "Usuarios",
            "clientes": "Clientes",
            "proveedores": "Proveedores",
            "etiquetas": "Etiquetas",
            "categorias": "Categorías",
            "ubicaciones": "Ubicaciones",
            "ordenes_compra": "Órdenes de Compra",
            "kits": "Kits",
            "historial_compras": "Historial de Compras",
            "respaldos": "Respaldos",
        }
        self.opciones = opciones
        menu.addItems([TITULOS.get(op, op.capitalize()) for op in opciones])
        menu.currentRowChanged.connect(self.cambiar_modulo)
        self.menu = menu  # para referencia en otros métodos

        # Área principal (stack)
        self.stack = QStackedWidget()
        self.modulos = {}
        for op in opciones:
            if op == "piezas":
                widget = PiezasWidget()
            elif op == "movimientos":
                widget = MovimientosWidget(user_id=self.user_id)
            elif op == "lotes":
                widget = LotesWidget()
            elif op == "usuarios":
                widget = UsuariosWidget()
            elif op == "clientes":
                widget = ClientesWidget()
            elif op == "proveedores":
                widget = ProveedoresWidget()
            elif op == "etiquetas":
                widget = EtiquetasWidget()
            elif op == "categorias":
                widget = CategoriasWidget()
            elif op == "ubicaciones":
                widget = UbicacionesWidget()
            elif op == "ordenes_compra":
                widget = OrdenesCompraWidget()
            elif op == "kits":
                widget = KitsWidget()
            elif op == "historial_compras":
                widget = HistorialComprasWidget()
            elif op == "respaldos":
                widget = RespaldosWidget(user_id=self.user_id)
            else:
                widget = QLabel(f"Vista {TITULOS.get(op, op.capitalize())} (en construcción)")
                widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                widget.setStyleSheet(f"color: white; font-size: 24px;")
            self.modulos[op] = widget
            self.stack.addWidget(widget)
        self.menu.setCurrentRow(0)

        # Layout principal con fondo azul oscuro
        fondo = QFrame()
        fondo.setStyleSheet(f"background: {COLOR_FONDO}; border: none;")
        fondo_layout = QVBoxLayout(fondo)
        fondo_layout.setContentsMargins(20, 20, 20, 20)
        fondo_layout.addWidget(self.stack)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(barra)
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        # Menú lateral en marco decorativo
        menu_frame = QFrame()
        menu_layout = QVBoxLayout(menu_frame)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)
        # Opcional: añade perfil, avatar o datos usuario aquí arriba del menú si tu mockup lo tiene
        menu_layout.addWidget(menu)
        menu_layout.addStretch()
        menu_frame.setStyleSheet(f"background: {COLOR_MENU}; border-right: 2px solid #e0e0e0;")
        body_layout.addWidget(menu_frame)
        body_layout.addWidget(fondo)
        body_layout.setStretch(0, 1)  # Menú lateral: 1 parte
        body_layout.setStretch(1, 3)  # Contenido: 3 partes
        main_layout.addLayout(body_layout)

        self.setLayout(main_layout)

    def cambiar_modulo(self, idx):
        self.stack.setCurrentIndex(idx)
