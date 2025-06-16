from PyQt6.QtWidgets import ( 
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidgetItem, 
    QHeaderView, QDialog, QFormLayout, QLineEdit, QMessageBox
)
from modelos.ubicaciones import (
    obtener_ubicaciones, agregar_ubicacion, editar_ubicacion, eliminar_ubicacion
)
from vistas.tabla_estilizada import TablaEstilizada

class UbicacionDialog(QDialog):
    def __init__(self, parent=None, nombre_actual=""):
        super().__init__(parent)
        self.setWindowTitle("Ubicación")
        layout = QFormLayout()
        self.input_nombre = QLineEdit(nombre_actual)
        layout.addRow("Nombre:", self.input_nombre)
        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Guardar")
        self.btn_cancel = QPushButton("Cancelar")
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addRow(btns)
        self.setLayout(layout)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def nombre(self):
        return self.input_nombre.text().strip()

class UbicacionesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Ubicaciones")
        layout = QVBoxLayout()

        titulo = QLabel("Gestión de Ubicaciones")
        titulo.setStyleSheet("font-size: 18px;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_nueva = QPushButton("Agregar ubicación")
        self.btn_nueva.clicked.connect(self.alta_ubicacion)
        btns.addWidget(self.btn_nueva)
        self.btn_editar = QPushButton("Editar ubicación seleccionada")
        self.btn_editar.clicked.connect(self.editar_ubicacion)
        btns.addWidget(self.btn_editar)
        self.btn_eliminar = QPushButton("Eliminar ubicación seleccionada")
        self.btn_eliminar.clicked.connect(self.eliminar_ubicacion)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.ubicaciones_todas = []

        self.tabla = TablaEstilizada(0, 2)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_ubicaciones()

    def cargar_ubicaciones(self):
        self.ubicaciones_todas = obtener_ubicaciones()
        self.mostrar_ubicaciones(self.ubicaciones_todas)

    def mostrar_ubicaciones(self, ubicaciones):
        self.tabla.setRowCount(0)
        for ubicacion in ubicaciones:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(ubicacion["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(ubicacion["nombre"]))

    def alta_ubicacion(self):
        dlg = UbicacionDialog(self)
        if dlg.exec():
            nombre = dlg.nombre()
            if not nombre:
                QMessageBox.warning(self, "Campo obligatorio", "El nombre es obligatorio.")
                return
            ok, err = agregar_ubicacion(nombre)
            if ok:
                self.cargar_ubicaciones()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo agregar la ubicación.\nDetalles: {err}")

    def editar_ubicacion(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Edición", "Selecciona una ubicación para editar.")
            return
        ubicacion_id = int(self.tabla.item(row, 0).text())
        nombre_actual = self.tabla.item(row, 1).text()
        dlg = UbicacionDialog(self, nombre_actual)
        if dlg.exec():
            nuevo_nombre = dlg.nombre()
            if not nuevo_nombre:
                QMessageBox.warning(self, "Campo obligatorio", "El nombre es obligatorio.")
                return
            ok, err = editar_ubicacion(ubicacion_id, nuevo_nombre)
            if ok:
                self.cargar_ubicaciones()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo editar la ubicación.\nDetalles: {err}")

    def eliminar_ubicacion(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminación", "Selecciona una ubicación para eliminar.")
            return
        ubicacion_id = int(self.tabla.item(row, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar esta ubicación?")
        if r == QMessageBox.StandardButton.Yes:
            ok, err = eliminar_ubicacion(ubicacion_id)
            if ok:
                self.cargar_ubicaciones()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar la ubicación.\nDetalles: {err}")

    def filtrar(self, texto):
        texto = texto.lower()
        ubicaciones_filtradas = [
            u for u in self.ubicaciones_todas
            if texto in u["nombre"].lower()
        ]
        self.mostrar_ubicaciones(ubicaciones_filtradas)
