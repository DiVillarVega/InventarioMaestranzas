from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QMessageBox
from PyQt6.QtCore import Qt
from conexion import get_connection
from vistas.dashboard import DashboardWindow
from estilos import COLOR_BARRA, COLOR_FONDO, FUENTE

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Inventario - Login")
        self.resize(900, 520)
        main_layout = QHBoxLayout(self)

        # Panel izquierdo (amarillo)
        left = QFrame()
        left.setStyleSheet(f"background: {COLOR_BARRA};")
        left.setFixedWidth(330)
        logo = QLabel("🛠️\nMAESTRANZAS\nUNIDOS S.A.")
        logo.setStyleSheet(f"font-size: 33px; font-weight: bold; color: #16202B; font-family: {FUENTE};")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vleft = QVBoxLayout(left)
        vleft.addStretch()
        vleft.addWidget(logo)
        vleft.addStretch()

        # Panel derecho (blanco, formulario)
        right = QFrame()
        right.setStyleSheet("background: white; border-top-right-radius: 22px; border-bottom-right-radius: 22px;")
        vright = QVBoxLayout(right)
        vright.addStretch()
        label = QLabel("Iniciar Sesión")
        label.setStyleSheet(f"font-size: 24px; font-weight: bold; font-family: {FUENTE}; color: {COLOR_FONDO};")
        vright.addWidget(label)
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Correo electrónico")
        self.input_email.setStyleSheet("margin-bottom: 20px;")
        vright.addWidget(self.input_email)
        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Contraseña")
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        vright.addWidget(self.input_pass)
        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.setStyleSheet(f"""
            background: {COLOR_FONDO};
            color: white;
            border-radius: 9px;
            font-size: 18px;
            font-weight: bold;
            padding: 12px 0;
            margin-top: 18px;
            font-family: {FUENTE};
        """)
        self.btn_login.clicked.connect(self.autenticar)
        vright.addWidget(self.btn_login)
        vright.addStretch()

        main_layout.addWidget(left)
        main_layout.addWidget(right)
        self.setLayout(main_layout)

    def autenticar(self):
        email = self.input_email.text()
        pwd = self.input_pass.text()
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, rol FROM trabajadores WHERE correo=%s AND password=%s", (email, pwd))
            usuario = cur.fetchone()
            conn.close()
            if usuario:
                self.hide()
                self.dashboard = DashboardWindow(usuario[0], usuario[1], usuario[2])
                self.dashboard.show()
            else:
                QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")
        else:
            QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos")
