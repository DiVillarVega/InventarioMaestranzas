from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from estilos import COLOR_CARD, FUENTE

class CardWidget(QWidget):
    def __init__(self, icono, titulo, valor):
        super().__init__()
        self.setFixedSize(200, 110)
        self.setStyleSheet(f"""
            background: {COLOR_CARD};
            border-radius: 18px;
            font-family: {FUENTE};
            color: white;
        """)
        layout = QVBoxLayout()
        label_icono = QLabel(icono)
        label_icono.setStyleSheet("font-size: 28px;")
        layout.addWidget(label_icono)
        label_titulo = QLabel(titulo)
        label_titulo.setStyleSheet("font-size: 15px; font-weight: bold;")
        layout.addWidget(label_titulo)
        label_valor = QLabel(str(valor))
        label_valor.setStyleSheet("font-size: 32px; font-weight: bold; margin-top: 5px;")
        layout.addWidget(label_valor)
        layout.addStretch()
        self.setLayout(layout)
