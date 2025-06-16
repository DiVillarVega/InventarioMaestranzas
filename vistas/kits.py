from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QLineEdit, QComboBox, QSpinBox, QMessageBox, QTableWidget
)
from modelos.kits import (
    obtener_kits, agregar_kit, editar_kit, eliminar_kit,
    obtener_piezas_kit, agregar_pieza_a_kit, eliminar_pieza_de_kit
)
from modelos.piezas import obtener_todas_piezas
from vistas.tabla_estilizada import TablaEstilizada

class PiezasKitDialog(QDialog):
    def __init__(self, kit_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar pieza a kit")
        layout = QFormLayout()

        self.input_pieza = QComboBox()
        piezas = obtener_todas_piezas()
        for p in piezas:
            self.input_pieza.addItem(p["nombre"], p["id"])

        self.input_cant = QSpinBox()
        self.input_cant.setMinimum(1)
        self.input_cant.setMaximum(100000)

        layout.addRow("Pieza:", self.input_pieza)
        layout.addRow("Cantidad:", self.input_cant)

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
            self.input_cant.value()
        )

class KitsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Kits")
        layout = QVBoxLayout()

        titulo = QLabel("Gestión de Kits")
        titulo.setStyleSheet("font-size: 18px;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_nuevo = QPushButton("Agregar kit")
        self.btn_nuevo.clicked.connect(self.alta_kit)
        btns.addWidget(self.btn_nuevo)
        self.btn_editar = QPushButton("Editar kit seleccionado")
        self.btn_editar.clicked.connect(self.editar_kit)
        btns.addWidget(self.btn_editar)
        self.btn_eliminar = QPushButton("Eliminar kit seleccionado")
        self.btn_eliminar.clicked.connect(self.eliminar_kit)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.kits_todos = []

        self.tabla = TablaEstilizada(0, 2)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        # Tabla para las piezas del kit
        self.tabla_piezas = TablaEstilizada(0, 3)
        self.tabla_piezas.setHorizontalHeaderLabels(["ID Pieza", "Nombre Pieza", "Cantidad"])
        self.tabla_piezas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(QLabel("Piezas del kit seleccionado:"))
        layout.addWidget(self.tabla_piezas)

        btns_piezas = QHBoxLayout()
        self.btn_agregar_pieza = QPushButton("Agregar pieza a kit")
        self.btn_agregar_pieza.clicked.connect(self.alta_pieza_kit)
        btns_piezas.addWidget(self.btn_agregar_pieza)
        self.btn_eliminar_pieza = QPushButton("Eliminar pieza de kit")
        self.btn_eliminar_pieza.clicked.connect(self.eliminar_pieza_kit)
        btns_piezas.addWidget(self.btn_eliminar_pieza)
        layout.addLayout(btns_piezas)

        self.setLayout(layout)
        self.cargar_kits()
        self.tabla.currentCellChanged.connect(lambda *_: self.cargar_piezas_kit())

    def cargar_kits(self):
        self.kits_todos = obtener_kits()
        self.mostrar_kits(self.kits_todos)
        self.tabla_piezas.setRowCount(0)

    def mostrar_kits(self, kits):
        self.tabla.setRowCount(0)
        for kit in kits:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(kit["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(kit["nombre"]))

    def alta_kit(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Agregar kit")
        layout = QFormLayout()
        input_nombre = QLineEdit()
        layout.addRow("Nombre:", input_nombre)
        btns = QHBoxLayout()
        btn_ok = QPushButton("Guardar")
        btn_cancel = QPushButton("Cancelar")
        btns.addWidget(btn_ok)
        btns.addWidget(btn_cancel)
        layout.addRow(btns)
        dlg.setLayout(layout)
        btn_ok.clicked.connect(dlg.accept)
        btn_cancel.clicked.connect(dlg.reject)
        if dlg.exec():
            nombre = input_nombre.text().strip()
            if not nombre:
                QMessageBox.warning(self, "Campo obligatorio", "El nombre del kit es obligatorio.")
                return
            ok, err = agregar_kit(nombre)
            if ok:
                self.cargar_kits()
                QMessageBox.information(self, "Éxito", "El kit fue registrado correctamente.")
            else:
                QMessageBox.critical(self, "Error", f"No se pudo registrar el kit.\nDetalles: {err}")

    def editar_kit(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Edición", "Selecciona un kit para editar.")
            return
        kit_id = int(self.tabla.item(row, 0).text())
        nombre_actual = self.tabla.item(row, 1).text()
        dlg = QDialog(self)
        dlg.setWindowTitle("Editar kit")
        layout = QFormLayout()
        input_nombre = QLineEdit(nombre_actual)
        layout.addRow("Nombre:", input_nombre)
        btns = QHBoxLayout()
        btn_ok = QPushButton("Guardar")
        btn_cancel = QPushButton("Cancelar")
        btns.addWidget(btn_ok)
        btns.addWidget(btn_cancel)
        layout.addRow(btns)
        dlg.setLayout(layout)
        btn_ok.clicked.connect(dlg.accept)
        btn_cancel.clicked.connect(dlg.reject)
        if dlg.exec():
            nuevo_nombre = input_nombre.text().strip()
            if not nuevo_nombre:
                QMessageBox.warning(self, "Campo obligatorio", "El nombre es obligatorio.")
                return
            ok, err = editar_kit(kit_id, nuevo_nombre)
            if ok:
                self.cargar_kits()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo editar el kit.\nDetalles: {err}")

    def eliminar_kit(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminación", "Selecciona un kit para eliminar.")
            return
        kit_id = int(self.tabla.item(row, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar este kit?")
        if r == QMessageBox.StandardButton.Yes:
            ok, err = eliminar_kit(kit_id)
            if ok:
                self.cargar_kits()
                self.tabla_piezas.setRowCount(0)
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el kit.\nDetalles: {err}")

    def cargar_piezas_kit(self):
        row = self.tabla.currentRow()
        if row == -1:
            self.tabla_piezas.setRowCount(0)
            return
        kit_id = int(self.tabla.item(row, 0).text())
        piezas = obtener_piezas_kit(kit_id)
        self.tabla_piezas.setRowCount(0)
        for pieza in piezas:
            row_pos = self.tabla_piezas.rowCount()
            self.tabla_piezas.insertRow(row_pos)
            self.tabla_piezas.setItem(row_pos, 0, QTableWidgetItem(str(pieza["pieza_id"])))
            self.tabla_piezas.setItem(row_pos, 1, QTableWidgetItem(pieza["nombre"]))
            self.tabla_piezas.setItem(row_pos, 2, QTableWidgetItem(str(pieza["cantidad"])))

    def alta_pieza_kit(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Selección", "Selecciona un kit primero.")
            return
        kit_id = int(self.tabla.item(row, 0).text())
        dlg = PiezasKitDialog(kit_id, self)
        if dlg.exec():
            pieza_id, cantidad = dlg.datos()
            ok, err = agregar_pieza_a_kit(kit_id, pieza_id, cantidad)
            if ok:
                self.cargar_piezas_kit()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo agregar la pieza.\nDetalles: {err}")

    def eliminar_pieza_kit(self):
        row = self.tabla.currentRow()
        row_pz = self.tabla_piezas.currentRow()
        if row == -1 or row_pz == -1:
            QMessageBox.warning(self, "Selección", "Selecciona un kit y una pieza del kit.")
            return
        kit_id = int(self.tabla.item(row, 0).text())
        pieza_id = int(self.tabla_piezas.item(row_pz, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar esta pieza del kit?")
        if r == QMessageBox.StandardButton.Yes:
            ok, err = eliminar_pieza_de_kit(kit_id, pieza_id)
            if ok:
                self.cargar_piezas_kit()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar la pieza del kit.\nDetalles: {err}")

    def filtrar(self, texto):
        texto = texto.lower()
        kits_filtrados = [
            k for k in self.kits_todos
            if texto in k["nombre"].lower()
        ]
        self.mostrar_kits(kits_filtrados)
