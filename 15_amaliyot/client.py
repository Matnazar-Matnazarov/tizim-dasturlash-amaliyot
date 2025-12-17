"""
Chat Client - Server bilan aloqa qilish uchun mijoz dasturi
"""

import socket
import threading
import sys
import os


HOST = "127.0.0.1"
CHAT_PORT = 5000
FILE_PORT = 5001


def receive_messages(sock):
    """Serverdan xabarlarni qabul qilish"""
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print("\nServer bilan ulanish uzildi.")
                break
            print(data.decode('utf-8'), end='')
        except (ConnectionError, OSError):
            print("\nServer bilan ulanish uzildi.")
            break


def send_file(filename, host=HOST, port=FILE_PORT):
    """Fayl yuborish"""
    if not os.path.exists(filename):
        print(f"Xato: {filename} fayli topilmadi.")
        return False
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        file_size = os.path.getsize(filename)
        header = f"{filename}|{file_size}|{HOST}:{FILE_PORT}"
        sock.sendall(header.encode('utf-8'))
        
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                sock.sendall(chunk)
        
        response = sock.recv(1024).decode('utf-8')
        print(f"[SERVER] {response}")
        sock.close()
        return True
        
    except Exception as e:
        print(f"Fayl yuborishda xato: {e}")
        return False


def main():
    """Asosiy mijoz funksiyasi"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, CHAT_PORT))
        
        # Xabarlarni qabul qilish thread
        receive_thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
        receive_thread.start()
        
        print("Chat serverga ulandi. Xabarlarni yuborishingiz mumkin.")
        print("Buyruqlar: !exit - chiqish, !list - mijozlar ro'yxati, !file <fayl> - fayl yuborish\n")
        
        while True:
            message = input()
            
            if message.strip() == "!exit":
                sock.sendall("!exit".encode('utf-8'))
                break
            elif message.strip().startswith("!file "):
                filename = message.strip()[6:]
                send_file(filename)
            else:
                sock.sendall(message.encode('utf-8'))
        
        sock.close()
        print("Chatdan chiqildi.")
        
    except ConnectionRefusedError:
        print(f"Xato: Server {HOST}:{CHAT_PORT} da ishlamayapti.")
    except KeyboardInterrupt:
        print("\nChatdan chiqildi.")
        try:
            sock.close()
        except:
            pass
    except Exception as e:
        print(f"Xato: {e}")


if __name__ == "__main__":
    main()

