# 💬 Python Chat Application

A real-time **two-user chat application** developed using Python, Socket Programming, Threading, and Tkinter GUI.

## 📌 Project Overview

This project is a real-time messaging application where multiple users can connect to a server and exchange messages instantly.

The application provides a simple and professional graphical user interface with:

* 👤 Username support
* 💬 Real-time messaging
* 🕒 Message timestamps
* 💭 Professional chat bubbles
* 🔄 Real-time communication
* 🖥️ Tkinter GUI
* 🔌 Socket-based client-server communication
* 🧵 Threading for simultaneous communication

## 🛠️ Technologies Used

* **Python**
* **Tkinter**
* **Socket Programming**
* **Threading**

## 📂 Project Structure

```text
Chat_Application/
│
├── server.py
├── client.py
├── README.md
└── screenshot.png
```

## ⚙️ How It Works

The application follows a client-server architecture.

```text
Client 1 ───────┐
                │
                ▼
             Server
                ▲
                │
Client 2 ───────┘
```

The server manages connected clients and broadcasts messages between them.

Each client connects to the server using:

```text
IP Address: 127.0.0.1
Port: 5050
```

## ▶️ How to Run

### Step 1 — Start the Server

Open `server.py` in Python IDLE and run the program.

The server should display:

```text
Server started successfully
Waiting for client...
IP: 127.0.0.1
PORT: 5050
```

### Step 2 — Start the Client

Open `client.py` in another Python IDLE window and run it.

Enter your username when prompted.

### Step 3 — Connect Another User

Run `client.py` again in another IDLE window.

Enter a different username.

Now both users can communicate in real time.

## 💬 Features

### 1. Real-Time Messaging

Users can send and receive messages instantly.

### 2. Username

Each user can enter a unique username before joining the chat.

### 3. Message Time

Every message displays the time it was sent.

Example:

```text
Hi!                         05:10 PM
Hello!                      05:11 PM
```

### 4. Chat Bubbles

Messages are displayed using a modern chat-bubble style interface.

### 5. Client-Server Communication

Python socket programming is used for communication between clients and the server.

### 6. Threading

Threading allows the application to receive messages while the user continues sending messages.

## 🧪 Testing

The application was tested by:

* Starting the server successfully
* Connecting multiple clients
* Sending messages between users
* Receiving messages in real time
* Testing username functionality
* Testing message timestamps
* Testing chat-bubble UI
* Testing client disconnection

## 📸 Screenshot

Add your project screenshot to the project folder with the name:

```text
screenshot.png
```

Then add it to this README:

```markdown
![Python Chat Application](screenshot.png)
```

## 🎯 Internship Task

**Task 5 – Chat Application**

### Objective

Build a real-time messaging application in Python.

### Implementation

This project implements the advanced GUI-based version using:

* Python
* Socket Programming
* Threading
* Tkinter

## ✅ Project Status

* ✅ GUI completed
* ✅ Client-Server communication completed
* ✅ Real-time messaging completed
* ✅ Username support completed
* ✅ Message timestamp completed
* ✅ Professional chat bubbles completed
* ✅ Testing completed
* ✅ README completed
##demo video
watch video link:["https://drive.google.com/file/d/12znVB4P-0cXT6feBjYGMKrem5tDBgVf4/view?usp=sharing"]
## 👩‍💻 Author

**ABIRAMI R**

## 📄 License

This project was developed for educational and internship purposes.
