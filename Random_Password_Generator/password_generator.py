import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip

history = []

def generate_password():
    try:
        length = int(length_var.get())
    except ValueError:
        messagebox.showerror("Invalid Length", "Enter a valid number.")
        return

    if length < 8:
        messagebox.showerror("Invalid Length", "Minimum length is 8.")
        return

    character_sets = []

    if uppercase_var.get():
        character_sets.append(string.ascii_uppercase)

    if lowercase_var.get():
        character_sets.append(string.ascii_lowercase)

    if numbers_var.get():
        character_sets.append(string.digits)

    if symbols_var.get():
        character_sets.append(string.punctuation)

    if len(character_sets) < 2:
        messagebox.showerror(
            "Selection Error",
            "Select at least 2 character types."
        )
        return

    password_characters = []

    for characters in character_sets:
        password_characters.append(secrets.choice(characters))

    all_characters = "".join(character_sets)

    while len(password_characters) < length:
        password_characters.append(
            secrets.choice(all_characters)
        )

    for i in range(len(password_characters) - 1, 0, -1):
        j = secrets.randbelow(i + 1)

        password_characters[i], password_characters[j] = (
            password_characters[j],
            password_characters[i]
        )

    password = "".join(password_characters)

    password_var.set(password)

    history.insert(0, password)

    if len(history) > 5:
        history.pop()

    update_history()
    update_strength(length, len(character_sets))


def update_strength(length, type_count):
    score = 0

    if length >= 8:
        score += 1

    if length >= 12:
        score += 1

    if length >= 16:
        score += 1

    if type_count >= 3:
        score += 1

    if type_count == 4:
        score += 1

    if score <= 2:
        strength_var.set("Weak")
        strength_label.config(fg="#e74c3c")

    elif score <= 4:
        strength_var.set("Medium")
        strength_label.config(fg="#f39c12")

    else:
        strength_var.set("Strong")
        strength_label.config(fg="#27ae60")


def copy_password():
    password = password_var.get()

    if not password:
        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )
        return

    try:
        pyperclip.copy(password)

        messagebox.showinfo(
            "Copied",
            "Password copied successfully!"
        )

    except Exception as error:
        messagebox.showerror(
            "Copy Error",
            str(error)
        )


def update_history():
    history_list.delete(0, tk.END)

    for number, password in enumerate(history, start=1):
        history_list.insert(
            tk.END,
            f"{number}. {password}"
        )


def clear_history():
    history.clear()
    history_list.delete(0, tk.END)

    password_var.set("")
    strength_var.set("Not Generated")

    strength_label.config(
        fg="#7f8c8d"
    )


window = tk.Tk()

window.title("Random Password Generator")
window.geometry("900x750")
window.minsize(700, 600)
window.configure(bg="#f4f7fb")


header = tk.Frame(
    window,
    bg="#243b55",
    height=110
)

header.pack(fill="x")

tk.Label(
    header,
    text="RANDOM PASSWORD GENERATOR",
    font=("Segoe UI", 25, "bold"),
    bg="#243b55",
    fg="white"
).pack(pady=(20, 5))

tk.Label(
    header,
    text="Generate Strong and Secure Passwords",
    font=("Segoe UI", 11),
    bg="#243b55",
    fg="#dfe6e9"
).pack()


container = tk.Frame(
    window,
    bg="#f4f7fb"
)

container.pack(
    fill="both",
    expand=True
)

canvas = tk.Canvas(
    container,
    bg="#f4f7fb",
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    container,
    orient="vertical",
    command=canvas.yview
)

scrollable_frame = tk.Frame(
    canvas,
    bg="#f4f7fb"
)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw",
    width=850
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


main_frame = tk.Frame(
    scrollable_frame,
    bg="#f4f7fb"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=60,
    pady=25
)


settings_card = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid"
)

settings_card.pack(
    fill="x"
)


tk.Label(
    settings_card,
    text="Password Settings",
    font=("Segoe UI", 18, "bold"),
    bg="white",
    fg="#243b55"
).pack(
    anchor="w",
    padx=30,
    pady=(20, 15)
)


tk.Label(
    settings_card,
    text="Password Length",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#34495e"
).pack(
    anchor="w",
    padx=30
)


length_var = tk.StringVar(
    value="12"
)


length_spinbox = tk.Spinbox(
    settings_card,
    from_=8,
    to=50,
    textvariable=length_var,
    width=10,
    font=("Segoe UI", 12),
    justify="center"
)

