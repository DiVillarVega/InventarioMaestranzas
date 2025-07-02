from PyQt6.QtWidgets import QTableWidget

class TablaEstilizada(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""
            QTableWidget {
                background: white;
                color: black;           
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
            QTableWidget::item:selected {
                background-color: #444a58;
                color: white;
            }
            QTableWidget::item:!active:selected {
                background-color: #3a3f4b;
                color: white;
            }                           
        """)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # <-- ESTA LÍNEA HACE TODAS LAS CELDAS NO EDITABLES
