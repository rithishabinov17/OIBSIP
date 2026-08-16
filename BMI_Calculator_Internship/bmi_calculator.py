import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect("bmi_records.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def calculate_bmi():
    try:
        name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if name == "":
            messagebox.showerror("Error", "Please enter your name.")
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Error",
                "Weight and height must be positive values."
            )
            return

        bmi = weight / (height ** 2)

        if bmi < 18.5:
            category = "Underweight"
            result_color = "orange"
        elif bmi < 25:
            category = "Normal"
            result_color = "green"
        elif bmi < 30:
            category = "Overweight"
            result_color = "orange"
        else:
            category = "Obese"
            result_color = "red"

        result_label.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}",
            fg=result_color
        )

        conn = sqlite3.connect("bmi_records.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO bmi_records
            (name, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            weight,
            height,
            bmi,
            category,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "BMI calculated and saved successfully!"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid numeric values."
        )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Database error:\n{error}"
        )

def delete_history(record_id, history_window):
    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this BMI record?"
    )

    if confirm:
        try:
            conn = sqlite3.connect("bmi_records.db")
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM bmi_records WHERE id = ?",
                (record_id,)
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "BMI record deleted successfully!"
            )

            load_history(history_window)

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Database error:\n{error}"
            )

def clear_all_history(history_window):
    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete all BMI records?"
    )

    if confirm:
        try:
            conn = sqlite3.connect("bmi_records.db")
            cursor = conn.cursor()

            cursor.execute("DELETE FROM bmi_records")

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "All BMI history deleted successfully!"
            )

            load_history(history_window)

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Database error:\n{error}"
            )

def load_history(history_window, search_name=""):
    for widget in history_window.winfo_children():
        if getattr(widget, "history_record", False):
            widget.destroy()

    conn = sqlite3.connect("bmi_records.db")
    cursor = conn.cursor()

    if search_name.strip() == "":
        cursor.execute("""
            SELECT id, name, weight, height, bmi, category, date
            FROM bmi_records
            ORDER BY id DESC
        """)
    else:
        cursor.execute("""
            SELECT id, name, weight, height, bmi, category, date
            FROM bmi_records
            WHERE name LIKE ?
            ORDER BY id DESC
        """, ("%" + search_name.strip() + "%",))

    records = cursor.fetchall()
    conn.close()

    if not records:
        no_record_label = tk.Label(
            history_window,
            text="No BMI records found.",
            font=("Arial", 14)
        )
        no_record_label.history_record = True
        no_record_label.pack(pady=20)
        return

    for record in records:
        record_id = record[0]

        frame = tk.Frame(history_window)
        frame.history_record = True
        frame.pack(fill="x", padx=10, pady=5)

        text = (
            f"ID: {record[0]} | "
            f"Name: {record[1]} | "
            f"Weight: {record[2]} kg | "
            f"Height: {record[3]} m | "
            f"BMI: {record[4]:.2f} | "
            f"{record[5]} | "
            f"{record[6]}"
        )

        record_label = tk.Label(
            frame,
            text=text,
            font=("Arial", 9),
            anchor="w"
        )
        record_label.pack(
            side="left",
            fill="x",
            expand=True
        )

        delete_button = tk.Button(
            frame,
            text="Delete",
            command=lambda id=record_id: delete_history(
                id,
                history_window
            )
        )
        delete_button.pack(side="right")

def search_history(history_window, search_entry):
    search_name = search_entry.get()
    load_history(history_window, search_name)

def view_history():
    history_window = tk.Toplevel(window)
    history_window.title("BMI History")
    history_window.geometry("900x600")

    history_label = tk.Label(
        history_window,
        text="BMI History",
        font=("Arial", 20, "bold")
    )
    history_label.pack(pady=15)

    search_frame = tk.Frame(history_window)
    search_frame.pack(pady=5)

    search_label = tk.Label(
        search_frame,
        text="Search Name:"
    )
    search_label.pack(side="left", padx=5)

    search_entry = tk.Entry(
        search_frame,
        width=25
    )
    search_entry.pack(side="left", padx=5)

    search_button = tk.Button(
        search_frame,
        text="Search",
        command=lambda: search_history(
            history_window,
            search_entry
        )
    )
    search_button.pack(side="left", padx=5)

    show_all_button = tk.Button(
        search_frame,
        text="Show All",
        command=lambda: [
            search_entry.delete(0, tk.END),
            load_history(history_window)
        ]
    )
    show_all_button.pack(side="left", padx=5)

    clear_button = tk.Button(
        history_window,
        text="Clear All History",
        command=lambda: clear_all_history(history_window),
        font=("Arial", 10, "bold")
    )
    clear_button.pack(pady=10)

    load_history(history_window)

create_database()

window = tk.Tk()
window.title("BMI Calculator")
window.geometry("500x550")

title = tk.Label(
    window,
    text="BMI Calculator",
    font=("Arial", 24, "bold")
)
title.pack(pady=20)

name_label = tk.Label(
    window,
    text="Name"
)
name_label.pack()

name_entry = tk.Entry(
    window,
    width=30
)
name_entry.pack(pady=5)

weight_label = tk.Label(
    window,
    text="Weight (kg)"
)
weight_label.pack()

weight_entry = tk.Entry(
    window,
    width=30
)
weight_entry.pack(pady=5)

height_label = tk.Label(
    window,
    text="Height (m)"
)
height_label.pack()

height_entry = tk.Entry(
    window,
    width=30
)
height_entry.pack(pady=5)

result_label = tk.Label(
    window,
    text="BMI: --",
    font=("Arial", 16, "bold")
)
result_label.pack(pady=20)

calculate_button = tk.Button(
    window,
    text="Calculate BMI",
    command=calculate_bmi,
    font=("Arial", 12, "bold")
)
calculate_button.pack()

history_button = tk.Button(
    window,
    text="View History",
    command=view_history,
    font=("Arial", 12, "bold")
)
history_button.pack(pady=15)

window.mainloop()
