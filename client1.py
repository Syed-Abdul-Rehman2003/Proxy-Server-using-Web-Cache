import socket
import tkinter as tk
import threading

HEADER = 64
PORT = 12345  # Port on which your proxy server is running
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
PROXY_SERVER = '127.0.0.1'  # IP of proxy server
ADDR = (PROXY_SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send():
    while True:
        message = input("")
        if message == DISCONNECT_MESSAGE:
            client.send(message.encode(FORMAT))
            break
        client.send(message.encode(FORMAT))

def send_message():
    message = entry.get()
    if message == DISCONNECT_MESSAGE:
        client.send(message.encode(FORMAT))
        client.close()
        window.destroy()
    else:
        client.send(message.encode(FORMAT))

window = tk.Tk()
window.title("Web browser")

frame = tk.Frame(window)
frame.pack(padx=20, pady=20)

label = tk.Label(frame, text="Enter URL:")
label.grid(row=0, column=0, padx=5, pady=5)

entry = tk.Entry(frame, width=30)
entry.grid(row=0, column=1, padx=5, pady=5)

choice_frame = tk.Frame(window)
choice_frame.pack(pady=10)

send_message_button = tk.Button(choice_frame, text="Send Request", command=send_message)
send_message_button.pack(side=tk.LEFT, padx=5)

send_thread = threading.Thread(target=send)
send_thread.start()

window.mainloop()


