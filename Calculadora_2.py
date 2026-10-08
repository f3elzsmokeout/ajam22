import wx
import math

class CalculadoraCientifica(wx.Frame): 

    def __init__(self):
        super().__init__(
            parent=None,
            title="Calculadora Científica",
            size=(470, 610)
        )

        self.expr = ""

        # Colores
        self.WHITE = "#ffffff"
        self.BG = "#f8f7fc"
        self.PURPLE = "#7c3aed"
        self.PURPLE_DARK = "#5b21b6"
        self.PURPLE_SOFT = "#ede9fe"
        self.PURPLE_BORDER = "#c4b5fd"
        self.TEXT = "#2a2233"
        self.MUTED = "#8b7c99"
        self.BTN = "#ffffff"

        self.SetBackgroundColour(self.BG)
        self.SetMinSize((470, 610))
        self.SetMaxSize((470, 610))

        self.create_ui()
        self.Centre()

    # ---------------------------------------------------------
    # LÓGICA DE LA CALCULADORA
    # ---------------------------------------------------------

    def update_display(self):
        self.display.SetLabel(self.expr if self.expr else "0")

    def put(self, value):
        if self.expr == "Error":
            self.expr = ""

        self.expr += value
        self.update_display()

    def clear(self, event=None):
        self.expr = ""
        self.update_display()

    def back(self, event=None):
        self.expr = self.expr[:-1]
        self.update_display()

    def safe_eval(self):
        return eval(
            self.expr,
            {"__builtins__": {}},
            {
                "pi": math.pi,
                "e": math.e
            }
        )

    def calc(self, event=None):
        try:
            self.expr = str(self.safe_eval())
        except Exception:
            self.expr = "Error"

        self.update_display()

        if self.expr == "Error":
            self.expr = ""

    def fn(self, name):
        try:
            x = float(self.safe_eval())

            if name == "sqrt":
                y = math.sqrt(x)

            elif name == "square":
                y = x ** 2

            elif name == "sin":
                y = math.sin(math.radians(x))

            elif name == "cos":
                y = math.cos(math.radians(x))

            elif name == "tan":
                y = math.tan(math.radians(x))

            elif name == "log":
                y = math.log10(x)

            elif name == "ln":
                y = math.log(x)

            elif name == "inv":
                y = 1 / x

            else:
                return

            self.expr = str(y)

        except Exception:
            self.expr = "Error"

        self.update_display()

    # ---------------------------------------------------------
    # CREACIÓN DE LA INTERFAZ
    # ---------------------------------------------------------

    def create_ui(self):

        container = wx.Panel(self)
        container.SetBackgroundColour(self.BG)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = wx.BoxSizer(wx.HORIZONTAL)

        title = wx.StaticText(
            container,
            label="Calculadora Científica"
        )

        title.SetForegroundColour(self.TEXT)
        title.SetFont(
            wx.Font(
                19,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        sci = wx.StaticText(
            container,
            label="  SCI  "
        )

        sci.SetForegroundColour(self.PURPLE_DARK)
        sci.SetBackgroundColour(self.PURPLE_SOFT)
        sci.SetFont(
            wx.Font(
                9,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        header.Add(title, 1, wx.ALIGN_CENTER_VERTICAL)
        header.Add(sci, 0, wx.ALIGN_CENTER_VERTICAL)

        main_sizer.Add(
            header,
            0,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
            18
        )

        # -----------------------------------------------------
        # DISPLAY
        # -----------------------------------------------------

        display_panel = wx.Panel(container)
        display_panel.SetBackgroundColour(self.WHITE)

        display_sizer = wx.BoxSizer(wx.VERTICAL)

        self.display = wx.StaticText(
            display_panel,
            label="0",
            style=wx.ALIGN_RIGHT
        )

        self.display.SetForegroundColour(self.TEXT)
        self.display.SetFont(
            wx.Font(
                29,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL
            )
        )

        display_sizer.Add(
            self.display,
            1,
            wx.EXPAND | wx.ALL,
            16
        )

        display_panel.SetSizer(display_sizer)

        main_sizer.Add(
            display_panel,
            0,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
            18
        )

        # -----------------------------------------------------
        # BOTONES CIENTÍFICOS
        # -----------------------------------------------------

        science = wx.GridSizer(
            rows=2,
            cols=4,
            vgap=8,
            hgap=8
        )

        scientific_buttons = [
            ("sin", lambda e: self.fn("sin")),
            ("cos", lambda e: self.fn("cos")),
            ("tan", lambda e: self.fn("tan")),
            ("log", lambda e: self.fn("log")),
            ("ln", lambda e: self.fn("ln")),
            ("√", lambda e: self.fn("sqrt")),
            ("x²", lambda e: self.fn("square")),
            ("1/x", lambda e: self.fn("inv")),
        ]

        for text, command in scientific_buttons:
            button = self.create_button(
                container,
                text,
                self.PURPLE_SOFT,
                self.PURPLE_DARK,
                self.PURPLE_BORDER
            )

            button.Bind(wx.EVT_BUTTON, command)

            science.Add(
                button,
                1,
                wx.EXPAND
            )

        main_sizer.Add(
            science,
            0,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
            18
        )

        # -----------------------------------------------------
        # TECLADO PRINCIPAL
        # -----------------------------------------------------

        keyboard = wx.GridSizer(
            rows=5,
            cols=5,
            vgap=8,
            hgap=8
        )

        buttons = [
            ("AC", self.clear, "special"),
            ("⌫", self.back, "special"),
            ("(", lambda e: self.put("("), "special"),
            (")", lambda e: self.put(")"), "special"),
            ("÷", lambda e: self.put("/"), "op"),

            ("7", lambda e: self.put("7"), "num"),
            ("8", lambda e: self.put("8"), "num"),
            ("9", lambda e: self.put("9"), "num"),
            ("π", lambda e: self.put("pi"), "special"),
            ("×", lambda e: self.put("*"), "op"),

            ("4", lambda e: self.put("4"), "num"),
            ("5", lambda e: self.put("5"), "num"),
            ("6", lambda e: self.put("6"), "num"),
            ("e", lambda e: self.put("e"), "special"),
            ("−", lambda e: self.put("-"), "op"),

            ("1", lambda e: self.put("1"), "num"),
            ("2", lambda e: self.put("2"), "num"),
            ("3", lambda e: self.put("3"), "num"),
            ("%", lambda e: self.put("%"), "special"),
            ("+", lambda e: self.put("+"), "op"),

            ("0", lambda e: self.put("0"), "num"),
            ("00", lambda e: self.put("00"), "num"),
            (".", lambda e: self.put("."), "num"),
            ("^", lambda e: self.put("**"), "special"),
            ("=", self.calc, "equal")
        ]

        for text, command, kind in buttons:

            if kind == "num":
                bg = self.BTN
                fg = self.TEXT
                border = "#ddd6fe"

            elif kind == "op":
                bg = self.PURPLE
                fg = self.WHITE
                border = self.PURPLE_DARK

            elif kind == "equal":
                bg = self.PURPLE_DARK
                fg = self.WHITE
                border = self.PURPLE_DARK

            else:
                bg = "#f5f3ff"
                fg = self.PURPLE_DARK
                border = self.PURPLE_BORDER

            button = self.create_button(
                container,
                text,
                bg,
                fg,
                border,
                font_size=13
            )

            button.Bind(wx.EVT_BUTTON, command)

            keyboard.Add(
                button,
                1,
                wx.EXPAND
            )

        main_sizer.Add(
            keyboard,
            1,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
            18
        )

        # -----------------------------------------------------
        # FIRMA
        # -----------------------------------------------------

        footer = wx.StaticText(
            container,
            label="Enrique Rojas"
        )

        footer.SetForegroundColour(self.MUTED)
        footer.SetFont(
            wx.Font(
                8,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL
            )
        )

        main_sizer.Add(
            footer,
            0,
            wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM,
            10
        )

        container.SetSizer(main_sizer)

    # ---------------------------------------------------------
    # CREAR BOTONES
    # ---------------------------------------------------------

    def create_button(
        self,
        parent,
        text,
        background,
        foreground,
        border,
        font_size=10
    ):

        button = wx.Button(
            parent,
            label=text
        )

        button.SetBackgroundColour(background)
        button.SetForegroundColour(foreground)

        button.SetFont(
            wx.Font(
                font_size,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        # El borde depende del sistema operativo/wxPython.
        # Usamos colores de fondo y texto para mantener
        # la apariencia.
        button.SetWindowStyleFlag(wx.BORDER_NONE)

        return button


class App(wx.App):

    def OnInit(self):
        frame = CalculadoraCientifica()
        frame.Show()
        return True


if __name__ == "__main__":
    app = App(False)
    app.MainLoop()