from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QComboBox, QSpinBox,
    QDateEdit, QMessageBox, QLineEdit
)
from modelos.lotes import obtener_lotes, agregar_lote, editar_lote, eliminar_lote
from modelos.movimientos import obtener_piezas_id_nombre
from PyQt6.QtCore import QDate
from vistas.tabla_estilizada import TablaEstilizada

class LoteDialog(QDialog):
    def __init__(self, parent=None, lote=None):
        super().__init__(parent)
        self.setWindowTitle("Alta/Edición de Lote")
        layout = QFormLayout()

        self.input_pieza = QComboBox()
        self.piezas = obtener_piezas_id_nombre()
        for p_id, p_nombre in self.piezas:
            self.input_pieza.addItem(p_nombre, p_id)

        self.input_codigo = QLineEdit()
        self.input_cant = QSpinBox()
        self.input_cant.setMinimum(1)
        self.input_cant.setMaximum(100000)
        self.input_fecha = QDateEdit()
        self.input_fecha.setCalendarPopup(True)
        self.input_fecha.setDate(QDate.currentDate())

        layout.addRow("Pieza:", self.input_pieza)
        layout.addRow("Código lote:", self.input_codigo)
        layout.addRow("Fecha vencimiento:", self.input_fecha)
        layout.addRow("Cantidad:", self.input_cant)

        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Guardar")
        self.btn_cancel = QPushButton("Cancelar")
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addRow(btns)
        self.setLayout(layout)

        self.btn_ok.clicked.connect(self.on_accept)
        self.btn_cancel.clicked.connect(self.reject)
        self.accepted = False

        # Si es edición, precarga datos
        if lote:
            idx = self.input_pieza.findText(lote["pieza"])
            if idx != -1:
                self.input_pieza.setCurrentIndex(idx)
            self.input_codigo.setText(lote["codigo"])
            self.input_fecha.setDate(QDate.fromString(lote["vencimiento"], "yyyy-MM-dd"))
            self.input_cant.setValue(lote["cantidad"])

        # Validación si no hay piezas
        if not self.piezas:
            self.input_pieza.setEnabled(False)
            self.input_codigo.setEnabled(False)
            self.input_cant.setEnabled(False)
            self.input_fecha.setEnabled(False)
            self.btn_ok.setEnabled(False)
            QMessageBox.warning(self, "No hay piezas", "Debes crear al menos una pieza antes de agregar lotes.")

    def on_accept(self):
        pieza_id = self.input_pieza.currentData()
        codigo = self.input_codigo.text()
        cantidad = self.input_cant.value()
        fecha = self.input_fecha.date().toString("yyyy-MM-dd")
        if pieza_id is None:
            QMessageBox.warning(self, "Error", "Debes seleccionar una pieza.")
            return
        if not codigo:
            QMessageBox.warning(self, "Error", "El código de lote es obligatorio.")
            return
        if cantidad <= 0:
            QMessageBox.warning(self, "Error", "La cantidad debe ser mayor a cero.")
            return
        if QDate.fromString(fecha, "yyyy-MM-dd") < QDate.currentDate():
            QMessageBox.warning(self, "Fecha inválida", "La fecha de vencimiento debe ser hoy o en el futuro.")
            return
        self.accepted = True
        self.accept()

    def datos(self):
        return (
            self.input_pieza.currentData(),
            self.input_codigo.text(),
            self.input_fecha.date().toString("yyyy-MM-dd"),
            self.input_cant.value()
        )

class LotesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Lotes")
        layout = QVBoxLayout()

        titulo = QLabel("Gestión de Lotes")
        titulo.setStyleSheet("font-size: 18px;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_nuevo = QPushButton("Agregar lote")
        self.btn_nuevo.clicked.connect(self.alta_lote)
        btns.addWidget(self.btn_nuevo)
        self.btn_editar = QPushButton("Editar lote seleccionado")
        self.btn_editar.clicked.connect(self.editar_lote)
        btns.addWidget(self.btn_editar)
        self.btn_eliminar = QPushButton("Eliminar lote seleccionado")
        self.btn_eliminar.clicked.connect(self.eliminar_lote)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.tabla = TablaEstilizada(0, 5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Pieza", "Código lote", "Vencimiento", "Cantidad"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_lotes()

    def cargar_lotes(self):
        self.tabla.setRowCount(0)
        lotes = obtener_lotes()
        for lote in lotes:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(lote["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(lote["pieza"]))
            self.tabla.setItem(row_pos, 2, QTableWidgetItem(lote["codigo"]))
            self.tabla.setItem(row_pos, 3, QTableWidgetItem(lote["vencimiento"]))
            self.tabla.setItem(row_pos, 4, QTableWidgetItem(str(lote["cantidad"])))

    def alta_lote(self):
        dlg = LoteDialog(self)
        if dlg.exec() and dlg.accepted:
            pieza_id, codigo, fecha, cantidad = dlg.datos()
            agregar_lote(pieza_id, codigo, fecha, cantidad)
            self.cargar_lotes()

    def editar_lote(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Edición", "Selecciona un lote para editar.")
            return
        lote = {
            "id": int(self.tabla.item(row, 0).text()),
            "pieza": self.tabla.item(row, 1).text(),
            "codigo": self.tabla.item(row, 2).text(),
            "vencimiento": self.tabla.item(row, 3).text(),
            "cantidad": int(self.tabla.item(row, 4).text())
        }
        dlg = LoteDialog(self, lote)
        if dlg.exec() and dlg.accepted:
            pieza_id, codigo, fecha, cantidad = dlg.datos()
            editar_lote(lote["id"], pieza_id, codigo, fecha, cantidad)
            self.cargar_lotes()

    def eliminar_lote(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminación", "Selecciona un lote para eliminar.")
            return
        lote_id = int(self.tabla.item(row, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar este lote?")
        if r == QMessageBox.StandardButton.Yes:
            eliminar_lote(lote_id)
            self.cargar_lotes()
