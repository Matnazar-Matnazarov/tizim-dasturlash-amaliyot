import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 0))

root = tk.Tk()
root.title("UDP Chat")

chat_log = scrolledtext.ScrolledText(root, state='disabled', width=50, height=20)
chat_log.pack(padx=10, pady=10)

msg_entry = tk.Entry(root, width=40)
msg_entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))

def send_message():
    msg = msg_entry.get()
    if msg:
        sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
        update_chat(f"You: {msg}")
        msg_entry.delete(0, tk.END)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10, pady=(0,10))

def receive_messages():
    while True:
        try:
            data, _ = sock.recvfrom(1024)
            msg = data.decode()
            root.after(0, lambda m=msg: update_chat(f"Server: {m}"))
        except:
            break

def update_chat(message):
    chat_log.config(state='normal')
    chat_log.insert(tk.END, message + "\n")
    chat_log.config(state='disabled')

threading.Thread(target=receive_messages, daemon=True).start()
root.mainloop()