length_spinbox.pack(
    anchor="w",
    padx=30,
    pady=8
)


tk.Label(
    settings_card,
    text="Character Types",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#34495e"
).pack(
    anchor="w",
    padx=30
)


uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)


check_frame = tk.Frame(
    settings_card,
    bg="white"
)

check_frame.pack(
    anchor="w",
    padx=25,
    pady=10
)


tk.Checkbutton(
    check_frame,
    text="Uppercase (A-Z)",
    variable=uppercase_var,
    bg="white",
    activebackground="white",
    font=("Segoe UI", 10)
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)


tk.Checkbutton(
    check_frame,
    text="Lowercase (a-z)",
    variable=lowercase_var,
    bg="white",
    activebackground="white",
    font=("Segoe UI", 10)
).grid(
    row=0,
    column=1,
    padx=30,
    pady=5,
    sticky="w"
)


tk.Checkbutton(
    check_frame,
    text="Numbers (0-9)",
    variable=numbers_var,
    bg="white",
    activebackground="white",
    font=("Segoe UI", 10)
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)


tk.Checkbutton(
    check_frame,
    text="Symbols (!@#)",
    variable=symbols_var,
    bg="white",
    activebackground="white",
    font=("Segoe UI", 10)
).grid(
    row=1,
    column=1,
    padx=30,
    pady=5,
    sticky="w"
)


generate_button = tk.Button(
    settings_card,
    text="GENERATE PASSWORD",
    command=generate_password,
    bg="#3498db",
    fg="white",
    activebackground="#2980b9",
    font=("Segoe UI", 14, "bold"),
    bd=0,
    cursor="hand2",
    height=2
)

generate_button.pack(
    fill="x",
    padx=30,
    pady=(5, 25)
)


result_card = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid"
)

result_card.pack(
    fill="x",
    pady=20
)


tk.Label(
    result_card,
    text="GENERATED PASSWORD",
    font=("Segoe UI", 12, "bold"),
    bg="white",
    fg="#7f8c8d"
).pack(
    pady=(20, 8)
)


password_var = tk.StringVar()


password_entry = tk.Entry(
    result_card,
    textvariable=password_var,
    font=("Consolas", 20, "bold"),
    justify="center",
    state="readonly",
    readonlybackground="white",
    bd=1
)

password_entry.pack(
    fill="x",
    padx=30,
    pady=8,
    ipady=10
)


copy_button = tk.Button(
    result_card,
    text="COPY PASSWORD",
    command=copy_password,
    bg="#27ae60",
    fg="white",
    activebackground="#219150",
    activeforeground="white",
    font=("Segoe UI", 16, "bold"),
    bd=0,
    cursor="hand2",
    height=2
)

copy_button.pack(
    fill="x",
    padx=100,
    pady=15
)


strength_frame = tk.Frame(
    result_card,
    bg="white"
)

strength_frame.pack(
    pady=(5, 20)
)


tk.Label(
    strength_frame,
    text="Password Strength:",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#34495e"
).pack(side="left")


strength_var = tk.StringVar(
    value="Not Generated"
)


strength_label = tk.Label(
    strength_frame,
    textvariable=strength_var,
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#7f8c8d"
)

strength_label.pack(
    side="left",
    padx=8
)


history_card = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid"
)

history_card.pack(
    fill="x"
)


tk.Label(
    history_card,
    text="LAST 5 GENERATED PASSWORDS",
    font=("Segoe UI", 17, "bold"),
    bg="white",
    fg="#243b55"
).pack(
    anchor="w",
    padx=30,
    pady=(20, 10)
)


history_list = tk.Listbox(
    history_card,
    height=6,
    font=("Consolas", 12),
    bd=1,
    relief="solid"
)

history_list.pack(
    fill="x",
    padx=30,
    pady=5
)


clear_button = tk.Button(
    history_card,
    text="CLEAR HISTORY",
    command=clear_history,
    bg="#e74c3c",
    fg="white",
    activebackground="#c0392b",
    activeforeground="white",
    font=("Segoe UI", 14, "bold"),
    bd=0,
    cursor="hand2",
    height=2
)

clear_button.pack(
    fill="x",
    padx=100,
    pady=15
)


tk.Label(
    scrollable_frame,
    text="Python + Tkinter + Secrets + Pyperclip",
    font=("Segoe UI", 9),
    bg="#f4f7fb",
    fg="#95a5a6"
).pack(
    pady=10
)


window.mainloop()
