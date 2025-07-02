from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QLineEdit, QMessageBox, QComboBox
)
from modelos.usuarios import (
    obtener_usuarios, agregar_usuario, editar_usuario, eliminar_usuario, cambiar_password
)
from vistas.tabla_estilizada import TablaEstilizada
from estilos import estilo_titulo, estilo_boton_general

ROLES = [
    'administrador',
    'gestor_inventario',
    'logistica',
    'produccion',
    'auditor'
]

class UsuarioDialog(QDialog):
    def __init__(self, parent=None, usuario=None, editar_password=False):
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
        self.setWindowTitle("Usuario")
        layout = QFormLayout()

        self.input_correo = QLineEdit(usuario["correo"] if usuario else "")
        self.input_nombre = QLineEdit(usuario["nombre"] if usuario else "")
        self.input_rol = QComboBox()
        self.input_rol.addItems(ROLES)
        if usuario:
            idx = ROLES.index(usuario["rol"]) if usuario["rol"] in ROLES else 0
            self.input_rol.setCurrentIndex(idx)

        layout.addRow("Correo:", self.input_correo)
        layout.addRow("Nombre:", self.input_nombre)
        layout.addRow("Rol:", self.input_rol)

        if not usuario or editar_password:
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
        rol = self.input_rol.currentText()
        password = self.input_password.text().strip() if self.input_password else None
        return correo, nombre, rol, password

class UsuariosWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Usuarios")
        layout = QVBoxLayout()

        titulo = QLabel("Gestión de Usuarios")
        titulo.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_nuevo = QPushButton("Agregar usuario")
        self.btn_nuevo.setStyleSheet(estilo_boton_general)
        self.btn_nuevo.clicked.connect(self.alta_usuario)
        btns.addWidget(self.btn_nuevo)
        self.btn_editar = QPushButton("Editar usuario seleccionado")
        self.btn_editar.setStyleSheet(estilo_boton_general)
        self.btn_editar.clicked.connect(self.editar_usuario)
        btns.addWidget(self.btn_editar)
        self.btn_password = QPushButton("Cambiar contraseña")
        self.btn_password.setStyleSheet(estilo_boton_general)
        self.btn_password.clicked.connect(self.cambiar_password)
        btns.addWidget(self.btn_password)
        self.btn_eliminar = QPushButton("Eliminar usuario seleccionado")
        self.btn_eliminar.setStyleSheet(estilo_boton_general)
        self.btn_eliminar.clicked.connect(self.eliminar_usuario)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.usuarios_todos = []

        self.tabla = TablaEstilizada(0, 4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Correo", "Nombre", "Rol"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_usuarios()

    def cargar_usuarios(self):
        self.usuarios_todos = obtener_usuarios()
        self.mostrar_usuarios(self.usuarios_todos)

    def mostrar_usuarios(self, usuarios):
        self.tabla.setRowCount(0)
        for usuario in usuarios:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(usuario["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(usuario["correo"]))
            self.tabla.setItem(row_pos, 2, QTableWidgetItem(usuario["nombre"]))
            self.tabla.setItem(row_pos, 3, QTableWidgetItem(usuario["rol"]))

    def alta_usuario(self):
        dlg = UsuarioDialog(self)
        if dlg.exec():
            correo, nombre, rol, password = dlg.datos()
            if not correo or not nombre or not rol or not password:
                QMessageBox.warning(self, "Campos obligatorios", "Completa todos los campos.")
                return
            ok, err = agregar_usuario(correo, password, nombre, rol)
            if ok:
                self.cargar_usuarios()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo agregar el usuario.\nDetalles: {err}")

    def editar_usuario(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Edición", "Selecciona un usuario para editar.")
            return
        usuario_id = int(self.tabla.item(row, 0).text())
        usuario = {
            "correo": self.tabla.item(row, 1).text(),
            "nombre": self.tabla.item(row, 2).text(),
            "rol": self.tabla.item(row, 3).text()
        }
        dlg = UsuarioDialog(self, usuario)
        if dlg.exec():
            correo, nombre, rol, _ = dlg.datos()
            if not correo or not nombre or not rol:
                QMessageBox.warning(self, "Campos obligatorios", "Completa todos los campos.")
                return
            ok, err = editar_usuario(usuario_id, correo, nombre, rol)
            if ok:
                self.cargar_usuarios()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo editar el usuario.\nDetalles: {err}")

    def cambiar_password(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Contraseña", "Selecciona un usuario para cambiar contraseña.")
            return
        usuario_id = int(self.tabla.item(row, 0).text())
        usuario = {
            "correo": self.tabla.item(row, 1).text(),
            "nombre": self.tabla.item(row, 2).text(),
            "rol": self.tabla.item(row, 3).text()
        }
        dlg = UsuarioDialog(self, usuario, editar_password=True)
        if dlg.exec():
            _, _, _, password = dlg.datos()
            if not password:
                QMessageBox.warning(self, "Contraseña", "Debes ingresar la nueva contraseña.")
                return
            ok, err = cambiar_password(usuario_id, password)
            if ok:
                QMessageBox.information(self, "Contraseña", "Contraseña cambiada correctamente.")
            else:
                QMessageBox.critical(self, "Error", f"No se pudo cambiar la contraseña.\nDetalles: {err}")

    def eliminar_usuario(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminación", "Selecciona un usuario para eliminar.")
            return
        usuario_id = int(self.tabla.item(row, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar este usuario?")
        if r == QMessageBox.StandardButton.Yes:
            ok, err = eliminar_usuario(usuario_id)
            if ok:
                self.cargar_usuarios()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el usuario.\nDetalles: {err}")
                
    def filtrar(self, texto):
        texto = texto.lower()
        usuarios_filtrados = [
            u for u in self.usuarios_todos
            if texto in u["correo"].lower()
            or texto in u["nombre"].lower()
            or texto in u["rol"].lower()
        ]
        self.mostrar_usuarios(usuarios_filtrados)
