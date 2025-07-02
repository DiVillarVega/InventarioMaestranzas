import sys
from PyQt6.QtWidgets import QApplication
from vistas.login import LoginWindow
from config import AUTOLOGIN, AUTOLOGIN_USER

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QWidget {
            background-color: #16202b;
            color: white;
            font-family: Segoe UI, Arial, sans-serif;
        }
        QPushButton {
            background-color: #ba846c;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #a46f5c;
        }
        QPushButton:pressed {
            background-color: #8e5f50;
        }
        QLineEdit, QComboBox, QTextEdit {
            background-color: #2c3a44;
            color: white;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 4px;
        }
        QTableWidget {
            background-color: #16202b;
            color: white;
            gridline-color: #3a4a58;
            font-family: Segoe UI, Arial, sans-serif;
        }
        QHeaderView::section {
            background-color: #ba846c;
            color: white;
            font-weight: bold;
            border: none;
            padding: 8px 0;
        }
        QMessageBox {
            background-color: #16202b;
            color: white;
            font-family: Segoe UI, Arial, sans-serif;
        }
        QMessageBox QPushButton {
            background-color: #ba846c;
            color: white;
            border-radius: 5px;
            padding: 5px 15px;
            min-width: 70px;
            font-weight: bold;
        }
        QMessageBox QPushButton:hover {
            background-color: #a46f5c;
        }
        QMessageBox QPushButton:pressed {
            background-color: #8e5f50;
        }
    """)

    if AUTOLOGIN:
        # Importar el dashboard directamente
        from conexion import get_connection
        conn = get_connection()
        user = None
        if conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, nombre, rol FROM trabajadores WHERE correo=%s AND password=%s",
                (AUTOLOGIN_USER["correo"], AUTOLOGIN_USER["password"])
            )
            user = cur.fetchone()
            conn.close()
        if user:
            from vistas.dashboard import DashboardWindow
            window = DashboardWindow(user[0], user[1], user[2])
        else:
            window = LoginWindow()
    else:
        window = LoginWindow()
    window.show()
    sys.exit(app.exec())
