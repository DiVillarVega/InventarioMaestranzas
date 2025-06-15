from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QLineEdit, QMessageBox
)
from modelos.clientes import (
    obtener_clientes, agregar_cliente, editar_cliente, eliminar_cliente, cambiar_password
)
from vistas.tabla_estilizada import TablaEstilizada

class ClienteDialog(QDialog):
    def __init__(self, parent=None, cliente=None, editar_password=False):
        super().__init__(parent)
        self.setWindowTitle("Cliente")
        layout = QFormLayout()

        self.input_correo = QLineEdit(cliente["correo"] if cliente else "")
        self.input_nombre = QLineEdit(cliente["nombre"] if cliente else "")

        layout.addRow("Correo:", self.input_correo)
        layout.addRow("Nombre:", self.input_nombre)

        if not cliente or editar_password:
            self.input_password = QLineEdit()
            self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
            layout.addRow("Contraseña:", self.input_password)
        else:
            self.input_password = None

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
        correo = self.input_correo.text().strip()
        nombre = self.input_nombre.text().strip()
        password = self.input_password.text().strip() if self.input_password else None
        return correo, nombre, password

class ClientesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Clientes")
        layout = QVBoxLayout()

        titulo = QLabel("Gestión de Clientes")
        titulo.setStyleSheet("font-size: 18px;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_nuevo = QPushButton("Agregar cliente")
        self.btn_nuevo.clicked.connect(self.alta_cliente)
        btns.addWidget(self.btn_nuevo)
        self.btn_editar = QPushButton("Editar cliente seleccionado")
        self.btn_editar.clicked.connect(self.editar_cliente)
        btns.addWidget(self.btn_editar)
        self.btn_password = QPushButton("Cambiar contraseña")
        self.btn_password.clicked.connect(self.cambiar_password)
        btns.addWidget(self.btn_password)
        self.btn_eliminar = QPushButton("Eliminar cliente seleccionado")
        self.btn_eliminar.clicked.connect(self.eliminar_cliente)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.tabla = TablaEstilizada(0, 3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Correo", "Nombre"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_clientes()

    def cargar_clientes(self):
        self.tabla.setRowCount(0)
        clientes = obtener_clientes()
        for cliente in clientes:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(cliente["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(cliente["correo"]))
            self.tabla.setItem(row_pos, 2, QTableWidgetItem(cliente["nombre"]))

    def alta_cliente(self):
        dlg = ClienteDialog(self)
        if dlg.exec():
            correo, nombre, password = dlg.datos()
            if not correo or not nombre or not password:
                QMessageBox.warning(self, "Campos obligatorios", "Completa todos los campos.")
                return
            ok, err = agregar_cliente(correo, password, nombre)
            if ok:
                self.cargar_clientes()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo agregar el cliente.\nDetalles: {err}")

    def editar_cliente(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Edición", "Selecciona un cliente para editar.")
            return
        cliente_id = int(self.tabla.item(row, 0).text())
        cliente = {
            "correo": self.tabla.item(row, 1).text(),
            "nombre": self.tabla.item(row, 2).text()
        }
        dlg = ClienteDialog(self, cliente)
        if dlg.exec():
            correo, nombre, _ = dlg.datos()
            if not correo or not nombre:
                QMessageBox.warning(self, "Campos obligatorios", "Completa todos los campos.")
                return
            ok, err = editar_cliente(cliente_id, correo, nombre)
            if ok:
                self.cargar_clientes()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo editar el cliente.\nDetalles: {err}")

    def cambiar_password(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Contraseña", "Selecciona un cliente para cambiar contraseña.")
            return
        cliente_id = int(self.tabla.item(row, 0).text())
        cliente = {
            "correo": self.tabla.item(row, 1).text(),
            "nombre": self.tabla.item(row, 2).text()
        }
        dlg = ClienteDialog(self, cliente, editar_password=True)
        if dlg.exec():
            _, _, password = dlg.datos()
            if not password:
                QMessageBox.warning(self, "Contraseña", "Debes ingresar la nueva contraseña.")
                return
            ok, err = cambiar_password(cliente_id, password)
            if ok:
                QMessageBox.information(self, "Contraseña", "Contraseña cambiada correctamente.")
            else:
                QMessageBox.critical(self, "Error", f"No se pudo cambiar la contraseña.\nDetalles: {err}")

    def eliminar_cliente(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminación", "Selecciona un cliente para eliminar.")
            return
        cliente_id = int(self.tabla.item(row, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar este cliente?")
        if r == QMessageBox.StandardButton.Yes:
            ok, err = eliminar_cliente(cliente_id)
            if ok:
                self.cargar_clientes()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el cliente.\nDetalles: {err}")
