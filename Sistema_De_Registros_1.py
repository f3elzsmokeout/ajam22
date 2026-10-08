import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

APP_DIR = Path.home() / ".registro_personas_enrique"
APP_DIR.mkdir(exist_ok=True)
DATA_FILE = APP_DIR / "datos.json"

def cargar():
    try:
        if DATA_FILE.exists():
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except:
        pass
    return []

def guardar_archivo():
    DATA_FILE.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def agregar():
    nombre = e_nombre.get().strip()
    edad = e_edad.get().strip()
    ciudad = e_ciudad.get().strip()
    estado = cb_estado.get()

    if not nombre or not edad:
        messagebox.showwarning("Faltan datos", "Completa el nombre y la edad.")
        return

    datos.append({
        "nombre": nombre,
        "edad": edad,
        "ciudad": ciudad,
        "estado": estado
    })

    guardar_archivo()

    e_nombre.delete(0, tk.END)
    e_edad.delete(0, tk.END)
    e_ciudad.delete(0, tk.END)
    cb_estado.set("Activo")
    refrescar()

def eliminar():
    sel = tabla.selection()

    if not sel:
        messagebox.showinfo(
            "Sin selección",
            "Selecciona un registro para eliminar."
        )
        return

    if not messagebox.askyesno(
        "Confirmar",
        "¿Deseas eliminar el registro seleccionado?"
    ):
        return

    indice = tabla.index(sel[0])
    datos.pop(indice)
    guardar_archivo()
    refrescar()

def refrescar():
    for item in tabla.get_children():
        tabla.delete(item)

    for d in datos:
        tabla.insert(
            "",
            "end",
            values=(
                d.get("nombre", ""),
                d.get("edad", ""),
                d.get("ciudad", ""),
                d.get("estado", "")
            )
        )

    lbl_total.config(text=f"Total de registros: {len(datos)}")

root = tk.Tk()
root.title("Sistema de Registro de Personas")
root.geometry("980x570")
root.minsize(820, 500)

BG = "#f7f8fc"
WHITE = "#ffffff"
NAVY = "#13203a"
NAVY_2 = "#1c2f54"
PURPLE = "#7451d6"
PURPLE_DARK = "#5837b5"
PURPLE_SOFT = "#f0ecff"
BORDER = "#d9d4ef"
TEXT = "#252738"
MUTED = "#7b8094"

root.configure(bg=BG)

style = ttk.Style(root)
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    fieldbackground=WHITE,
    foreground=TEXT,
    rowheight=30,
    borderwidth=0,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background=NAVY,
    foreground="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat"
)

style.map(
    "Treeview.Heading",
    background=[("active", NAVY_2)]
)

style.configure(
    "Purple.TButton",
    background=PURPLE,
    foreground="white",
    padding=9,
    font=("Segoe UI", 10, "bold")
)

style.map(
    "Purple.TButton",
    background=[("active", PURPLE_DARK)]
)

style.configure(
    "Light.TButton",
    background=PURPLE_SOFT,
    foreground=PURPLE_DARK,
    padding=9,
    font=("Segoe UI", 10, "bold")
)

style.map(
    "Light.TButton",
    background=[("active", "#e5ddff")]
)

# Encabezado
header = tk.Frame(root, bg=NAVY, height=92)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="Sistema de Registro de Personas",
    bg=NAVY,
    fg="white",
    font=("Segoe UI", 22, "bold")
).pack(anchor="w", padx=28, pady=(18, 0))

tk.Label(
    header,
    text="Organiza y administra tus registros de forma sencilla.",
    bg=NAVY,
    fg="#cfd7e8",
    font=("Segoe UI", 10)
).pack(anchor="w", padx=29, pady=(2, 0))

# Contenedor principal
body = tk.Frame(root, bg=BG)
body.pack(fill="both", expand=True, padx=22, pady=22)

left = tk.Frame(
    body,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)
left.pack(side="left", fill="y", padx=(0, 14))

right = tk.Frame(
    body,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)
right.pack(side="left", fill="both", expand=True)

# Panel formulario
tk.Label(
    left,
    text="Nuevo registro",
    bg=WHITE,
    fg=NAVY,
    font=("Segoe UI", 17, "bold")
).pack(anchor="w", padx=20, pady=(20, 4))

tk.Label(
    left,
    text="Completa los datos de la persona.",
    bg=WHITE,
    fg=MUTED,
    font=("Segoe UI", 9)
).pack(anchor="w", padx=20, pady=(0, 14))

form = tk.Frame(left, bg=WHITE)
form.pack(fill="x", padx=20)

def campo(label):
    tk.Label(
        form,
        text=label,
        bg=WHITE,
        fg=NAVY_2,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", pady=(8, 3))

    e = ttk.Entry(form, width=30, font=("Segoe UI", 10))
    e.pack(fill="x")
    return e

e_nombre = campo("Nombre completo")
e_edad = campo("Edad")
e_ciudad = campo("Ciudad")

tk.Label(
    form,
    text="Estado",
    bg=WHITE,
    fg=NAVY_2,
    font=("Segoe UI", 10, "bold")
).pack(anchor="w", pady=(8, 3))

cb_estado = ttk.Combobox(
    form,
    values=["Activo", "Inactivo"],
    state="readonly",
    width=27
)
cb_estado.set("Activo")
cb_estado.pack(fill="x")

ttk.Button(
    form,
    text="Guardar registro",
    style="Purple.TButton",
    command=agregar
).pack(fill="x", pady=(20, 7))

ttk.Button(
    form,
    text="Eliminar seleccionado",
    style="Light.TButton",
    command=eliminar
).pack(fill="x")

tk.Label(
    left,
    text="Enrique Rojas",
    bg=WHITE,
    fg="#a0a3b2",
    font=("Segoe UI", 8)
).pack(side="bottom", pady=14)

# Panel lista
top = tk.Frame(right, bg=WHITE)
top.pack(fill="x", padx=20, pady=(20, 10))

tk.Label(
    top,
    text="Registros guardados",
    bg=WHITE,
    fg=NAVY,
    font=("Segoe UI", 17, "bold")
).pack(side="left")

lbl_total = tk.Label(
    top,
    text="Total de registros: 0",
    bg=PURPLE_SOFT,
    fg=PURPLE_DARK,
    font=("Segoe UI", 9, "bold"),
    padx=10,
    pady=5
)
lbl_total.pack(side="right")

table_frame = tk.Frame(right, bg=WHITE)
table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

tabla = ttk.Treeview(
    table_frame,
    columns=("Nombre", "Edad", "Ciudad", "Estado"),
    show="headings",
    selectmode="browse"
)

for col, width in [
    ("Nombre", 240),
    ("Edad", 80),
    ("Ciudad", 170),
    ("Estado", 110)
]:
    tabla.heading(col, text=col)
    tabla.column(col, width=width, anchor="w")

scroll = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tabla.yview
)
tabla.configure(yscrollcommand=scroll.set)

tabla.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

root.bind("<Delete>", lambda e: eliminar())

datos = cargar()
refrescar()
root.mainloop()
