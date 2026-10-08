import wx
import json
from pathlib import Path

APP_DIR = Path.home() / ".inventario_enrique"
APP_DIR.mkdir(exist_ok=True)
DATA_FILE = APP_DIR / "inventario.json"


def cargar():
    try:
        if DATA_FILE.exists():
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return []


def guardar():
    DATA_FILE.write_text(
        json.dumps(inventario, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


class InventarioFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            None,
            title="Sistema de Registro de Inventario",
            size=(1020, 620),
            style=wx.DEFAULT_FRAME_STYLE
        )

        self.SetMinSize((880, 540))

        # Colores
        self.BG = wx.Colour("#f4fbff")
        self.WHITE = wx.Colour("#ffffff")
        self.BLUE = wx.Colour("#5cc8ff")
        self.BLUE_DARK = wx.Colour("#218fca")
        self.BLUE_SOFT = wx.Colour("#dff4ff")
        self.LIME = wx.Colour("#b7f34a")
        self.LIME_DARK = wx.Colour("#79b91d")
        self.LIME_SOFT = wx.Colour("#efffd2")
        self.TEXT = wx.Colour("#203040")
        self.MUTED = wx.Colour("#718395")
        self.BORDER = wx.Colour("#cbe7f3")

        self.SetBackgroundColour(self.BG)

        self.inventario = cargar()

        self.crear_interfaz()
        self.refrescar()

        # Tecla Delete
        self.Bind(wx.EVT_CHAR_HOOK, self.on_tecla)

        self.Centre()

    def crear_interfaz(self):

        # =========================================================
        # BARRA SUPERIOR
        # =========================================================

        top = wx.Panel(self)
        top.SetBackgroundColour(self.WHITE)

        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        titulo = wx.StaticText(
            top,
            label="Sistema de Registro de Inventario"
        )
        titulo.SetForegroundColour(self.TEXT)
        titulo.SetFont(
            wx.Font(
                21,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        badge = wx.StaticText(
            top,
            label="● ACTIVO"
        )
        badge.SetBackgroundColour(self.LIME_SOFT)
        badge.SetForegroundColour(self.LIME_DARK)
        badge.SetFont(
            wx.Font(
                9,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        top_sizer.Add(titulo, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 26)
        top_sizer.AddStretchSpacer()
        top_sizer.Add(
            badge,
            0,
            wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP | wx.BOTTOM,
            20
        )

        top.SetSizer(top_sizer)

        # =========================================================
        # CUERPO PRINCIPAL
        # =========================================================

        body = wx.Panel(self)
        body.SetBackgroundColour(self.BG)

        body_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # =========================================================
        # COLUMNA IZQUIERDA
        # =========================================================

        left = wx.Panel(body)
        left.SetBackgroundColour(self.WHITE)

        left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Barra verde superior
        barra = wx.Panel(left)
        barra.SetBackgroundColour(self.LIME)
        barra.SetMinSize((-1, 8))

        left_sizer.Add(barra, 0, wx.EXPAND)

        nuevo = wx.StaticText(
            left,
            label="Nuevo producto"
        )
        nuevo.SetForegroundColour(self.TEXT)
        nuevo.SetFont(
            wx.Font(
                17,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        left_sizer.Add(
            nuevo,
            0,
            wx.LEFT | wx.RIGHT | wx.TOP,
            22
        )

        descripcion = wx.StaticText(
            left,
            label="Agrega información al inventario."
        )
        descripcion.SetForegroundColour(self.MUTED)
        descripcion.SetFont(
            wx.Font(
                9,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL
            )
        )

        left_sizer.Add(
            descripcion,
            0,
            wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM,
            22
        )

        # Formulario
        form = wx.Panel(left)
        form.SetBackgroundColour(self.WHITE)

        form_sizer = wx.BoxSizer(wx.VERTICAL)

        # Producto
        lbl = self.crear_label(form, "Producto")
        form_sizer.Add(lbl, 0, wx.TOP, 9)

        self.e_producto = wx.TextCtrl(form)
        self.e_producto.SetMinSize((-1, 32))
        form_sizer.Add(self.e_producto, 0, wx.EXPAND | wx.TOP, 3)

        # Cantidad
        lbl = self.crear_label(form, "Cantidad")
        form_sizer.Add(lbl, 0, wx.TOP, 9)

        self.e_cantidad = wx.TextCtrl(form)
        self.e_cantidad.SetMinSize((-1, 32))
        form_sizer.Add(self.e_cantidad, 0, wx.EXPAND | wx.TOP, 3)

        # Precio
        lbl = self.crear_label(form, "Precio unitario")
        form_sizer.Add(lbl, 0, wx.TOP, 9)

        self.e_precio = wx.TextCtrl(form)
        self.e_precio.SetMinSize((-1, 32))
        form_sizer.Add(self.e_precio, 0, wx.EXPAND | wx.TOP, 3)

        # Botón agregar
        self.btn_agregar = wx.Button(
            form,
            label="+ Agregar producto"
        )
        self.btn_agregar.SetBackgroundColour(self.LIME)
        self.btn_agregar.SetForegroundColour(wx.Colour("#27410a"))
        self.btn_agregar.SetFont(
            wx.Font(
                10,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        form_sizer.Add(
            self.btn_agregar,
            0,
            wx.EXPAND | wx.TOP,
            22
        )

        self.btn_agregar.Bind(
            wx.EVT_BUTTON,
            self.agregar
        )

        # Botón eliminar
        self.btn_eliminar = wx.Button(
            form,
            label="Eliminar seleccionado"
        )
        self.btn_eliminar.SetBackgroundColour(self.BLUE_SOFT)
        self.btn_eliminar.SetForegroundColour(self.BLUE_DARK)
        self.btn_eliminar.SetFont(
            wx.Font(
                10,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        form_sizer.Add(
            self.btn_eliminar,
            0,
            wx.EXPAND | wx.TOP,
            8
        )

        self.btn_eliminar.Bind(
            wx.EVT_BUTTON,
            self.eliminar
        )

        form.SetSizer(form_sizer)

        left_sizer.Add(
            form,
            0,
            wx.EXPAND | wx.LEFT | wx.RIGHT,
            22
        )

        left_sizer.AddStretchSpacer()

        autor = wx.StaticText(
            left,
            label="Enrique Rojas"
        )
        autor.SetForegroundColour(wx.Colour("#a5b7c3"))
        autor.SetFont(
            wx.Font(
                8,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL
            )
        )

        left_sizer.Add(
            autor,
            0,
            wx.ALIGN_CENTER | wx.BOTTOM,
            14
        )

        left.SetSizer(left_sizer)

        # =========================================================
        # ÁREA DERECHA
        # =========================================================

        right = wx.Panel(body)
        right.SetBackgroundColour(self.BG)

        right_sizer = wx.BoxSizer(wx.VERTICAL)

        # =========================================================
        # TARJETAS
        # =========================================================

        cards = wx.Panel(right)
        cards.SetBackgroundColour(self.BG)

        cards_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_productos = self.crear_tarjeta(
            cards,
            cards_sizer,
            "PRODUCTOS",
            self.BLUE_DARK
        )

        self.lbl_unidades = self.crear_tarjeta(
            cards,
            cards_sizer,
            "UNIDADES",
            self.LIME_DARK
        )

        self.lbl_total = self.crear_tarjeta(
            cards,
            cards_sizer,
            "VALOR TOTAL",
            self.BLUE_DARK
        )

        cards.SetSizer(cards_sizer)

        right_sizer.Add(
            cards,
            0,
            wx.EXPAND | wx.BOTTOM,
            14
        )

        # =========================================================
        # TABLA
        # =========================================================

        table_card = wx.Panel(right)
        table_card.SetBackgroundColour(self.WHITE)

        table_sizer = wx.BoxSizer(wx.VERTICAL)

        header = wx.Panel(table_card)
        header.SetBackgroundColour(self.WHITE)

        header_sizer = wx.BoxSizer(wx.HORIZONTAL)

        inventario_lbl = wx.StaticText(
            header,
            label="Inventario actual"
        )
        inventario_lbl.SetForegroundColour(self.TEXT)
        inventario_lbl.SetFont(
            wx.Font(
                17,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        vista = wx.StaticText(
            header,
            label="Vista general"
        )
        vista.SetBackgroundColour(self.BLUE_SOFT)
        vista.SetForegroundColour(self.BLUE_DARK)
        vista.SetFont(
            wx.Font(
                9,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        header_sizer.Add(
            inventario_lbl,
            0,
            wx.ALIGN_CENTER_VERTICAL
        )
        header_sizer.AddStretchSpacer()
        header_sizer.Add(
            vista,
            0,
            wx.ALIGN_CENTER_VERTICAL
        )

        header.SetSizer(header_sizer)

        table_sizer.Add(
            header,
            0,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM,
            18
        )

        # Lista
        self.tabla = wx.ListCtrl(
            table_card,
            style=wx.LC_REPORT |
                  wx.LC_SINGLE_SEL |
                  wx.BORDER_NONE
        )

        self.tabla.SetBackgroundColour(self.WHITE)
        self.tabla.SetTextColour(self.TEXT)

        self.tabla.InsertColumn(
            0,
            "Producto",
            wx.LIST_FORMAT_LEFT,
            260
        )

        self.tabla.InsertColumn(
            1,
            "Cantidad",
            wx.LIST_FORMAT_LEFT,
            100
        )

        self.tabla.InsertColumn(
            2,
            "Precio",
            wx.LIST_FORMAT_LEFT,
            120
        )

        self.tabla.InsertColumn(
            3,
            "Subtotal",
            wx.LIST_FORMAT_LEFT,
            130
        )

        table_sizer.Add(
            self.tabla,
            1,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            20
        )

        table_card.SetSizer(table_sizer)

        right_sizer.Add(
            table_card,
            1,
            wx.EXPAND
        )

        right.SetSizer(right_sizer)

        # =========================================================
        # BODY
        # =========================================================

        body_sizer.Add(
            left,
            0,
            wx.EXPAND | wx.RIGHT,
            16
        )

        body_sizer.Add(
            right,
            1,
            wx.EXPAND
        )

        body.SetSizer(body_sizer)

        # =========================================================
        # SIZER PRINCIPAL
        # =========================================================

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(
            top,
            0,
            wx.EXPAND
        )

        main_sizer.Add(
            body,
            1,
            wx.EXPAND | wx.ALL,
            22
        )

        self.SetSizer(main_sizer)

    # =============================================================
    # FUNCIONES DE INTERFAZ
    # =============================================================

    def crear_label(self, parent, texto):
        label = wx.StaticText(
            parent,
            label=texto
        )

        label.SetForegroundColour(self.TEXT)
        label.SetFont(
            wx.Font(
                10,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        return label

    def crear_tarjeta(self, parent, sizer, titulo, color):

        frame = wx.Panel(parent)
        frame.SetBackgroundColour(self.WHITE)

        frame_sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(
            frame,
            label=titulo
        )
        label.SetForegroundColour(self.MUTED)
        label.SetFont(
            wx.Font(
                9,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        valor = wx.StaticText(
            frame,
            label="0"
        )
        valor.SetForegroundColour(color)
        valor.SetFont(
            wx.Font(
                20,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        frame_sizer.Add(
            label,
            0,
            wx.TOP | wx.LEFT | wx.RIGHT,
            12
        )

        frame_sizer.Add(
            valor,
            0,
            wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            4
        )

        frame.SetSizer(frame_sizer)

        sizer.Add(
            frame,
            1,
            wx.EXPAND | wx.LEFT | wx.RIGHT,
            5
        )

        return valor

    # =============================================================
    # FUNCIONES DEL INVENTARIO
    # =============================================================

    def limpiar_campos(self):
        self.e_producto.Clear()
        self.e_cantidad.Clear()
        self.e_precio.Clear()
        self.e_producto.SetFocus()

    def agregar(self, event=None):

        producto = self.e_producto.GetValue().strip()

        try:
            cantidad = int(
                self.e_cantidad.GetValue()
            )

            # Permite tanto 10.50 como 10,50
            precio_texto = self.e_precio.GetValue().replace(",", ".")
            precio = float(precio_texto)

        except ValueError:

            wx.MessageBox(
                "Cantidad y precio deben ser números.",
                "Datos inválidos",
                wx.OK | wx.ICON_WARNING
            )

            return

        if not producto or cantidad <= 0 or precio < 0:

            wx.MessageBox(
                "Completa correctamente todos los campos.",
                "Datos inválidos",
                wx.OK | wx.ICON_WARNING
            )

            return

        self.inventario.append({
            "producto": producto,
            "cantidad": cantidad,
            "precio": precio
        })

        guardar_inventario(self.inventario)

        self.limpiar_campos()
        self.refrescar()

    def eliminar(self, event=None):

        seleccionado = self.tabla.GetFirstSelected()

        if seleccionado == -1:

            wx.MessageBox(
                "Selecciona un producto para eliminar.",
                "Sin selección",
                wx.OK | wx.ICON_INFORMATION
            )

            return

        respuesta = wx.MessageBox(
            "¿Deseas eliminar el producto seleccionado?",
            "Confirmar eliminación",
            wx.YES_NO | wx.ICON_QUESTION
        )

        if respuesta != wx.YES:
            return

        self.inventario.pop(seleccionado)

        guardar_inventario(self.inventario)

        self.refrescar()

    def refrescar(self):

        self.tabla.DeleteAllItems()

        total_valor = 0
        total_unidades = 0

        for producto in self.inventario:

            cantidad = producto["cantidad"]
            precio = producto["precio"]

            subtotal = cantidad * precio

            total_valor += subtotal
            total_unidades += cantidad

            indice = self.tabla.InsertItem(
                self.tabla.GetItemCount(),
                producto["producto"]
            )

            self.tabla.SetItem(
                indice,
                1,
                str(cantidad)
            )

            self.tabla.SetItem(
                indice,
                2,
                f"Bs {precio:.2f}"
            )

            self.tabla.SetItem(
                indice,
                3,
                f"Bs {subtotal:.2f}"
            )

    def on_tecla(self, event):

        if event.GetKeyCode() == wx.WXK_DELETE:
            self.eliminar()
        else:
            event.Skip()


def guardar_inventario(datos):

    DATA_FILE.write_text(
        json.dumps(
            datos,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


# =============================================================
# INICIO DE LA APLICACIÓN
# =============================================================

if __name__ == "__main__":

    app = wx.App(False)

    frame = InventarioFrame()
    frame.Show()

    app.MainLoop()