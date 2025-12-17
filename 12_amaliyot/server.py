import socket
import datetime

HOST = '127.0.0.1'
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server ishga tushdi. Mijoz kutilyapti...")

    conn, _ = s.accept()
    with conn:
        print("Mijoz ulandi")
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            data = data.strip().lower()

            if data == 'time':
                response = datetime.datetime.now().strftime("%H:%M:%S")
            elif data == 'date':
                response = datetime.datetime.now().strftime("%Y-%m-%d")
            else:
                response = data

            print(f"Mijozdan kelgan: {data}")
            conn.sendall(response.encode('utf-8'))
