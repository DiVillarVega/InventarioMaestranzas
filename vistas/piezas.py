from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QTableWidgetItem, QHeaderView, QLineEdit, QDialog, QFormLayout, QSpinBox, QMessageBox
)
from modelos.piezas import obtener_todas_piezas, agregar_pieza, editar_pieza, eliminar_pieza
from vistas.tabla_estilizada import TablaEstilizada

class AltaPiezaDialog(QDialog):
    def __init__(self, parent=None, pieza=None):
        super().__init__(parent)
        self.setWindowTitle("Alta/Edición de Pieza")
        layout = QFormLayout()

        self.input_codigo = QLineEdit()
        self.input_nombre = QLineEdit()
        self.input_desc = QLineEdit()
        self.input_stock = QSpinBox()
        self.input_stock.setMinimum(0)
        self.input_stock.setMaximum(100000)
        self.input_ubic = QLineEdit()

        layout.addRow("Código:", self.input_codigo)
        layout.addRow("Nombre:", self.input_nombre)
        layout.addRow("Descripción:", self.input_desc)
        layout.addRow("Stock:", self.input_stock)
        layout.addRow("Ubicación:", self.input_ubic)

        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Guardar")
        self.btn_cancel = QPushButton("Cancelar")
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)

        layout.addRow(btns)
        self.setLayout(layout)

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

        # Si es edición, cargar datos
        self.pieza = pieza
        if pieza:
            self.input_codigo.setText(pieza["codigo"])
            self.input_nombre.setText(pieza["nombre"])
            self.input_desc.setText(pieza["descripcion"] or "")
            self.input_stock.setValue(pieza["stock"])
            self.input_ubic.setText(pieza["ubicacion"] or "")

    def datos(self):
        return (
            self.input_codigo.text(),
            self.input_nombre.text(),
            self.input_desc.text(),
            self.input_stock.value(),
            self.input_ubic.text()
        )

class PiezasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Piezas")
        layout = QVBoxLayout()

        titulo = QLabel("Gestión de Piezas")
        titulo.setStyleSheet("font-size: 18px;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_nueva = QPushButton("Agregar nueva pieza")
        self.btn_nueva.clicked.connect(self.alta_pieza)
        btns.addWidget(self.btn_nueva)

        self.btn_editar = QPushButton("Editar pieza seleccionada")
        self.btn_editar.clicked.connect(self.editar_pieza)
        btns.addWidget(self.btn_editar)

        self.btn_eliminar = QPushButton("Eliminar pieza seleccionada")
        self.btn_eliminar.clicked.connect(self.eliminar_pieza)
        btns.addWidget(self.btn_eliminar)

        layout.addLayout(btns)

        # Inicializa la lista para el filtro
        self.piezas_todas = []

        # Tabla estilizada
        self.tabla = TablaEstilizada(0, 6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Código", "Nombre", "Descripción", "Stock", "Ubicación"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)
        
        self.setLayout(layout)
        self.cargar_piezas()

    def cargar_piezas(self):
        self.piezas_todas = obtener_todas_piezas()
        self.mostrar_piezas(self.piezas_todas)

    def mostrar_piezas(self, piezas):
        self.tabla.setRowCount(0)
        for pieza in piezas:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(pieza["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(pieza["codigo"]))
            self.tabla.setItem(row_pos, 2, QTableWidgetItem(pieza["nombre"]))
            self.tabla.setItem(row_pos, 3, QTableWidgetItem(pieza["descripcion"] or ""))
            self.tabla.setItem(row_pos, 4, QTableWidgetItem(str(pieza["stock"])))
            self.tabla.setItem(row_pos, 5, QTableWidgetItem(pieza["ubicacion"] or ""))

    def alta_pieza(self):
        dlg = AltaPiezaDialog(self)
        if dlg.exec():
            codigo, nombre, desc, stock, ubicacion = dlg.datos()
            if not codigo or not nombre or stock is None:
                QMessageBox.warning(self, "Campos obligatorios", "Código, nombre y stock son obligatorios.")
                return
            ok, err = agregar_pieza(codigo, nombre, desc, stock, ubicacion)
            if ok:
                self.cargar_piezas()
                QMessageBox.information(self, "Éxito", "La pieza fue registrada correctamente.")
            else:
                QMessageBox.critical(self, "Error", f"No se pudo registrar la pieza.\nDetalles: {err}")


    def editar_pieza(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Edición", "Seleccione una pieza para editar")
            return
        pieza = {
            "id": int(self.tabla.item(row, 0).text()),
            "codigo": self.tabla.item(row, 1).text(),
            "nombre": self.tabla.item(row, 2).text(),
            "descripcion": self.tabla.item(row, 3).text(),
            "stock": int(self.tabla.item(row, 4).text()),
            "ubicacion": self.tabla.item(row, 5).text(),
        }
        dlg = AltaPiezaDialog(self, pieza)
        if dlg.exec():
            codigo, nombre, desc, stock, ubicacion = dlg.datos()
            editar_pieza(pieza["id"], codigo, nombre, desc, stock, ubicacion)
            self.cargar_piezas()

    def eliminar_pieza(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminación", "Seleccione una pieza para eliminar")
            return
        pieza_id = int(self.tabla.item(row, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar esta pieza?")
        if r == QMessageBox.StandardButton.Yes:
            eliminar_pieza(pieza_id)
            self.cargar_piezas()

    def filtrar(self, texto):
        texto = texto.lower()
        piezas_filtradas = [
            p for p in self.piezas_todas
            if texto in p["codigo"].lower()
            or texto in p["nombre"].lower()
            or texto in (p["descripcion"] or "").lower()
            or texto in (p["ubicacion"] or "").lower()
        ]
        self.mostrar_piezas(piezas_filtradas)
