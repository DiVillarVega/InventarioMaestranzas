from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QFrame,
    QLineEdit, QStackedWidget, QPushButton, QSizePolicy, QSpacerItem,
    QListWidgetItem, QDialog, QScrollArea, QDialogButtonBox
)
from PyQt6.QtCore import Qt, QSize, QRectF
from PyQt6.QtGui import QIcon, QColor, QFont, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer
from datetime import datetime, timedelta

import os

from conexion import get_connection
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


def get_white_svg_icon(svg_path, size=QSize(24, 24)):
    if not os.path.exists(svg_path):
        print(f"Advertencia: El archivo SVG no existe: {svg_path}")
        return QIcon()

    renderer = QSvgRenderer(svg_path)
    if not renderer.isValid():
        print(f"Advertencia: El archivo SVG no es válido: {svg_path}")
        return QIcon()

    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    renderer.render(painter, QRectF(0, 0, size.width(), size.height()))

    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), Qt.GlobalColor.white)

    painter.end()

    return QIcon(pixmap)
            
    
def get_black_svg_icon(svg_path, size=QSize(24, 24)):
    if not os.path.exists(svg_path):
        print(f"Advertencia: El archivo SVG no existe: {svg_path}")
        return QIcon()

    renderer = QSvgRenderer(svg_path)
    if not renderer.isValid():
        print(f"Advertencia: El archivo SVG no es válido: {svg_path}")
        return QIcon()

    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    renderer.render(painter, QRectF(0, 0, size.width(), size.height()))
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), Qt.GlobalColor.black)

    painter.end()

    return QIcon(pixmap)


