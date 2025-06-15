import sys
from PyQt6.QtWidgets import QApplication
from vistas.login import LoginWindow
from config import AUTOLOGIN, AUTOLOGIN_USER

if __name__ == "__main__":
    app = QApplication(sys.argv)
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
