import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("UDP working...")

while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode()
    print(f"{addr[0]}: {msg}")
    sock.sendto(msg.encode(), addr)
    print("Message", msg)