class DashboardWindow(QWidget):
    def __init__(self, user_id, user_name, user_rol):
        super().__init__()
        self.setWindowTitle("Dashboard - Maestranzas Unidos S.A.")
        self.resize(1200, 1300) 
        self.user_id = user_id
        self.user_name = user_name
        self.user_rol = user_rol
        self.setup_ui()
        self.update_bell_icon()  # Actualizar icono campana al iniciar


    def setup_ui(self):
        def get_icon_path(icon_name):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_dir, 'icons', icon_name)

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

        # Botón de campana (notificaciones)
        self.bell_button = QPushButton()
        self.bell_button.setIconSize(QSize(24, 24))
        self.bell_button.setFlat(True)
        self.bell_button.clicked.connect(self.show_notifications)
        barra_layout.addWidget(self.bell_button)

        # Un solo QLineEdit para búsqueda
        self.busqueda = QLineEdit()
        self.busqueda.setPlaceholderText("Buscar...")
        self.busqueda.setFixedWidth(280)
        self.busqueda.setStyleSheet(
            f"background: white; color: black; border-radius: 7px; padding: 10px 16px; font-family: {FUENTE}; font-size: 16px;"
        )
        self.busqueda.textChanged.connect(self.buscar_en_modulo_actual)
        barra_layout.addWidget(self.busqueda)

        # -- Continúa igual el resto del código setup_ui --
        # (No hay cambios en lo que sigue)

        menu_lateral_widget = QWidget() 
        menu_lateral_layout = QVBoxLayout(menu_lateral_widget)
        menu_lateral_layout.setContentsMargins(0, 0, 0, 0) 
        menu_lateral_layout.setSpacing(0)
        menu_lateral_widget.setFixedWidth(240)
        menu_lateral_widget.setStyleSheet(f"background: #3D4B59; border-right: 2px solid #32384B;") 

        user_info_frame = QFrame()
        user_info_frame.setStyleSheet(f"background-color: #3D4B59;") 
        user_info_layout = QVBoxLayout(user_info_frame)
        user_info_layout.setContentsMargins(20, 20, 20, 10)
        user_info_layout.setSpacing(5)

        label_user_name = QLabel(self.user_name)
        label_user_name.setStyleSheet(f"font-size: 18px; font-weight: bold; font-family: {FUENTE}; color: #FFFFFF;") 
        user_info_layout.addWidget(label_user_name)

        label_user_rol = QLabel(self.user_rol.capitalize().replace("_", " "))
        label_user_rol.setStyleSheet(f"font-size: 14px; font-family: {FUENTE}; color: #FFFFFF;") 
        user_info_layout.addWidget(label_user_rol)
        
        user_info_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.btn_mi_perfil = QPushButton("Mi Perfil")
        self.btn_mi_perfil.setIcon(get_white_svg_icon(get_icon_path("account.svg"))) 
        self.btn_mi_perfil.setIconSize(QSize(20, 20))
        self.btn_mi_perfil.setStyleSheet(f"""
            QPushButton {{
                background-color: #3D4B59; 
                color: white; 
                font-family: {FUENTE};
                font-size: 15px;
                text-align: left;
                padding: 8px 6px; 
                border: none;
            }}
            QPushButton:hover {{
                background-color: #D0AF79; 
                color: white;
            }}
        """)
        user_info_layout.addWidget(self.btn_mi_perfil)

        self.btn_logout_menu_top = QPushButton("Cerrar sesión")
        self.btn_logout_menu_top.setIcon(get_white_svg_icon(get_icon_path("logout.svg"))) 
        self.btn_logout_menu_top.setIconSize(QSize(20, 20))
        self.btn_logout_menu_top.setStyleSheet(f"""
            QPushButton {{
                background-color: #3D4B59; 
                color: white; 
                font-family: {FUENTE};
                font-size: 15px;
                text-align: left;
                padding: 8px 6px; 
                border: none;
            }}
            QPushButton:hover {{
                background-color: #D0AF79; 
                color: white;
            }}
        """)
        self.btn_logout_menu_top.clicked.connect(self.logout)
        user_info_layout.addWidget(self.btn_logout_menu_top)
        
        user_info_layout.addSpacerItem(QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        menu_lateral_layout.addWidget(user_info_frame)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #32384B; margin: 10px 20px;") 
        menu_lateral_layout.addWidget(separator)

        menu_lateral_layout.addWidget(user_info_frame)

        titulo_inventario = QLabel("INVENTARIO")
        titulo_inventario.setFixedHeight(36)
        titulo_inventario.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        titulo_inventario.setStyleSheet(f"""
            background-color: #e5e4e9;
            color: #16202B;
            font-family: {FUENTE};
            font-size: 14px;
            font-weight: bold;
            padding-left: 20px;
            border-bottom: 1px solid #a0a0a0;
        """)
        menu_lateral_layout.addWidget(titulo_inventario)


        menu = QListWidget()
        menu.setContentsMargins(0, 0, 0, 0) 
        menu.setSpacing(0) 

        menu.setStyleSheet(f"""
            QListWidget {{
                background: #3D4B59; 
                border: none;
                font-family: {FUENTE};
                font-size: 16px;
                padding-top: 5px; 
                color: white; 
                outline: 0; 
            }}
            QListWidget::item {{
                height: 30px; 
                margin-bottom: 5px; 
                border-radius: 5px;
                padding-left: 20px;
                padding-right: 5px;
            }}
            QListWidget::item:selected {{
                background: #FAB647; 
                color: black; 
                font-weight: bold;
                border: none;
            }}
            QListWidget::item:hover {{
                background: #D0AF79; 
                color: white;
            }}
            QScrollBar:vertical {{
                border: none;
                background: transparent; 
                width: 0px; 
            }}
            QScrollBar::handle:vertical {{
                background: transparent;
                width: 0px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
                height: 0px;
                width: 0px;
            }}
        """)
        menu.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        menu.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        menu.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


        self.MENU_ITEM_ICON_PATH = get_icon_path("package.svg")
        self.DEFAULT_MENU_ITEM_ICON = get_white_svg_icon(self.MENU_ITEM_ICON_PATH)

        self.TITULOS = {
            "dashboard": "Inicio",
            "piezas": "Inventario General",
            "nueva_pieza": "Nueva Pieza",
            "movimientos": "Registrar movimientos",
            "lotes": "Gestión de Lotes",
            "etiquetas": "Etiquetas",
            "categorias": "Categorías",
            "usuarios": "Usuarios",
            "clientes": "Clientes",
            "proveedores": "Proveedores",
            "ubicaciones": "Ubicaciones",
            "ordenes_compra": "Órdenes de Compra",
            "kits": "Kits",
            "historial_compras": "Historial de Compras",
            "respaldos": "Respaldos",
        }

        self.opciones_menu_keys = [] 

        opciones_permitidas = ROLES_PANTALLAS.get(self.user_rol, [])

        secciones_y_modulos_filtrados = [
            ("INVENTARIO", ["piezas", "nueva_pieza", "movimientos", "lotes", "etiquetas", "categorias",
                             "ordenes_compra", "kits", "historial_compras", "ubicaciones",
                             "usuarios", "clientes", "proveedores", "respaldos"]),
        ]


        for seccion_titulo, modulos_en_seccion in secciones_y_modulos_filtrados:

            for op_key in modulos_en_seccion:
                if op_key in opciones_permitidas: 
                    titulo = self.TITULOS.get(op_key, op_key.capitalize())
                    item = QListWidgetItem(self.DEFAULT_MENU_ITEM_ICON, titulo) 
                    menu.addItem(item)
                    self.opciones_menu_keys.append(op_key) 
        


        menu.currentRowChanged.connect(self._handle_menu_selection)
        self.menu = menu

        menu_lateral_layout.addWidget(menu, stretch=1)


        self.stack = QStackedWidget()
        self.modulos = {}
        for op_key in self.opciones_menu_keys: 
            if op_key == "piezas":
                widget = PiezasWidget()
            elif op_key == "movimientos":
                widget = MovimientosWidget(user_id=self.user_id)
            elif op_key == "lotes":
                widget = LotesWidget()
            elif op_key == "usuarios":
                widget = UsuariosWidget()
            elif op_key == "clientes":
                widget = ClientesWidget()
            elif op_key == "proveedores":
                widget = ProveedoresWidget()
            elif op_key == "etiquetas":
                widget = EtiquetasWidget()
            elif op_key == "categorias":
                widget = CategoriasWidget()
            elif op_key == "ubicaciones":
                widget = UbicacionesWidget()
            elif op_key == "ordenes_compra":
                widget = OrdenesCompraWidget()
            elif op_key == "kits":
                widget = KitsWidget()
            elif op_key == "historial_compras":
                widget = HistorialComprasWidget()
            elif op_key == "respaldos":
                widget = RespaldosWidget(user_id=self.user_id)
            elif op_key == "nueva_pieza":
                widget = QLabel("Vista Nueva Pieza (en construcción)")
                widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                widget.setStyleSheet(f"color: white; font-size: 24px;")
            else:
                widget = QLabel(f"Vista {self.TITULOS.get(op_key, op_key.capitalize())} (en construcción)")
                widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                widget.setStyleSheet(f"color: white; font-size: 24px;")
            
            self.modulos[op_key] = widget
            self.stack.addWidget(widget)

        first_selectable_item_index = -1
        for i in range(self.menu.count()):
            if self.menu.item(i).flags() & Qt.ItemFlag.ItemIsSelectable:
                first_selectable_item_index = i
                break
        
        if first_selectable_item_index != -1:
            self.menu.setCurrentRow(first_selectable_item_index)
        else:
            self.stack.setCurrentIndex(-1)

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

        body_layout.addWidget(menu_lateral_widget)
        body_layout.addWidget(fondo)

        body_layout.setStretch(0, 1)
        body_layout.setStretch(1, 3)
        main_layout.addLayout(body_layout)

        self.setLayout(main_layout)

    def update_bell_icon(self):
        """
        Verifica si hay piezas con stock < 10 y actualiza el icono de la campana.
        """
        conn = get_connection()
        low_stock = []
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT nombre, stock_actual FROM piezas WHERE stock_actual < 10")
            low_stock = cur.fetchall()
            conn.close()

        # Cambiar icono segun existencia de notificaciones
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/icons/'
        icon_name = 'bell-badge.svg' if low_stock else 'bell.svg'
        icon = get_black_svg_icon(os.path.join(base_path, icon_name))
        self.bell_button.setIcon(icon)
        # Guardar datos para mostrar luego
        self.notifications = low_stock

    def show_notifications(self):
        bajos_stock = []
        proximos_vencimientos = []
        try:
            conn = get_connection()
            if conn:
                cur = conn.cursor()
                fecha_limite = datetime.now().date() + timedelta(days=10)
                # Consulta stock bajo
                cur.execute("SELECT nombre, stock_actual FROM piezas WHERE stock_actual < 10")
                bajos_stock = cur.fetchall()
                cur.execute("SELECT codigo_lote, fecha_vencimiento FROM lotes WHERE fecha_vencimiento <= %s", (fecha_limite,))
                proximos_vencimientos = cur.fetchall()
                conn.close()
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")

        dialog = QDialog(self)
        dialog.setWindowTitle("Notificaciones")
        layout = QVBoxLayout(dialog)

        if bajos_stock or proximos_vencimientos:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            content = QWidget()
            v = QVBoxLayout(content)
          
            for nombre, stock in bajos_stock:
                lbl = QLabel(f"Pieza '{nombre}' con stock bajo: {stock}")
                lbl.setWordWrap(True)
                v.addWidget(lbl)
            for nombre, fecha in proximos_vencimientos:
                lbl = QLabel(f"Pieza '{nombre}' próxima a vencer el: {fecha}")
                lbl.setWordWrap(True)
                v.addWidget(lbl)
            content.setLayout(v)
            scroll.setWidget(content)
            layout.addWidget(scroll)
        else:
            lbl = QLabel("No hay notificaciones")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)

        dialog.resize(300, 200)
        dialog.exec()


    def buscar_en_modulo_actual(self, texto):
        widget_actual = self.stack.currentWidget()
        if hasattr(widget_actual, "filtrar"):
            widget_actual.filtrar(texto)

    def _handle_menu_selection(self, current_row):
        selected_item = self.menu.item(current_row)

        if selected_item and not (selected_item.flags() & Qt.ItemFlag.ItemIsSelectable):
            current_index_in_stack = self.stack.currentIndex()
            if current_index_in_stack != -1:
                current_modulo_key = self.opciones_menu_keys[current_index_in_stack]
                for i in range(self.menu.count()):
                    item = self.menu.item(i)
                    if item.text() == self.TITULOS.get(current_modulo_key, current_modulo_key):
                        self.menu.setCurrentRow(i)
                        break
            return

        modulo_key = self.opciones_menu_keys[current_row]
        if modulo_key in self.modulos:
            widget = self.modulos[modulo_key]
            self.stack.setCurrentWidget(widget)
            self.busqueda.clear()
            self.setWindowTitle(f"{self.TITULOS.get(modulo_key)} - Maestranzas Unidos S.A.")
        else:
            print(f"No existe el módulo para la clave: {modulo_key}")

    def logout(self):
        from vistas.login import LoginWindow
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()


