from PyQt6.QtWidgets import ( 
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidgetItem, 
    QHeaderView, QDialog, QFormLayout, QComboBox, QMessageBox
)
from modelos.ordenes_compra import obtener_ordenes, agregar_orden, editar_estado_orden, eliminar_orden
from vistas.tabla_estilizada import TablaEstilizada

ESTADOS = ['pendiente', 'enviada', 'recibida', 'cancelada']

class OrdenesCompraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Órdenes de Compra")
        layout = QVBoxLayout()

        titulo = QLabel("Órdenes de Compra")
        titulo.setStyleSheet("font-size: 18px;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        self.btn_nueva = QPushButton("Crear orden")
        self.btn_nueva.clicked.connect(self.crear_orden)
        btns.addWidget(self.btn_nueva)
        self.btn_eliminar = QPushButton("Eliminar orden seleccionada")
        self.btn_eliminar.clicked.connect(self.eliminar_orden)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.ordenes_todas = []

        self.tabla = TablaEstilizada(0, 6)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Cliente", "Proveedor", "Fecha", "Estado", "Creado por"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_ordenes()

    def cargar_ordenes(self):
        self.ordenes_todas = obtener_ordenes()
        self.mostrar_ordenes(self.ordenes_todas)

    def mostrar_ordenes(self, ordenes):
        self.tabla.setRowCount(0)
        for o in ordenes:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)
            self.tabla.setItem(row_pos, 0, QTableWidgetItem(str(o["id"])))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(o["cliente"]))
            self.tabla.setItem(row_pos, 2, QTableWidgetItem(o["proveedor"]))
            self.tabla.setItem(row_pos, 3, QTableWidgetItem(o["fecha"]))
            self.tabla.setItem(row_pos, 4, QTableWidgetItem(o["estado"]))
            self.tabla.setItem(row_pos, 5, QTableWidgetItem(o["creado_por"]))

    def crear_orden(self):
        # Placeholder para el formulario de alta de orden
        QMessageBox.information(self, "Crear orden", "Funcionalidad en construcción.")

    def eliminar_orden(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminación", "Selecciona una orden para eliminar.")
            return
        orden_id = int(self.tabla.item(row, 0).text())
        r = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar esta orden?")
        if r == QMessageBox.StandardButton.Yes:
            ok, err = eliminar_orden(orden_id)
            if ok:
                self.cargar_ordenes()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar la orden.\nDetalles: {err}")
                
    def filtrar(self, texto):
        texto = texto.lower()
        ordenes_filtradas = [
            o for o in self.ordenes_todas
            if texto in str(o["id"])
            or texto in (o["cliente"] or "").lower()
            or texto in (o["proveedor"] or "").lower()
            or texto in (o["fecha"] or "").lower()
            or texto in (o["estado"] or "").lower()
            or texto in (o["creado_por"] or "").lower()
        ]
        self.mostrar_ordenes(ordenes_filtradas)
