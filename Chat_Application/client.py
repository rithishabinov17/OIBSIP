import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

window = tk.Tk()
window.withdraw()

username = simpledialog.askstring(
    "Username",
    "Enter your name:"
)

if not username:
    username = "User"

window.deiconify()
window.title("Python Chat Application")
window.geometry("650x650")
window.minsize(550, 550)

header = tk.Frame(
    window,
    bg="#1565C0",
    height=65
)
header.pack(fill=tk.X)
header.pack_propagate(False)

title = tk.Label(
    header,
    text="💬 Python Chat Application",
    font=("Arial", 18, "bold"),
    bg="#1565C0",
    fg="white"
)
title.pack(side=tk.LEFT, padx=15)

status = tk.Label(
    header,
    text="● Online",
    font=("Arial", 11, "bold"),
    bg="#1565C0",
    fg="white"
)
status.pack(side=tk.RIGHT, padx=15)

name_label = tk.Label(
    window,
    text="Logged in as: " + username,
    font=("Arial", 10, "bold"),
    fg="#555555"
)
name_label.pack(anchor="w", padx=15, pady=(10, 5))

chat_container = tk.Frame(
    window,
    bg="#E8EEF5",
    bd=1,
    relief="solid"
)
chat_container.pack(
    fill=tk.BOTH,
    expand=True,
    padx=12,
    pady=5
)

canvas = tk.Canvas(
    chat_container,
    bg="#E8EEF5",
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    chat_container,
    orient="vertical",
    command=canvas.yview
)

chat_frame = tk.Frame(
    canvas,
    bg="#E8EEF5"
)

chat_window = canvas.create_window(
    (0, 0),
    window=chat_frame,
    anchor="nw"
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)

canvas.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)

def update_scroll(event=None):
    canvas.configure(
        scrollregion=canvas.bbox("all")
    )
    canvas.yview_moveto(1.0)

chat_frame.bind(
    "<Configure>",
    update_scroll
)

def resize_chat(event):
    canvas.itemconfig(
        chat_window,
        width=event.width
    )

canvas.bind(
    "<Configure>",
    resize_chat
)

bottom = tk.Frame(
    window,
    bg="#F5F5F5"
)
bottom.pack(
    fill=tk.X,
    padx=12,
    pady=12
)

message_entry = tk.Entry(
    bottom,
    font=("Arial", 12),
    bd=1,
    relief="solid"
)
message_entry.pack(
    side=tk.LEFT,
    fill=tk.X,
    expand=True,
    ipady=8,
    padx=(0, 10)
)

def get_time():
    return datetime.now().strftime("%I:%M %p")

def add_message(sender, message, message_time, own_message=False):

    row = tk.Frame(
        chat_frame,
        bg="#E8EEF5"
    )
    row.pack(
        fill=tk.X,
        padx=10,
        pady=5
    )

    if own_message:

        bubble = tk.Frame(
            row,
            bg="#1565C0",
            padx=12,
            pady=8
        )
        bubble.pack(
            side=tk.RIGHT,
            anchor="e"
        )

        message_label = tk.Label(
            bubble,
            text=message,
            font=("Arial", 11),
            bg="#1565C0",
            fg="white",
            justify="left",
            wraplength=350
        )
        message_label.pack(anchor="w")

        time_label = tk.Label(
            bubble,
            text=message_time,
            font=("Arial", 8),
            bg="#1565C0",
            fg="#DDEBFF"
        )
        time_label.pack(
            anchor="e",
            pady=(3, 0)
        )

    else:

        bubble = tk.Frame(
            row,
            bg="white",
            padx=12,
            pady=8,
            bd=1,
            relief="solid"
        )
        bubble.pack(
            side=tk.LEFT,
            anchor="w"
        )

        sender_label = tk.Label(
            bubble,
            text=sender,
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#1565C0"
        )
        sender_label.pack(
            anchor="w"
        )

        message_label = tk.Label(
            bubble,
            text=message,
            font=("Arial", 11),
            bg="white",
            fg="#222222",
            justify="left",
            wraplength=350
        )
        message_label.pack(
            anchor="w",
            pady=(2, 0)
        )

        time_label = tk.Label(
            bubble,
            text=message_time,
            font=("Arial", 8),
            bg="white",
            fg="#888888"
        )
        time_label.pack(
            anchor="e",
            pady=(3, 0)
        )

    window.after(
        50,
        update_scroll
    )

def receive_messages():

    while True:

        try:
            message = client.recv(1024).decode()

            if not message:
                break

            if message == "USERNAME":
                client.send(username.encode())

            else:

                if ": " in message:

                    sender, text = message.split(
                        ": ",
                        1
                    )

                    window.after(
                        0,
                        add_message,
                        sender,
                        text,
                        get_time(),
                        False
                    )

                else:

                    window.after(
                        0,
                        add_message,
                        "System",
                        message,
                        get_time(),
                        False
                    )

        except:

            window.after(
                0,
                lambda: status.config(
                    text="● Offline"
                )
            )

            break

def send_message():

    message = message_entry.get().strip()

    if message:

        full_message = username + ": " + message

        try:

            client.send(
                full_message.encode()
            )

            add_message(
                "You",
                message,
                get_time(),
                True
            )

            message_entry.delete(
                0,
                tk.END
            )

        except:

            status.config(
                text="● Offline"
            )

def enter_pressed(event):
    send_message()

def close_chat():

    try:
        client.close()
    except:
        pass

    window.destroy()

send_button = tk.Button(
    bottom,
    text="Send",
    font=("Arial", 11, "bold"),
    bg="#1565C0",
    fg="white",
    activebackground="#0D47A1",
    activeforeground="white",
    width=10,
    bd=0,
    command=send_message
)
send_button.pack(
    side=tk.RIGHT,
    ipady=7
)

message_entry.bind(
    "<Return>",
    enter_pressed
)

clear_button = tk.Button(
    window,
    text="Clear Chat",
    font=("Arial", 10),
    width=12,
    command=lambda: [
        widget.destroy()
        for widget in chat_frame.winfo_children()
    ]
)
clear_button.pack(
    pady=(0, 8)
)

window.protocol(
    "WM_DELETE_WINDOW",
    close_chat
)

threading.Thread(
    target=receive_messages,
    daemon=True
).start()

message_entry.focus()

window.mainloop()
