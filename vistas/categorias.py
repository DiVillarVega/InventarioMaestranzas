from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QLineEdit, QMessageBox
)
from modelos.categorias import (
    obtener_categorias, agregar_categoria, editar_categoria, eliminar_categoria
)
from vistas.tabla_estilizada import TablaEstilizada
from estilos import estilo_titulo, estilo_boton_general

class CategoriaDialog(QDialog):
    def __init__(self, parent=None, nombre_actual=""):
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
        self.setWindowTitle("Categoría")
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

class CategoriasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Categorías")
        layout = QVBoxLayout()

        titulo = QLabel("Gestión de Categorías")
        titulo.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_nueva = QPushButton("Agregar categoría")
        self.btn_nueva.setStyleSheet(estilo_boton_general)       
        self.btn_nueva.clicked.connect(self.alta_categoria)
        btns.addWidget(self.btn_nueva)
        self.btn_editar = QPushButton("Editar categoría seleccionada")
        self.btn_editar.setStyleSheet(estilo_boton_general)
        self.btn_editar.clicked.connect(self.editar_categoria)
        btns.addWidget(self.btn_editar)
        self.btn_eliminar = QPushButton("Eliminar categoría seleccionada")
        self.btn_eliminar.setStyleSheet(estilo_boton_general)
        self.btn_eliminar.clicked.connect(self.eliminar_categoria)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.categorias_todas = []

        self.tabla = TablaEstilizada(0, 2)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_categorias()

    def cargar_categorias(self):
        self.categorias_todas = obtener_categorias()
        self.mostrar_categorias(self.categorias_todas)

    def mostrar_categorias(self, categorias):
        self.tabla.setRowCount(0)
        for categoria in categorias:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(categoria["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(categoria["nombre"]))

    def alta_categoria(self):
        dlg = CategoriaDialog(self)
        if dlg.exec():
            nombre = dlg.nombre()
            if not nombre:
                QMessageBox.warning(self, "Campo obligatorio", "El nombre es obligatorio.")
                return
            ok, err = agregar_categoria(nombre)
            if ok:
                self.cargar_categorias()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo agregar la categoría.\nDetalles: {err}")

    def editar_categoria(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Edición", "Selecciona una categoría para editar.")
            return
        categoria_id = int(self.tabla.item(row, 0).text())
        nombre_actual = self.tabla.item(row, 1).text()
        dlg = CategoriaDialog(self, nombre_actual)
        if dlg.exec():
            nuevo_nombre = dlg.nombre()
            if not nuevo_nombre:
                QMessageBox.warning(self, "Campo obligatorio", "El nombre es obligatorio.")
                return
            ok, err = editar_categoria(categoria_id, nuevo_nombre)
            if ok:
                self.cargar_categorias()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo editar la categoría.\nDetalles: {err}")

    def eliminar_categoria(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminación", "Selecciona una categoría para eliminar.")
            return
        categoria_id = int(self.tabla.item(row, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar esta categoría?")
        if r == QMessageBox.StandardButton.Yes:
            ok, err = eliminar_categoria(categoria_id)
            if ok:
                self.cargar_categorias()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar la categoría.\nDetalles: {err}")

    def filtrar(self, texto):
        texto = texto.lower()
        categorias_filtradas = [
            c for c in self.categorias_todas
            if texto in c["nombre"].lower()
        ]
        self.mostrar_categorias(categorias_filtradas)
