from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QLineEdit, QMessageBox
)
from modelos.respaldos import obtener_respaldos, agregar_respaldo, eliminar_respaldo
from vistas.tabla_estilizada import TablaEstilizada
from PyQt6.QtWidgets import QFileDialog
from modelos.respaldos import obtener_respaldos, agregar_respaldo, eliminar_respaldo, generar_respaldo_json
import json
from estilos import estilo_titulo, estilo_boton_general

class RespaldosWidget(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Gestión de Respaldos")
        layout = QVBoxLayout()

        titulo = QLabel("Gestión de Respaldos")
        titulo.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_nuevo = QPushButton("Registrar respaldo")
        self.btn_nuevo.setStyleSheet(estilo_boton_general)
        self.btn_nuevo.clicked.connect(self.alta_respaldo)
        btns.addWidget(self.btn_nuevo)
        self.btn_eliminar = QPushButton("Eliminar respaldo seleccionado")
        self.btn_eliminar.setStyleSheet(estilo_boton_general)
        self.btn_eliminar.clicked.connect(self.eliminar_respaldo)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.respaldos_todos = []

        self.tabla = TablaEstilizada(0, 4)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Fecha", "Realizado por", "Ruta archivo"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_respaldos()

    def cargar_respaldos(self):
        self.respaldos_todos = obtener_respaldos()
        self.mostrar_respaldos(self.respaldos_todos)

    def mostrar_respaldos(self, respaldos):
        self.tabla.setRowCount(0)
        for r in respaldos:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(r["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(r["fecha"]))
            self.tabla.setItem(row_pos, 2, QTableWidgetItem(r["realizado_por"]))
            self.tabla.setItem(row_pos, 3, QTableWidgetItem(r["ruta_archivo"]))

    def alta_respaldo(self):
        datos_json, err = generar_respaldo_json()
        if err:
            QMessageBox.critical(self, "Error", err)
            return

        # Mostrar diálogo para elegir ubicación del archivo
        ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar respaldo", "", "Archivos JSON (*.json)")
        if not ruta_archivo:
            return

        try:
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                json.dump(datos_json, f, indent=4, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo.\nDetalles: {e}")
            return

        ok, err = agregar_respaldo(self.user_id, ruta_archivo)
        if ok:
            QMessageBox.information(self, "Éxito", "Respaldo registrado correctamente.")
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
    
    def filtrar(self, texto):
        texto = texto.lower()
        respaldos_filtrados = [
            r for r in self.respaldos_todos
            if texto in (r["fecha"] or "").lower()
            or texto in (r["realizado_por"] or "").lower()
            or texto in (r["ruta_archivo"] or "").lower()
        ]
        self.mostrar_respaldos(respaldos_filtrados)
