import socket

HOST = '127.0.0.1'
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Serverga ulandingiz. Xabar yuboring ('exit' yozsangiz chiqasiz).")

    while True:
        message = input("Yuboriladigan xabar: ")

        if message.lower() == 'exit':
            print("Ulanish yopildi.")
            break

        s.sendall(message.encode("utf-8"))
        data = s.recv(1024).decode('utf-8')
        print(f"Server javobi: {data}")
