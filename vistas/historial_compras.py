from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QComboBox, QDoubleSpinBox, QDateEdit, QMessageBox
)
from modelos.historial_compras import obtener_historial_compras, agregar_compra, eliminar_compra
from modelos.piezas import obtener_todas_piezas
from modelos.proveedores import obtener_proveedores
from PyQt6.QtCore import QDate
from vistas.tabla_estilizada import TablaEstilizada
from estilos import estilo_titulo, estilo_boton_general

class AltaCompraDialog(QDialog):
    def __init__(self, parent=None):
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
        self.setWindowTitle("Registrar compra")
        layout = QFormLayout()

        self.input_pieza = QComboBox()
        piezas = obtener_todas_piezas()
        for p in piezas:
            self.input_pieza.addItem(p["nombre"], p["id"])

        self.input_proveedor = QComboBox()
        proveedores = obtener_proveedores()
        for pr in proveedores:
            self.input_proveedor.addItem(pr["nombre"], pr["id"])

        self.input_precio = QDoubleSpinBox()
        self.input_precio.setMinimum(0)
        self.input_precio.setMaximum(10000000)
        self.input_precio.setDecimals(2)
        self.input_fecha = QDateEdit()
        self.input_fecha.setCalendarPopup(True)
        self.input_fecha.setDate(QDate.currentDate())

        layout.addRow("Pieza:", self.input_pieza)
        layout.addRow("Proveedor:", self.input_proveedor)
        layout.addRow("Precio:", self.input_precio)
        layout.addRow("Fecha:", self.input_fecha)

        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Guardar")
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
            self.input_proveedor.currentData(),
            self.input_precio.value(),
            self.input_fecha.date().toString("yyyy-MM-dd")
        )

class HistorialComprasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historial de Compras")
        layout = QVBoxLayout()

        titulo = QLabel("Historial de Compras")
        titulo.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_nueva = QPushButton("Registrar compra")
        self.btn_nueva.setStyleSheet(estilo_boton_general)
        self.btn_nueva.clicked.connect(self.alta_compra)
        btns.addWidget(self.btn_nueva)
        self.btn_eliminar = QPushButton("Eliminar compra seleccionada")
        self.btn_eliminar.setStyleSheet(estilo_boton_general)
        self.btn_eliminar.clicked.connect(self.eliminar_compra)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.compras_todas = []

        self.tabla = TablaEstilizada(0, 6)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Pieza", "Proveedor", "Precio", "Fecha", "Observaciones"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_historial()

    def cargar_historial(self):
        self.compras_todas = obtener_historial_compras()
        self.mostrar_historial(self.compras_todas)

    def mostrar_historial(self, compras):
        self.tabla.setRowCount(0)
        for c in compras:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(c["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(c["pieza"]))
            self.tabla.setItem(row_pos, 2, QTableWidgetItem(c["proveedor"]))
            self.tabla.setItem(row_pos, 3, QTableWidgetItem(f"{c['precio']:.2f}"))
            self.tabla.setItem(row_pos, 4, QTableWidgetItem(c["fecha"]))
            self.tabla.setItem(row_pos, 5, QTableWidgetItem(c.get("observaciones", "") or ""))


    def alta_compra(self):
        dlg = AltaCompraDialog(self)
        if dlg.exec():
            pieza_id, proveedor_id, precio, fecha = dlg.datos()
            ok, err = agregar_compra(pieza_id, proveedor_id, precio, fecha)
            if ok:
                self.cargar_historial()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo registrar la compra.\nDetalles: {err}")

    def eliminar_compra(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminación", "Selecciona una compra para eliminar.")
            return
        compra_id = int(self.tabla.item(row, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar esta compra?")
        if r == QMessageBox.StandardButton.Yes:
            ok, err = eliminar_compra(compra_id)
            if ok:
                self.cargar_historial()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar la compra.\nDetalles: {err}")

    def filtrar(self, texto):
        texto = texto.lower()
        compras_filtradas = [
            c for c in self.compras_todas
            if texto in (c["pieza"] or "").lower()
            or texto in (c["proveedor"] or "").lower()
            or texto in str(c["precio"])
            or texto in (c["fecha"] or "").lower()
            or texto in (c.get("observaciones", "") or "").lower()
        ]
        self.mostrar_historial(compras_filtradas)
