import socket
import threading
import webbrowser as wb
import tkinter as tk
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    log(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        try:
           # msg_length = conn.recv(HEADER).decode('utf-8')
        #if msg_length:
            #msg_length = int(msg_length)
            msg = conn.recv(4090).decode('utf-8')
            wb.get().open(msg)
            if msg == "!DISCONNECT":
                connected = False
            log(f"[REQUEST FROM {addr}] {msg}")
            break
        except ValueError as e:
            wb.get().open(msg)
            print(f"[ERROR] {e}")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            break
    
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# Function to start the server
def start_server():
    server_thread = threading.Thread(target=start)
    server_thread.start()
    log("[STARTING] Main Server is starting...")

# Function to stop the server
def stop_server():
    server.close()
    exit()

# Function to log messages to the GUI
def log(message):
    text_area.insert(tk.END, message + '\n')
    text_area.see(tk.END)  # Auto-scroll to the bottom of the text area

# GUI setup
root = tk.Tk()
root.title("Main Server")

# Text area to display logs
text_area = tk.Text(root, height=20, width=50)
text_area.pack(padx=10, pady=10)

# Start button
start_button = tk.Button(root, text="Start Server", command=start_server)
start_button.pack(side=tk.LEFT, padx=10)

# Stop button
stop_button = tk.Button(root, text="Stop Server", command=stop_server)
stop_button.pack(side=tk.RIGHT, padx=10)

root.mainloop()