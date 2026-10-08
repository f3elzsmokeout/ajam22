import tkinter as tk

expr = ""

def update():
    display_var.set(expr if expr else "0")

def add(value):
    global expr
    if expr == "Error":
        expr = ""
    expr += value
    update()

def clear():
    global expr
    expr = ""
    update()

def back():
    global expr
    expr = expr[:-1]
    update()

def result():
    global expr
    try:
        expr = str(eval(expr, {"__builtins__": {}}, {}))
    except:
        expr = "Error"
    update()
    if expr == "Error":
        expr = ""

root = tk.Tk()
root.title("Calculadora Básica")
root.geometry("360x520")
root.resizable(False, False)

BG = "#0b0b0b"
PANEL = "#161616"
BORDER = "#3a3a3a"
BTN = "#252525"
BTN_HOVER = "#343434"
OP = "#4a4a4a"
TEXT = "#f2f2f2"
MUTED = "#8f8f8f"
EQUAL = "#d6d6d6"

root.configure(bg=BG)

container = tk.Frame(root, bg=BG, padx=16, pady=16)
container.pack(fill="both", expand=True)

tk.Label(
    container,
    text="Calculadora Básica",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 17, "bold")
).pack(anchor="w", pady=(0, 12))

display_frame = tk.Frame(
    container,
    bg=PANEL,
    highlightbackground=BORDER,
    highlightthickness=1
)
display_frame.pack(fill="x", pady=(0, 12))

display_var = tk.StringVar(value="0")

tk.Label(
    display_frame,
    textvariable=display_var,
    bg=PANEL,
    fg=TEXT,
    anchor="e",
    font=("Segoe UI", 30),
    padx=14,
    pady=18
).pack(fill="x")

grid = tk.Frame(container, bg=BG)
grid.pack(fill="both", expand=True)

buttons = [
    ("C", clear, "special"),
    ("(", lambda: add("("), "special"),
    (")", lambda: add(")"), "special"),
    ("÷", lambda: add("/"), "op"),

    ("7", lambda: add("7"), "num"),
    ("8", lambda: add("8"), "num"),
    ("9", lambda: add("9"), "num"),
    ("×", lambda: add("*"), "op"),

    ("4", lambda: add("4"), "num"),
    ("5", lambda: add("5"), "num"),
    ("6", lambda: add("6"), "num"),
    ("−", lambda: add("-"), "op"),

    ("1", lambda: add("1"), "num"),
    ("2", lambda: add("2"), "num"),
    ("3", lambda: add("3"), "num"),
    ("+", lambda: add("+"), "op"),

    ("0", lambda: add("0"), "num"),
    (".", lambda: add("."), "num"),
    ("⌫", back, "special"),
    ("=", result, "equal")
]

for i, (text, command, kind) in enumerate(buttons):
    if kind == "num":
        bg = BTN
        fg = TEXT
    elif kind == "op":
        bg = OP
        fg = TEXT
    elif kind == "equal":
        bg = EQUAL
        fg = "#111111"
    else:
        bg = "#303030"
        fg = TEXT

    btn = tk.Button(
        grid,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=BTN_HOVER if kind != "equal" else "#eeeeee",
        activeforeground=TEXT if kind != "equal" else "#111111",
        relief="flat",
        bd=0,
        highlightbackground=BORDER,
        highlightthickness=1,
        font=("Segoe UI", 15, "bold"),
        cursor="hand2"
    )
    btn.grid(
        row=i // 4,
        column=i % 4,
        sticky="nsew",
        padx=5,
        pady=5
    )

for r in range(5):
    grid.rowconfigure(r, weight=1)

for c in range(4):
    grid.columnconfigure(c, weight=1)

tk.Label(
    container,
    text="Enrique Rojas",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 8)
).pack(pady=(10, 0))

root.mainloop()
