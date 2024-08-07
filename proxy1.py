import socket
import threading
import tkinter as tk
from collections import OrderedDict
import webbrowser as wb
# Constants
HEADER = 64
PORT = 12345
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
BUFFER_SIZE = 4096
FORMAT = 'utf-8'
CACHE_SIZE = 3

# Setup Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Cache Initialization
cache = OrderedDict()

# Function to handle client connections
def handle_client(conn, addr):
    log(f"[NEW CONNECTION] {addr} connected")
    while True:
        try:
            request = conn.recv(BUFFER_SIZE).decode(FORMAT)
            if not request:
                break
            log(f"[REQUEST FROM {addr}] {request}")
            if request in cache:
                log(f"[CACHE HIT] {request}")
                response = cache[request]
                wb.get().open(request)
            else:
                log(f"[CACHE MISS] {request}")
                response = fetch_data_from_server(request)
                cache[request] = response
            conn.sendall(response.encode(FORMAT))
        except Exception as e:
            log(f"[ERROR] {e}")
            break
    conn.close()

# Function to fetch data from the main server
def fetch_data_from_server(request):
    host = socket.gethostbyname(socket.gethostname())
    port = 5050
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
        proxy_socket.connect((host, port))
        proxy_socket.sendall(request.encode(FORMAT))
        response = proxy_socket.recv(BUFFER_SIZE).decode(FORMAT)
    return response

def start():
    server.listen()
    print(f"[LISTENING] Proxy Server is listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        log(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# Function to start the server
def start_server():
    server_thread = threading.Thread(target=start)
    server_thread.start()
    log("[STARTING] Proxy Server is starting...")

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
root.title("Proxy Server")

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