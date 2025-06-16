from PyQt6.QtWidgets import QTableWidget

class TablaEstilizada(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""
            QTableWidget {
                background: white;
                border-radius: 12px;
                font-size: 15px;
                font-family: Segoe UI;
            }
            QHeaderView::section {
                background-color: #F7B500;
                color: #16202B;
                font-weight: bold;
                font-size: 16px;
                border: none;
                padding: 8px 0;
            }
            QTableWidget::item {
                padding: 7px;
            }
            QTableCornerButton::section {
                background-color: #F7B500;
            }
        """)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # <-- ESTA LÍNEA HACE TODAS LAS CELDAS NO EDITABLES
