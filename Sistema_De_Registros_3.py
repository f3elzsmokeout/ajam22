import sys
import json
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QFrame,
    QStackedWidget,
    QAbstractItemView,
)


# ============================================================
# ARCHIVOS
# ============================================================

APP_DIR = Path.home() / ".sistema_registro_estudiantes"
APP_DIR.mkdir(exist_ok=True)

DATA_FILE = APP_DIR / "datos.json"


def cargar():
    try:
        if DATA_FILE.exists():
            return json.loads(
                DATA_FILE.read_text(encoding="utf-8")
            )
    except Exception:
        pass

    return []


# ============================================================
# VENTANA PRINCIPAL
# ============================================================

class SistemaRegistro(QMainWindow):

    def __init__(self):
        super().__init__()

        self.datos = cargar()

        self.setWindowTitle("Sistema de Registro de Estudiantes")
        self.setMinimumSize(880, 530)
        self.resize(1040, 610)

        # Colores
        self.BG = "#08090d"
        self.PANEL = "#12141b"
        self.PANEL_2 = "#181b24"
        self.PURPLE = "#8b5cf6"
        self.PURPLE_DARK = "#6d3fdb"
        self.PURPLE_SOFT = "#241a3a"
        self.CYAN = "#59d8ff"
        self.CYAN_SOFT = "#15303a"
        self.TEXT = "#f5f7fb"
        self.MUTED = "#8e97a8"
        self.BORDER = "#59d8ff"

        self.setStyleSheet(
            f"QMainWindow {{ background-color: {self.BG}; }}"
        )

        self.crear_interfaz()
        self.crear_atajos()

        self.mostrar("inicio")

    # ========================================================
    # INTERFAZ PRINCIPAL
    # ========================================================

    def crear_interfaz(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ----------------------------------------------------
        # BARRA LATERAL
        # ----------------------------------------------------

        side = QFrame()
        side.setFixedWidth(250)

        side.setStyleSheet(f"""
            QFrame {{
                background-color: {self.PANEL};
                border-right: 1px solid {self.CYAN};
            }}
        """)

        side_layout = QVBoxLayout(side)
        side_layout.setContentsMargins(16, 25, 16, 16)
        side_layout.setSpacing(8)

        titulo = QLabel(
            "Sistema de Registro\n"
            "de Estudiantes"
        )

        titulo.setFont(
            QFont("Segoe UI", 17, QFont.Weight.Bold)
        )

        titulo.setStyleSheet(
            f"color: {self.TEXT}; border: none;"
        )

        side_layout.addWidget(titulo)

        menu_label = QLabel("Menú principal")
        menu_label.setFont(
            QFont("Segoe UI", 9, QFont.Weight.Bold)
        )

        menu_label.setStyleSheet(
            f"color: {self.CYAN}; border: none;"
        )

        side_layout.addWidget(menu_label)
        side_layout.addSpacing(10)

        # Botones del menú
        btn_inicio = self.crear_boton_menu(
            "Inicio            Alt+1",
            lambda: self.mostrar("inicio")
        )

        btn_registro = self.crear_boton_menu(
            "Nuevo registro   Alt+2",
            lambda: self.mostrar("registro")
        )

        btn_listado = self.crear_boton_menu(
            "Listado          Alt+3",
            lambda: self.mostrar("listado")
        )

        side_layout.addWidget(btn_inicio)
        side_layout.addWidget(btn_registro)
        side_layout.addWidget(btn_listado)

        side_layout.addStretch()

        autor = QLabel("Enrique Rojas")
        autor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        autor.setFont(QFont("Segoe UI", 8))

        autor.setStyleSheet(
            f"color: {self.MUTED}; border: none;"
        )

        side_layout.addWidget(autor)

        main_layout.addWidget(side)

        # ----------------------------------------------------
        # CONTENIDO
        # ----------------------------------------------------

        self.stack = QStackedWidget()

        self.stack.setStyleSheet(
            f"background-color: {self.BG};"
        )

        main_layout.addWidget(self.stack)

        # Crear vistas
        self.inicio = self.crear_inicio()
        self.registro = self.crear_registro()
        self.listado = self.crear_listado()

        self.stack.addWidget(self.inicio)
        self.stack.addWidget(self.registro)
        self.stack.addWidget(self.listado)

    # ========================================================
    # BOTÓN MENÚ
    # ========================================================

    def crear_boton_menu(self, texto, comando):

        boton = QPushButton(texto)

        boton.setMinimumHeight(43)
        boton.setCursor(Qt.CursorShape.PointingHandCursor)

        boton.clicked.connect(comando)

        boton.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.PANEL_2};
                color: {self.TEXT};
                border: 1px solid {self.CYAN};
                border-radius: 4px;
                text-align: left;
                padding-left: 16px;
                font-family: "Segoe UI";
                font-size: 10pt;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: {self.PURPLE_SOFT};
                color: {self.CYAN};
            }}

            QPushButton:pressed {{
                background-color: {self.PURPLE_DARK};
                color: white;
            }}
        """)

        return boton

    # ========================================================
    # CREAR TARJETA
    # ========================================================

    def crear_panel(self):

        exterior = QWidget()

        layout = QVBoxLayout(exterior)
        layout.setContentsMargins(26, 26, 26, 26)

        tarjeta = QFrame()

        tarjeta.setStyleSheet(f"""
            QFrame {{
                background-color: {self.PANEL};
                border: 1px solid {self.CYAN};
                border-radius: 3px;
            }}
        """)

        layout.addWidget(tarjeta)

        return exterior, tarjeta

    # ========================================================
    # INICIO
    # ========================================================

    def crear_inicio(self):

        exterior, card = self.crear_panel()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 28, 28, 28)

        titulo = QLabel("Panel principal")

        titulo.setFont(
            QFont("Segoe UI", 23, QFont.Weight.Bold)
        )

        titulo.setStyleSheet(
            f"color: {self.TEXT}; border: none;"
        )

        layout.addWidget(titulo)

        descripcion = QLabel(
            "Administra los registros de estudiantes "
            "desde un solo lugar."
        )

        descripcion.setFont(QFont("Segoe UI", 10))

        descripcion.setStyleSheet(
            f"color: {self.MUTED}; border: none;"
        )

        layout.addWidget(descripcion)

        # Resumen
        resumen = QFrame()

        resumen.setFixedWidth(250)

        resumen.setStyleSheet(f"""
            QFrame {{
                background-color: {self.PURPLE_SOFT};
                border: 1px solid {self.CYAN};
                border-radius: 3px;
            }}
        """)

        resumen_layout = QVBoxLayout(resumen)
        resumen_layout.setContentsMargins(18, 14, 18, 14)

        label_total = QLabel("TOTAL DE REGISTROS")

        label_total.setFont(
            QFont("Segoe UI", 9, QFont.Weight.Bold)
        )

        label_total.setStyleSheet(
            f"color: {self.CYAN}; border: none;"
        )

        resumen_layout.addWidget(label_total)

        self.lbl_total = QLabel("0")

        self.lbl_total.setFont(
            QFont("Segoe UI", 26, QFont.Weight.Bold)
        )

        self.lbl_total.setStyleSheet(
            f"color: {self.PURPLE}; border: none;"
        )

        resumen_layout.addWidget(self.lbl_total)

        layout.addSpacing(25)
        layout.addWidget(resumen, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addStretch()

        return exterior

    # ========================================================
    # REGISTRO
    # ========================================================

    def crear_registro(self):

        exterior, card = self.crear_panel()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 28, 28, 28)

        titulo = QLabel("Registrar estudiante")

        titulo.setFont(
            QFont("Segoe UI", 23, QFont.Weight.Bold)
        )

        titulo.setStyleSheet(
            f"color: {self.TEXT}; border: none;"
        )

        layout.addWidget(titulo)
        layout.addSpacing(10)

        form = QWidget()

        form_layout = QVBoxLayout(form)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(5)

        self.e_nombre = self.crear_campo(
            form_layout,
            "Nombre completo"
        )

        self.e_curso = self.crear_campo(
            form_layout,
            "Curso"
        )

        self.e_telefono = self.crear_campo(
            form_layout,
            "Teléfono"
        )

        self.e_nota = self.crear_campo(
            form_layout,
            "Nota"
        )

        boton_guardar = QPushButton(
            "Guardar estudiante"
        )

        boton_guardar.setFixedWidth(190)
        boton_guardar.setFixedHeight(42)
        boton_guardar.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        boton_guardar.clicked.connect(self.guardar)

        boton_guardar.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.PURPLE};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 9px;
                font-family: "Segoe UI";
                font-size: 10pt;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: {self.PURPLE_DARK};
            }}
        """)

        form_layout.addSpacing(10)
        form_layout.addWidget(boton_guardar)

        layout.addWidget(form)
        layout.addStretch()

        return exterior

    # ========================================================
    # CAMPOS
    # ========================================================

    def crear_campo(self, layout, texto):

        label = QLabel(texto)

        label.setFont(
            QFont("Segoe UI", 10, QFont.Weight.Bold)
        )

        label.setStyleSheet(
            f"color: {self.CYAN}; border: none;"
        )

        layout.addWidget(label)

        entry = QLineEdit()

        entry.setFixedWidth(430)
        entry.setFixedHeight(34)

        entry.setFont(QFont("Segoe UI", 10))

        entry.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.PANEL_2};
                color: {self.TEXT};
                border: 1px solid #303644;
                border-radius: 3px;
                padding: 5px 8px;
            }}

            QLineEdit:focus {{
                border: 1px solid {self.CYAN};
            }}
        """)

        layout.addWidget(entry)
        layout.addSpacing(6)

        return entry

    # ========================================================
    # LISTADO
    # ========================================================

    def crear_listado(self):

        exterior, card = self.crear_panel()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 28, 28, 28)

        # Parte superior
        top = QHBoxLayout()

        titulo = QLabel("Listado de estudiantes")

        titulo.setFont(
            QFont("Segoe UI", 23, QFont.Weight.Bold)
        )

        titulo.setStyleSheet(
            f"color: {self.TEXT}; border: none;"
        )

        top.addWidget(titulo)
        top.addStretch()

        # Botón eliminar
        btn_eliminar = QPushButton(
            "Eliminar seleccionado"
        )

        btn_eliminar.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        btn_eliminar.clicked.connect(
            self.eliminar_seleccionado
        )

        btn_eliminar.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.CYAN_SOFT};
                color: {self.CYAN};
                border: none;
                border-radius: 4px;
                padding: 9px;
                font-family: "Segoe UI";
                font-size: 10pt;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: #1c4452;
            }}
        """)

        top.addWidget(btn_eliminar)

        # Botón vaciar
        btn_vaciar = QPushButton("Vaciar lista")

        btn_vaciar.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        btn_vaciar.clicked.connect(
            self.vaciar_lista
        )

        btn_vaciar.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.PURPLE};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 9px;
                font-family: "Segoe UI";
                font-size: 10pt;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: {self.PURPLE_DARK};
            }}
        """)

        top.addWidget(btn_vaciar)

        layout.addLayout(top)
        layout.addSpacing(10)

        # ----------------------------------------------------
        # TABLA
        # ----------------------------------------------------

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(4)

        self.tabla.setHorizontalHeaderLabels([
            "Nombre",
            "Curso",
            "Teléfono",
            "Nota"
        ])

        self.tabla.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.tabla.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.tabla.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.tabla.setAlternatingRowColors(False)

        self.tabla.verticalHeader().setVisible(False)

        header = self.tabla.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.Stretch
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Stretch
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.Stretch
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.tabla.setStyleSheet(f"""
            QTableWidget {{
                background-color: {self.PANEL_2};
                color: {self.TEXT};
                border: 1px solid {self.CYAN};
                gridline-color: #303644;
                font-family: "Segoe UI";
                font-size: 10pt;
                selection-background-color: {self.PURPLE_DARK};
                selection-color: white;
            }}

            QHeaderView::section {{
                background-color: {self.PURPLE_DARK};
                color: white;
                padding: 8px;
                border: none;
                font-family: "Segoe UI";
                font-size: 10pt;
                font-weight: bold;
            }}

            QTableWidget::item {{
                padding: 6px;
                border-bottom: 1px solid #252936;
            }}
        """)

        layout.addWidget(self.tabla)

        return exterior

    # ========================================================
    # MOSTRAR VISTA
    # ========================================================

    def mostrar(self, nombre):

        indices = {
            "inicio": 0,
            "registro": 1,
            "listado": 2
        }

        self.stack.setCurrentIndex(indices[nombre])

        self.refrescar()

    # ========================================================
    # GUARDAR
    # ========================================================

    def guardar(self):

        nombre = self.e_nombre.text().strip()
        curso = self.e_curso.text().strip()
        telefono = self.e_telefono.text().strip()
        nota = self.e_nota.text().strip()

        if not nombre:
            QMessageBox.warning(
                self,
                "Falta información",
                "Ingresa el nombre del estudiante."
            )
            return

        self.datos.append({
            "nombre": nombre,
            "curso": curso,
            "telefono": telefono,
            "nota": nota
        })

        self.guardar_archivo()

        # Limpiar campos
        self.e_nombre.clear()
        self.e_curso.clear()
        self.e_telefono.clear()
        self.e_nota.clear()

        self.mostrar("listado")

    # ========================================================
    # GUARDAR JSON
    # ========================================================

    def guardar_archivo(self):

        try:
            DATA_FILE.write_text(
                json.dumps(
                    self.datos,
                    ensure_ascii=False,
                    indent=2
                ),
                encoding="utf-8"
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo guardar el archivo:\n{error}"
            )

    # ========================================================
    # ELIMINAR
    # ========================================================

    def eliminar_seleccionado(self):

        fila = self.tabla.currentRow()

        if fila < 0:

            QMessageBox.information(
                self,
                "Sin selección",
                "Selecciona un estudiante de la lista."
            )

            return

        respuesta = QMessageBox.question(
            self,
            "Eliminar registro",
            "¿Deseas eliminar el registro seleccionado?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if respuesta != QMessageBox.StandardButton.Yes:
            return

        if fila < len(self.datos):

            self.datos.pop(fila)

            self.guardar_archivo()
            self.refrescar()

    # ========================================================
    # VACIAR LISTA
    # ========================================================

    def vaciar_lista(self):

        if not self.datos:

            QMessageBox.information(
                self,
                "Lista vacía",
                "No hay registros para eliminar."
            )

            return

        respuesta = QMessageBox.question(
            self,
            "Vaciar lista",
            "¿Seguro que deseas eliminar todos los registros?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if respuesta != QMessageBox.StandardButton.Yes:
            return

        self.datos.clear()

        self.guardar_archivo()
        self.refrescar()

    # ========================================================
    # ACTUALIZAR TABLA
    # ========================================================

    def refrescar(self):

        # Total
        if hasattr(self, "lbl_total"):
            self.lbl_total.setText(
                str(len(self.datos))
            )

        # Tabla
        if not hasattr(self, "tabla"):
            return

        self.tabla.setRowCount(0)

        for d in self.datos:

            fila = self.tabla.rowCount()

            self.tabla.insertRow(fila)

            valores = [
                d.get("nombre", ""),
                d.get("curso", ""),
                d.get("telefono", ""),
                d.get("nota", "")
            ]

            for columna, valor in enumerate(valores):

                item = QTableWidgetItem(str(valor))

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignVCenter |
                    Qt.AlignmentFlag.AlignLeft
                )

                self.tabla.setItem(
                    fila,
                    columna,
                    item
                )

    # ========================================================
    # ATAJOS
    # ========================================================

    def crear_atajos(self):

        # Alt + 1
        self.shortcut_inicio = QShortcut(
            QKeySequence("Alt+1"),
            self
        )

        self.shortcut_inicio.activated.connect(
            lambda: self.mostrar("inicio")
        )

        # Alt + 2
        self.shortcut_registro = QShortcut(
            QKeySequence("Alt+2"),
            self
        )

        self.shortcut_registro.activated.connect(
            lambda: self.mostrar("registro")
        )

        # Alt + 3
        self.shortcut_listado = QShortcut(
            QKeySequence("Alt+3"),
            self
        )

        self.shortcut_listado.activated.connect(
            lambda: self.mostrar("listado")
        )

        # Delete
        self.shortcut_delete = QShortcut(
            QKeySequence(Qt.Key.Key_Delete),
            self
        )

        self.shortcut_delete.activated.connect(
            self.eliminar_seleccionado
        )


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setApplicationName(
        "Sistema de Registro de Estudiantes"
    )

    ventana = SistemaRegistro()
    ventana.show()

    sys.exit(app.exec())