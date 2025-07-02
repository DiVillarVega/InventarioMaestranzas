from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QComboBox, QSpinBox, QDoubleSpinBox, QMessageBox
)
from modelos.ordenes_compra_detalle import obtener_detalle_orden, agregar_item_orden, eliminar_item_orden
from modelos.piezas import obtener_todas_piezas
from estilos import estilo_titulo, estilo_boton_general

class DetalleOrdenDialog(QDialog):
    def __init__(self, orden_id, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #16202b;
                color: white;
                font-family: Segoe UI;
            }
            QLabel {
                color: white;
            }
            QLineEdit, QComboBox, QTextEdit, QSpinBox, QDoubleSpinBox {
                background-color: #2c3a44;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
            }
            QPushButton {
                background-color: #ba846c;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #a46f5c;
            }
            QPushButton:pressed {
                background-color: #8e5f50;
            }
        """)        
        self.setWindowTitle("Agregar ítem a la orden")
        layout = QFormLayout()

        self.input_pieza = QComboBox()
        piezas = obtener_todas_piezas()
        self.piezas_map = {}
        for p in piezas:
            self.input_pieza.addItem(p["nombre"], p["id"])
            self.piezas_map[p["nombre"]] = p["id"]

        self.input_cant = QSpinBox()
        self.input_cant.setMinimum(1)
        self.input_cant.setMaximum(100000)
        self.input_precio = QDoubleSpinBox()
        self.input_precio.setMinimum(0)
        self.input_precio.setMaximum(10000000)
        self.input_precio.setDecimals(2)

        layout.addRow("Pieza:", self.input_pieza)
        layout.addRow("Cantidad:", self.input_cant)
        layout.addRow("Precio unitario:", self.input_precio)

        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Agregar")
        self.btn_cancel = QPushButton("Cancelar")
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addRow(btns)
        self.setLayout(layout)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def datos(self):
        return (
            self.input_pieza.currentData(),
            self.input_cant.value(),
            self.input_precio.value()
        )

class DetalleOrdenWidget(QWidget):
    def __init__(self, orden_id):
        super().__init__()
        self.orden_id = orden_id
        self.setWindowTitle("Detalle de Orden de Compra")
        layout = QVBoxLayout()

        titulo = QLabel("Detalle de la Orden")
        titulo.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_agregar = QPushButton("Agregar ítem")
        self.btn_agregar.setStyleSheet(estilo_boton_general)        
        self.btn_agregar.clicked.connect(self.alta_item)
        btns.addWidget(self.btn_agregar)
        self.btn_eliminar = QPushButton("Eliminar ítem seleccionado")
        self.btn_eliminar.setStyleSheet(estilo_boton_general)   
        self.btn_eliminar.clicked.connect(self.eliminar_item)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.tabla = QTableWidget(0, 4)
        self.tabla.setHorizontalHeaderLabels([
            "ID Pieza", "Pieza", "Cantidad", "Precio unitario"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_detalle()

    def cargar_detalle(self):
        self.tabla.setRowCount(0)
        detalle = obtener_detalle_orden(self.orden_id)
        for item in detalle:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(item["pieza_id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(item["pieza"]))
            self.tabla.setItem(row_pos, 2, QTableWidgetItem(str(item["cantidad"])))
            self.tabla.setItem(row_pos, 3, QTableWidgetItem(f"{item['precio_unitario']:.2f}"))

    def alta_item(self):
        dlg = DetalleOrdenDialog(self.orden_id, self)
        if dlg.exec():
            pieza_id, cantidad, precio = dlg.datos()
            ok, err = agregar_item_orden(self.orden_id, pieza_id, cantidad, precio)
            if ok:
                self.cargar_detalle()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo agregar el ítem.\nDetalles: {err}")

    def eliminar_item(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminación", "Selecciona un ítem para eliminar.")
            return
        pieza_id = int(self.tabla.item(row, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar este ítem?")
        if r == QMessageBox.StandardButton.Yes:
            ok, err = eliminar_item_orden(self.orden_id, pieza_id)
            if ok:
                self.cargar_detalle()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el ítem.\nDetalles: {err}")
