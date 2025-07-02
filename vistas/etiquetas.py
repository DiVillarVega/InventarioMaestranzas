from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QLineEdit, QMessageBox
)
from modelos.etiquetas import (
    obtener_etiquetas, agregar_etiqueta, editar_etiqueta, eliminar_etiqueta
)
from vistas.tabla_estilizada import TablaEstilizada
from estilos import estilo_titulo, estilo_boton_general

class EtiquetaDialog(QDialog):
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
        self.setWindowTitle("Etiqueta")
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

class EtiquetasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Etiquetas")
        layout = QVBoxLayout()

        titulo = QLabel("Gestión de Etiquetas")
        titulo.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_nueva = QPushButton("Agregar etiqueta")
        self.btn_nueva.setStyleSheet(estilo_boton_general)
        self.btn_nueva.clicked.connect(self.alta_etiqueta)
        btns.addWidget(self.btn_nueva)
        self.btn_editar = QPushButton("Editar etiqueta seleccionada")
        self.btn_editar.setStyleSheet(estilo_boton_general)
        self.btn_editar.clicked.connect(self.editar_etiqueta)
        btns.addWidget(self.btn_editar)
        self.btn_eliminar = QPushButton("Eliminar etiqueta seleccionada")
        self.btn_eliminar.setStyleSheet(estilo_boton_general)
        self.btn_eliminar.clicked.connect(self.eliminar_etiqueta)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.etiquetas_todas = []

        self.tabla = TablaEstilizada(0, 2)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_etiquetas()

    def cargar_etiquetas(self):
        self.etiquetas_todas = obtener_etiquetas()
        self.mostrar_etiquetas(self.etiquetas_todas)

    def mostrar_etiquetas(self, etiquetas):
        self.tabla.setRowCount(0)
        for etiqueta in etiquetas:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(etiqueta["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(etiqueta["nombre"]))

    def alta_etiqueta(self):
        dlg = EtiquetaDialog(self)
        if dlg.exec():
            nombre = dlg.nombre()
            if not nombre:
                QMessageBox.warning(self, "Campo obligatorio", "El nombre es obligatorio.")
                return
            ok, err = agregar_etiqueta(nombre)
            if ok:
                self.cargar_etiquetas()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo agregar la etiqueta.\nDetalles: {err}")

    def editar_etiqueta(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Edición", "Selecciona una etiqueta para editar.")
            return
        etiqueta_id = int(self.tabla.item(row, 0).text())
        nombre_actual = self.tabla.item(row, 1).text()
        dlg = EtiquetaDialog(self, nombre_actual)
        if dlg.exec():
            nuevo_nombre = dlg.nombre()
            if not nuevo_nombre:
                QMessageBox.warning(self, "Campo obligatorio", "El nombre es obligatorio.")
                return
            ok, err = editar_etiqueta(etiqueta_id, nuevo_nombre)
            if ok:
                self.cargar_etiquetas()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo editar la etiqueta.\nDetalles: {err}")

    def eliminar_etiqueta(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminación", "Selecciona una etiqueta para eliminar.")
            return
        etiqueta_id = int(self.tabla.item(row, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar esta etiqueta?")
        if r == QMessageBox.StandardButton.Yes:
            ok, err = eliminar_etiqueta(etiqueta_id)
            if ok:
                self.cargar_etiquetas()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar la etiqueta.\nDetalles: {err}")
                
    def filtrar(self, texto):
        texto = texto.lower()
        etiquetas_filtradas = [
            e for e in self.etiquetas_todas
            if texto in e["nombre"].lower()
        ]
        self.mostrar_etiquetas(etiquetas_filtradas)
