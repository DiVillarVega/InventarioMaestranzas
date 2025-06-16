from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QLineEdit, QMessageBox
)
from modelos.proveedores import (
    obtener_proveedores, agregar_proveedor, editar_proveedor, eliminar_proveedor
)
from vistas.tabla_estilizada import TablaEstilizada

class ProveedorDialog(QDialog):
    def __init__(self, parent=None, proveedor=None):
        super().__init__(parent)
        self.setWindowTitle("Proveedor")
        layout = QFormLayout()

        self.input_nombre = QLineEdit(proveedor["nombre"] if proveedor else "")
        self.input_razon = QLineEdit(proveedor["razon_social"] if proveedor else "")
        self.input_rut = QLineEdit(proveedor["rut"] if proveedor else "")
        self.input_direccion = QLineEdit(proveedor["direccion"] if proveedor else "")
        self.input_telefono = QLineEdit(proveedor["telefono"] if proveedor else "")
        self.input_correo = QLineEdit(proveedor["correo"] if proveedor else "")
        self.input_productos = QLineEdit(proveedor["productos"] if proveedor else "")
        self.input_pago = QLineEdit(proveedor["condiciones_pago"] if proveedor else "")

        layout.addRow("Nombre:", self.input_nombre)
        layout.addRow("Razón social:", self.input_razon)
        layout.addRow("RUT:", self.input_rut)
        layout.addRow("Dirección:", self.input_direccion)
        layout.addRow("Teléfono:", self.input_telefono)
        layout.addRow("Correo:", self.input_correo)
        layout.addRow("Productos:", self.input_productos)
        layout.addRow("Condiciones de pago:", self.input_pago)

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
            self.input_nombre.text().strip(),
            self.input_razon.text().strip(),
            self.input_rut.text().strip(),
            self.input_direccion.text().strip(),
            self.input_telefono.text().strip(),
            self.input_correo.text().strip(),
            self.input_productos.text().strip(),
            self.input_pago.text().strip()
        )

class ProveedoresWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Proveedores")
        layout = QVBoxLayout()

        titulo = QLabel("Gestión de Proveedores")
        titulo.setStyleSheet("font-size: 18px;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_nuevo = QPushButton("Agregar proveedor")
        self.btn_nuevo.clicked.connect(self.alta_proveedor)
        btns.addWidget(self.btn_nuevo)
        self.btn_editar = QPushButton("Editar proveedor seleccionado")
        self.btn_editar.clicked.connect(self.editar_proveedor)
        btns.addWidget(self.btn_editar)
        self.btn_eliminar = QPushButton("Eliminar proveedor seleccionado")
        self.btn_eliminar.clicked.connect(self.eliminar_proveedor)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.proveedores_todos = []

        self.tabla = TablaEstilizada(0, 9)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Razón social", "RUT", "Dirección",
            "Teléfono", "Correo", "Productos", "Cond. de pago"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_proveedores()

    def cargar_proveedores(self):
        self.proveedores_todos = obtener_proveedores()
        self.mostrar_proveedores(self.proveedores_todos)

    def mostrar_proveedores(self, proveedores):
        self.tabla.setRowCount(0)
        for p in proveedores:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(p["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(p["nombre"]))
            self.tabla.setItem(row_pos, 2, QTableWidgetItem(p["razon_social"] or ""))
            self.tabla.setItem(row_pos, 3, QTableWidgetItem(p["rut"] or ""))
            self.tabla.setItem(row_pos, 4, QTableWidgetItem(p["direccion"] or ""))
            self.tabla.setItem(row_pos, 5, QTableWidgetItem(p["telefono"] or ""))
            self.tabla.setItem(row_pos, 6, QTableWidgetItem(p["correo"] or ""))
            self.tabla.setItem(row_pos, 7, QTableWidgetItem(p["productos"] or ""))
            self.tabla.setItem(row_pos, 8, QTableWidgetItem(p["condiciones_pago"] or ""))

    def alta_proveedor(self):
        dlg = ProveedorDialog(self)
        if dlg.exec():
            datos = dlg.datos()
            if not datos[0]:
                QMessageBox.warning(self, "Campo obligatorio", "El nombre es obligatorio.")
                return
            ok, err = agregar_proveedor(*datos)
            if ok:
                self.cargar_proveedores()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo agregar el proveedor.\nDetalles: {err}")

    def editar_proveedor(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Edición", "Selecciona un proveedor para editar.")
            return
        proveedor_id = int(self.tabla.item(row, 0).text())
        proveedor = {
            "nombre": self.tabla.item(row, 1).text(),
            "razon_social": self.tabla.item(row, 2).text(),
            "rut": self.tabla.item(row, 3).text(),
            "direccion": self.tabla.item(row, 4).text(),
            "telefono": self.tabla.item(row, 5).text(),
            "correo": self.tabla.item(row, 6).text(),
            "productos": self.tabla.item(row, 7).text(),
            "condiciones_pago": self.tabla.item(row, 8).text()
        }
        dlg = ProveedorDialog(self, proveedor)
        if dlg.exec():
            datos = dlg.datos()
            if not datos[0]:
                QMessageBox.warning(self, "Campo obligatorio", "El nombre es obligatorio.")
                return
            ok, err = editar_proveedor(proveedor_id, *datos)
            if ok:
                self.cargar_proveedores()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo editar el proveedor.\nDetalles: {err}")

    def eliminar_proveedor(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminación", "Selecciona un proveedor para eliminar.")
            return
        proveedor_id = int(self.tabla.item(row, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar este proveedor?")
        if r == QMessageBox.StandardButton.Yes:
            ok, err = eliminar_proveedor(proveedor_id)
            if ok:
                self.cargar_proveedores()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el proveedor.\nDetalles: {err}")
                
    def filtrar(self, texto):
        texto = texto.lower()
        proveedores_filtrados = [
            p for p in self.proveedores_todos
            if texto in p["nombre"].lower()
            or texto in (p["razon_social"] or "").lower()
            or texto in (p["rut"] or "").lower()
            or texto in (p["direccion"] or "").lower()
            or texto in (p["telefono"] or "").lower()
            or texto in (p["correo"] or "").lower()
            or texto in (p["productos"] or "").lower()
            or texto in (p["condiciones_pago"] or "").lower()
        ]
        self.mostrar_proveedores(proveedores_filtrados)
