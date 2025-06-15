from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QLineEdit, QMessageBox
)
from modelos.respaldos import obtener_respaldos, agregar_respaldo, eliminar_respaldo
from vistas.tabla_estilizada import TablaEstilizada
class AltaRespaldoDialog(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar respaldo")
        layout = QFormLayout()
        self.input_ruta = QLineEdit()
        layout.addRow("Ruta archivo:", self.input_ruta)

        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Guardar")
        self.btn_cancel = QPushButton("Cancelar")
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addRow(btns)
        self.setLayout(layout)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        self.user_id = user_id

    def datos(self):
        return self.user_id, self.input_ruta.text().strip()

class RespaldosWidget(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Gestión de Respaldos")
        layout = QVBoxLayout()

        titulo = QLabel("Gestión de Respaldos")
        titulo.setStyleSheet("font-size: 18px;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_nuevo = QPushButton("Registrar respaldo")
        self.btn_nuevo.clicked.connect(self.alta_respaldo)
        btns.addWidget(self.btn_nuevo)
        self.btn_eliminar = QPushButton("Eliminar respaldo seleccionado")
        self.btn_eliminar.clicked.connect(self.eliminar_respaldo)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.tabla = TablaEstilizada(0, 4)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Fecha", "Realizado por", "Ruta archivo"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_respaldos()

    def cargar_respaldos(self):
        self.tabla.setRowCount(0)
        respaldos = obtener_respaldos()
        for r in respaldos:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(r["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(r["fecha"]))
            self.tabla.setItem(row_pos, 2, QTableWidgetItem(r["realizado_por"]))
            self.tabla.setItem(row_pos, 3, QTableWidgetItem(r["ruta_archivo"]))

    def alta_respaldo(self):
        dlg = AltaRespaldoDialog(self.user_id, self)
        if dlg.exec():
            user_id, ruta = dlg.datos()
            if not ruta:
                QMessageBox.warning(self, "Campo obligatorio", "Debes indicar la ruta del respaldo.")
                return
            ok, err = agregar_respaldo(user_id, ruta)
            if ok:
                self.cargar_respaldos()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo registrar el respaldo.\nDetalles: {err}")

    def eliminar_respaldo(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminación", "Selecciona un respaldo para eliminar.")
            return
        respaldo_id = int(self.tabla.item(row, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar este respaldo?")
        if r == QMessageBox.StandardButton.Yes:
            ok, err = eliminar_respaldo(respaldo_id)
            if ok:
                self.cargar_respaldos()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el respaldo.\nDetalles: {err}")
