from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QComboBox, QSpinBox, QTextEdit, QMessageBox
)
from modelos.movimientos import (
    obtener_movimientos, registrar_movimiento, obtener_piezas_id_nombre, obtener_stock_actual
)
from PyQt6.QtCore import Qt
from vistas.tabla_estilizada import TablaEstilizada
from estilos import estilo_titulo, estilo_boton_general

class AltaMovimientoDialog(QDialog):
    def __init__(self, user_id, parent=None):
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
        self.setWindowTitle("Registrar Movimiento")
        layout = QFormLayout()

        self.input_tipo = QComboBox()
        self.input_tipo.addItems(["entrada", "salida"])
        self.input_pieza = QComboBox()
        piezas = obtener_piezas_id_nombre()
        self.piezas_map = {}
        for p_id, p_nombre in piezas:
            self.input_pieza.addItem(p_nombre, p_id)
            self.piezas_map[p_nombre] = p_id

        self.input_cant = QSpinBox()
        self.input_cant.setMinimum(1)
        self.input_cant.setMaximum(100000)
        self.input_obs = QTextEdit()

        layout.addRow("Tipo:", self.input_tipo)
        layout.addRow("Pieza:", self.input_pieza)
        layout.addRow("Cantidad:", self.input_cant)
        layout.addRow("Observaciones:", self.input_obs)

        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Guardar")
        self.btn_cancel = QPushButton("Cancelar")
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addRow(btns)
        self.setLayout(layout)

        self.btn_ok.clicked.connect(self.on_accept)
        self.btn_cancel.clicked.connect(self.reject)
        self.accepted = False  # flag para saber si todo fue validado

        self.user_id = user_id

        # Si no hay piezas, deshabilitar formulario
        if len(piezas) == 0:
            self.input_tipo.setEnabled(False)
            self.input_pieza.setEnabled(False)
            self.input_cant.setEnabled(False)
            self.input_obs.setEnabled(False)
            self.btn_ok.setEnabled(False)
            QMessageBox.warning(self, "No hay piezas", "Debes crear al menos una pieza antes de registrar movimientos.")

    def on_accept(self):
        pieza_id = self.input_pieza.currentData()
        tipo = self.input_tipo.currentText()
        cantidad = self.input_cant.value()
        if pieza_id is None:
            QMessageBox.warning(self, "Error", "Debes seleccionar una pieza.")
            return
        if cantidad <= 0:
            QMessageBox.warning(self, "Cantidad inválida", "La cantidad debe ser mayor a cero.")
            return
        if tipo == "salida":
            stock_actual = obtener_stock_actual(pieza_id)
            if cantidad > stock_actual:
                QMessageBox.warning(self, "Stock insuficiente",
                    f"La pieza seleccionada tiene un stock de {stock_actual}. No puedes retirar más que eso.")
                return
        self.accepted = True
        self.accept()

    def datos(self):
        pieza_id = self.input_pieza.currentData()
        tipo = self.input_tipo.currentText()
        cantidad = self.input_cant.value()
        obs = self.input_obs.toPlainText()
        return pieza_id, tipo, cantidad, self.user_id, obs

class MovimientosWidget(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Registro de Movimientos")
        layout = QVBoxLayout()

        titulo = QLabel("Movimientos de Inventario")
        titulo.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        layout.addWidget(titulo)

        self.btn_nuevo = QPushButton("Registrar nuevo movimiento")
        self.btn_nuevo.setStyleSheet(estilo_boton_general)
        self.btn_nuevo.clicked.connect(self.alta_movimiento)
        layout.addWidget(self.btn_nuevo)

        self.movimientos_todos = []

        self.tabla = TablaEstilizada(0, 6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Pieza", "Tipo", "Cantidad", "Fecha", "Usuario"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_movimientos()

    def cargar_movimientos(self):
        self.movimientos_todos = obtener_movimientos()
        self.mostrar_movimientos(self.movimientos_todos)

    def mostrar_movimientos(self, movimientos):
        self.tabla.setRowCount(0)
        for mov in movimientos:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(mov["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(mov["pieza"]))
            self.tabla.setItem(row_pos, 2, QTableWidgetItem(mov["tipo"].capitalize()))
            self.tabla.setItem(row_pos, 3, QTableWidgetItem(str(mov["cantidad"])))
            self.tabla.setItem(row_pos, 4, QTableWidgetItem(mov["fecha"]))
            self.tabla.setItem(row_pos, 5, QTableWidgetItem(mov["usuario"]))

    def alta_movimiento(self):
        dlg = AltaMovimientoDialog(self.user_id, self)
        result = dlg.exec()
        if result and getattr(dlg, "accepted", False):
            pieza_id, tipo, cantidad, user_id, obs = dlg.datos()
            registrar_movimiento(pieza_id, tipo, cantidad, user_id, obs)
            self.cargar_movimientos()

    def filtrar(self, texto):
        texto = texto.lower()
        movs_filtrados = [
            m for m in self.movimientos_todos
            if texto in m["pieza"].lower()
            or texto in m["tipo"].lower()
            or texto in (m["usuario"] or "").lower()
            or texto in str(m["cantidad"])
            or texto in str(m["fecha"])
            or texto in (m.get("observacion", "") or "").lower()
        ]
        self.mostrar_movimientos(movs_filtrados)
