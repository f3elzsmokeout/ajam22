import sys
import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
)


class Calculadora(QWidget):

    def __init__(self):
        super().__init__()

        self.expr = ""
        self.scientific_mode = False

        # Colores
        self.PINK = "#ff4fa3"
        self.PINK_DARK = "#d93687"
        self.PINK_SOFT = "#2a1220"
        self.BLACK = "#090909"
        self.PANEL = "#151515"
        self.BUTTON = "#222222"
        self.TEXT = "#ffffff"
        self.MUTED = "#9b7d8b"

        self.setWindowTitle("Calculadora Multifunción")
        self.setFixedSize(430, 650)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.BLACK};
                color: {self.TEXT};
                font-family: "Segoe UI";
            }}
        """)

        self.crear_interfaz()

        # Atajo F2
        self.shortcut_f2 = QShortcut(
            QKeySequence("F2"),
            self
        )
        self.shortcut_f2.activated.connect(
            self.toggle_mode
        )

    # =========================================================
    # LÓGICA
    # =========================================================

    def update_display(self):
        self.display.setText(
            self.expr if self.expr else "0"
        )

    def add(self, value):
        if self.expr == "Error":
            self.expr = ""

        self.expr += value
        self.update_display()

    def clear(self):
        self.expr = ""
        self.update_display()

    def back(self):
        self.expr = self.expr[:-1]
        self.update_display()

    def safe_eval(self):
        allowed = {
            "pi": math.pi,
            "e": math.e
        }

        return eval(
            self.expr,
            {"__builtins__": {}},
            allowed
        )

    def calculate(self):
        try:
            self.expr = str(
                self.safe_eval()
            )
        except Exception:
            self.expr = "Error"

        self.update_display()

    def scientific(self, name):

        try:
            x = float(
                self.safe_eval()
            )

            if name == "sqrt":
                result = math.sqrt(x)

            elif name == "square":
                result = x ** 2

            elif name == "cube":
                result = x ** 3

            elif name == "sin":
                result = math.sin(
                    math.radians(x)
                )

            elif name == "cos":
                result = math.cos(
                    math.radians(x)
                )

            elif name == "tan":
                result = math.tan(
                    math.radians(x)
                )

            elif name == "log":
                result = math.log10(x)

            elif name == "ln":
                result = math.log(x)

            elif name == "inv":
                result = 1 / x

            elif name == "abs":
                result = abs(x)

            else:
                return

            self.expr = str(result)

        except Exception:
            self.expr = "Error"

        self.update_display()

    # =========================================================
    # CAMBIAR MODO
    # =========================================================

    def toggle_mode(self):

        self.scientific_mode = (
            not self.scientific_mode
        )

        if self.scientific_mode:

            self.sci_frame.show()

            self.mode_label.setText(
                "Modo científico"
            )

            self.mode_button.setText(
                "Modo básico  ·  F2"
            )

        else:

            self.sci_frame.hide()

            self.mode_label.setText(
                "Modo básico"
            )

            self.mode_button.setText(
                "Modo científico  ·  F2"
            )

    # =========================================================
    # CREAR INTERFAZ
    # =========================================================

    def crear_interfaz(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            18, 18, 18, 18
        )

        main_layout.setSpacing(0)

        # -----------------------------------------------------
        # TÍTULO
        # -----------------------------------------------------

        title_layout = QHBoxLayout()

        title = QLabel(
            "Calculadora Multifunción"
        )

        title.setFont(
            QFont(
                "Segoe UI",
                18,
                QFont.Weight.Bold
            )
        )

        title.setStyleSheet(
            f"color: {self.TEXT};"
        )

        self.mode_label = QLabel(
            "Modo básico"
        )

        self.mode_label.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Bold
            )
        )

        self.mode_label.setStyleSheet(
            f"color: {self.PINK};"
        )

        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(
            self.mode_label
        )

        main_layout.addLayout(
            title_layout
        )

        # -----------------------------------------------------
        # DISPLAY
        # -----------------------------------------------------

        display_frame = QFrame()

        display_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.PANEL};
                border: 1px solid {self.PINK_DARK};
                border-radius: 2px;
            }}
        """)

        display_layout = QVBoxLayout(
            display_frame
        )

        display_layout.setContentsMargins(
            14, 14, 14, 14
        )

        self.display = QLabel("0")

        self.display.setAlignment(
            Qt.AlignmentFlag.AlignRight |
            Qt.AlignmentFlag.AlignVCenter
        )

        self.display.setFont(
            QFont(
                "Segoe UI",
                28
            )
        )

        self.display.setStyleSheet(
            f"color: {self.TEXT};"
            "border: none;"
        )

        display_layout.addWidget(
            self.display
        )

        main_layout.addSpacing(16)

        main_layout.addWidget(
            display_frame
        )

        # -----------------------------------------------------
        # BOTÓN DE MODO
        # -----------------------------------------------------

        self.mode_button = QPushButton(
            "Modo científico  ·  F2"
        )

        self.mode_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.mode_button.setFixedHeight(40)

        self.mode_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.PINK_SOFT};
                color: {self.PINK};
                border: none;
                border-radius: 4px;
                font-size: 10pt;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: #3a1729;
            }}

            QPushButton:pressed {{
                background-color: {self.PINK_DARK};
                color: white;
            }}
        """)

        self.mode_button.clicked.connect(
            self.toggle_mode
        )

        main_layout.addSpacing(10)

        main_layout.addWidget(
            self.mode_button
        )

        # -----------------------------------------------------
        # PANEL CIENTÍFICO
        # -----------------------------------------------------

        self.sci_frame = QFrame()

        self.sci_frame.setStyleSheet(
            f"background-color: {self.BLACK};"
        )

        sci_layout = QGridLayout(
            self.sci_frame
        )

        sci_layout.setContentsMargins(
            0, 10, 0, 0
        )

        sci_layout.setSpacing(6)

        scientific_buttons = [
            ("√", "sqrt"),
            ("x²", "square"),
            ("x³", "cube"),
            ("1/x", "inv"),
            ("sin", "sin"),
            ("cos", "cos"),
            ("tan", "tan"),
            ("log", "log"),
            ("ln", "ln"),
            ("|x|", "abs"),
        ]

        for i, (text, function) in enumerate(
            scientific_buttons
        ):

            button = self.create_scientific_button(
                text
            )

            button.clicked.connect(
                lambda checked=False,
                f=function:
                self.scientific(f)
            )

            sci_layout.addWidget(
                button,
                i // 5,
                i % 5
            )

        main_layout.addWidget(
            self.sci_frame
        )

        # Inicialmente oculto
        self.sci_frame.hide()

        # -----------------------------------------------------
        # TECLADO PRINCIPAL
        # -----------------------------------------------------

        keys_frame = QFrame()

        keys_layout = QGridLayout(
            keys_frame
        )

        keys_layout.setContentsMargins(
            0, 10, 0, 0
        )

        keys_layout.setSpacing(8)

        buttons = [
            ("AC", "clear", "special"),
            ("⌫", "back", "special"),
            ("(", "(", "special"),
            (")", ")", "special"),
            ("÷", "/", "op"),

            ("7", "7", "num"),
            ("8", "8", "num"),
            ("9", "9", "num"),
            ("π", "pi", "special"),
            ("×", "*", "op"),

            ("4", "4", "num"),
            ("5", "5", "num"),
            ("6", "6", "num"),
            ("e", "e", "special"),
            ("−", "-", "op"),

            ("1", "1", "num"),
            ("2", "2", "num"),
            ("3", "3", "num"),
            ("%", "%", "special"),
            ("+", "+", "op"),

            ("0", "0", "num"),
            ("00", "00", "num"),
            (".", ".", "num"),
            ("^", "**", "special"),
            ("=", "calculate", "equal"),
        ]

        for i, (text, value, kind) in enumerate(
            buttons
        ):

            button = self.create_main_button(
                text,
                kind
            )

            if value == "clear":
                button.clicked.connect(
                    self.clear
                )

            elif value == "back":
                button.clicked.connect(
                    self.back
                )

            elif value == "calculate":
                button.clicked.connect(
                    self.calculate
                )

            else:
                button.clicked.connect(
                    lambda checked=False,
                    v=value:
                    self.add(v)
                )

            keys_layout.addWidget(
                button,
                i // 5,
                i % 5
            )

        for row in range(5):
            keys_layout.setRowStretch(
                row,
                1
            )

        for col in range(5):
            keys_layout.setColumnStretch(
                col,
                1
            )

        main_layout.addWidget(
            keys_frame,
            1
        )

        # -----------------------------------------------------
        # FIRMA
        # -----------------------------------------------------

        footer = QLabel(
            "Enrique Rojas"
        )

        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        footer.setFont(
            QFont(
                "Segoe UI",
                8
            )
        )

        footer.setStyleSheet(
            f"color: {self.MUTED};"
        )

        main_layout.addWidget(
            footer
        )

    # =========================================================
    # BOTONES CIENTÍFICOS
    # =========================================================

    def create_scientific_button(
        self,
        text
    ):

        button = QPushButton(text)

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setMinimumHeight(40)

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.PINK_SOFT};
                color: {self.PINK};
                border: none;
                border-radius: 4px;
                font-size: 10pt;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: {self.PINK_DARK};
                color: white;
            }}

            QPushButton:pressed {{
                background-color: {self.PINK_DARK};
                color: white;
            }}
        """)

        return button

    # =========================================================
    # BOTONES PRINCIPALES
    # =========================================================

    def create_main_button(
        self,
        text,
        kind
    ):

        button = QPushButton(text)

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setMinimumHeight(55)

        if kind == "num":

            background = self.BUTTON
            foreground = self.TEXT
            hover = "#333333"

        elif kind == "op":

            background = self.PINK_DARK
            foreground = "white"
            hover = self.PINK

        elif kind == "equal":

            background = self.PINK
            foreground = "#16000b"
            hover = "#ff75b8"

        else:

            background = self.PINK_SOFT
            foreground = self.PINK
            hover = self.PINK_DARK

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {background};
                color: {foreground};
                border: none;
                border-radius: 4px;
                font-size: 13pt;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: {hover};
                color: white;
            }}

            QPushButton:pressed {{
                background-color: {self.PINK_DARK};
                color: white;
            }}
        """)

        return button


# =============================================================
# EJECUAR PROGRAMA
# =============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Calculadora()
    window.show()

    sys.exit(
        app.exec()
    )