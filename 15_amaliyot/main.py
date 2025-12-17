"""
Topshiriq: Multi-Client Chat Server with File Transfer and Commands
Birlashtirilgan topshiriqlar:
- Chat funksiyasi (7)
- Maxsus buyruqlar !exit va !list (8)
- Timeout bilan select (9)
- Statistikalar (10)
- Non-blocking chat server (11)
- Fayl yuborish (12)
- Logging (6)
"""

import selectors
import socket
import threading
import time
import os
from datetime import datetime
from collections import defaultdict

# Global o'zgaruvchilar
HOST = "127.0.0.1"
PORT = 5000
FILE_PORT = 5001
LOG_FILE = "server.log"
UPLOADS_DIR = "uploads"
STATS_INTERVAL = 10  # soniya

# Statistikalar
stats = {
    'total_messages': 0,
    'total_files': 0,
    'active_clients': 0,
    'start_time': time.time()
}

# Mijozlar ro'yxati: {socket: {'addr': addr, 'nickname': nickname}}
clients = {}

# Selectorlar
sel = selectors.DefaultSelector()
file_sel = selectors.DefaultSelector()

# Uploads papkasini yaratish
os.makedirs(UPLOADS_DIR, exist_ok=True)


def log_message(message_type, message, client_addr=None):
    """Xabarlarni server.log fayliga yozish"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    addr_str = f" [{client_addr}]" if client_addr else ""
    log_entry = f"[{timestamp}]{addr_str} [{message_type}] {message}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    print(f"[{timestamp}]{addr_str} {message}")


def broadcast_message(sender_sock, message, exclude_sender=True):
    """Barcha mijozlarga xabar yuborish"""
    disconnected = []
    for sock, client_info in clients.items():
        if exclude_sender and sock == sender_sock:
            continue
        try:
            sock.sendall(message.encode('utf-8'))
        except (ConnectionError, OSError):
            disconnected.append(sock)
    
    # Uzilgan ulanishlarni tozalash
    for sock in disconnected:
        handle_client_disconnect(sock)


def handle_client_disconnect(sock):
    """Mijoz uzilganda tozalash"""
    if sock in clients:
        client_info = clients[sock]
        addr = client_info['addr']
        nickname = client_info.get('nickname', 'Unknown')
        
        log_message("DISCONNECT", f"Mijoz chiqdi: {nickname} ({addr[0]}:{addr[1]})", addr)
        broadcast_message(sock, f"[SERVER] {nickname} chatdan chiqdi.\n", exclude_sender=False)
        
        sel.unregister(sock)
        sock.close()
        del clients[sock]
        stats['active_clients'] = len(clients)


def handle_client_command(sock, command, client_info):
    """Maxsus buyruqlarni boshqarish"""
    command = command.strip().lower()
    
    if command == "!exit":
        handle_client_disconnect(sock)
        return True
    elif command == "!list":
        client_list = []
        for s, info in clients.items():
            nickname = info.get('nickname', 'Unknown')
            addr = info['addr']
            client_list.append(f"  - {nickname} ({addr[0]}:{addr[1]})")
        
        response = "[SERVER] Ulangan mijozlar:\n" + "\n".join(client_list) + "\n"
        try:
            sock.sendall(response.encode('utf-8'))
        except (ConnectionError, OSError):
            handle_client_disconnect(sock)
            return True
        return True
    
    return False


def read_client(sock):
    """Mijozdan xabar o'qish"""
    try:
        data = sock.recv(4096)
        if not data:
            handle_client_disconnect(sock)
            return
        
        message = data.decode('utf-8', errors='ignore').strip()
        client_info = clients[sock]
        addr = client_info['addr']
        nickname = client_info.get('nickname', f"Client-{addr[1]}")
        
        # Maxsus buyruqlarni tekshirish
        if message.startswith('!'):
            if handle_client_command(sock, message, client_info):
                return
        
        # Oddiy xabar
        formatted_message = f"[{nickname}]: {message}\n"
        log_message("MESSAGE", f"{nickname}: {message}", addr)
        broadcast_message(sock, formatted_message)
        stats['total_messages'] += 1
        
    except (ConnectionError, OSError, UnicodeDecodeError) as e:
        handle_client_disconnect(sock)


def accept_client(sock):
    """Yangi mijozni qabul qilish"""
    try:
        conn, addr = sock.accept()
        conn.setblocking(False)
        
        # Nickname so'rash
        conn.sendall(b"[SERVER] Ismingizni kiriting: ")
        
        # Mijozni ro'yxatga qo'shish
        clients[conn] = {'addr': addr, 'nickname': None}
        stats['active_clients'] = len(clients)
        
        sel.register(conn, selectors.EVENT_READ, read_client)
        log_message("CONNECT", f"Yangi mijoz ulanmoqda: {addr[0]}:{addr[1]}", addr)
        
        # Boshqa mijozlarga xabar berish
        broadcast_message(conn, f"[SERVER] Yangi mijoz chatga qo'shildi.\n", exclude_sender=False)
        
    except (OSError, ConnectionError) as e:
        log_message("ERROR", f"Yangi mijozni qabul qilishda xato: {e}")


def handle_file_upload(sock):
    """Fayl yuborishni qabul qilish"""
    try:
        # Fayl nomi va hajmini olish
        header = sock.recv(1024).decode('utf-8', errors='ignore')
        if not header:
            file_sel.unregister(sock)
            sock.close()
            return
        
        parts = header.split('|')
        if len(parts) != 3:
            sock.sendall(b"ERROR: Invalid file header")
            file_sel.unregister(sock)
            sock.close()
            return
        
        filename, file_size_str, client_addr = parts
        file_size = int(file_size_str)
        
        # Xavfsizlik: faqat fayl nomini olish
        filename = os.path.basename(filename)
        filepath = os.path.join(UPLOADS_DIR, f"{int(time.time())}_{filename}")
        
        log_message("FILE_UPLOAD", f"Fayl qabul qilinmoqda: {filename} ({file_size} bytes)", client_addr)
        
        # Faylni qabul qilish
        received = 0
        with open(filepath, 'wb') as f:
            while received < file_size:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                f.write(chunk)
                received += len(chunk)
        
        if received == file_size:
            sock.sendall(f"SUCCESS: Fayl saqlandi: {filepath}".encode('utf-8'))
            log_message("FILE_SUCCESS", f"Fayl saqlandi: {filepath} ({file_size} bytes)", client_addr)
            stats['total_files'] += 1
        else:
            sock.sendall(f"ERROR: Fayl to'liq yuklanmadi".encode('utf-8'))
            os.remove(filepath)
            log_message("FILE_ERROR", f"Fayl to'liq yuklanmadi: {filename}", client_addr)
        
        file_sel.unregister(sock)
        sock.close()
        
    except (OSError, ValueError, ConnectionError) as e:
        log_message("FILE_ERROR", f"Fayl yuklashda xato: {e}")
        try:
            file_sel.unregister(sock)
            sock.close()
        except:
            pass


def accept_file_client(sock):
    """Fayl yuborish uchun yangi mijozni qabul qilish"""
    try:
        conn, addr = sock.accept()
        conn.setblocking(False)
        file_sel.register(conn, selectors.EVENT_READ, handle_file_upload)
        log_message("FILE_CONNECT", f"Fayl yuborish ulanishi: {addr[0]}:{addr[1]}", addr)
    except (OSError, ConnectionError) as e:
        log_message("ERROR", f"Fayl mijozini qabul qilishda xato: {e}")


def print_stats():
    """Statistikalarni chiqarish"""
    uptime = int(time.time() - stats['start_time'])
    uptime_str = f"{uptime // 60}min {uptime % 60}sec"
    
    stats_msg = (
        f"\n=== STATISTIKALAR ===\n"
        f"Faol mijozlar: {stats['active_clients']}\n"
        f"Jami xabarlar: {stats['total_messages']}\n"
        f"Jami fayllar: {stats['total_files']}\n"
        f"Server vaqti: {uptime_str}\n"
        f"====================\n"
    )
    print(stats_msg)
    log_message("STATS", stats_msg.strip())


def stats_thread():
    """Statistikalarni har 10 soniyada chiqarish"""
    while True:
        time.sleep(STATS_INTERVAL)
        print_stats()


def main():
    """Asosiy server funksiyasi"""
    # Chat server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    server.setblocking(False)
    sel.register(server, selectors.EVENT_READ, accept_client)
    
    # Fayl server
    file_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    file_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    file_server.bind((HOST, FILE_PORT))
    file_server.listen()
    file_server.setblocking(False)
    file_sel.register(file_server, selectors.EVENT_READ, accept_file_client)
    
    log_message("START", f"Chat server {HOST}:{PORT} da ishga tushdi")
    log_message("START", f"Fayl server {HOST}:{FILE_PORT} da ishga tushdi")
    print(f"Chat server {HOST}:{PORT} da ishlayapti...")
    print(f"Fayl server {HOST}:{FILE_PORT} da ishlayapti...")
    print("Statistikalar har 10 soniyada chiqadi.\n")
    
    # Statistikalar threadini ishga tushirish
    stats_thread_obj = threading.Thread(target=stats_thread, daemon=True)
    stats_thread_obj.start()
    
    # Asosiy loop
    try:
        while True:
            # Chat server
            events = sel.select(timeout=5)
            if events:
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj)
            else:
                # Timeout - hech narsa bo'lmadi
                pass  # Statistikalar alohida threadda chiqadi
            
            # Fayl server
            file_events = file_sel.select(timeout=0.1)
            for key, mask in file_events:
                callback = key.data
                callback(key.fileobj)
                
    except KeyboardInterrupt:
        log_message("SHUTDOWN", "Server to'xtatilmoqda...")
        print("\nServer to'xtatilmoqda...")
        
        # Barcha mijozlarni yopish
        for sock in list(clients.keys()):
            try:
                sock.sendall(b"[SERVER] Server yopilmoqda...\n")
                sock.close()
            except:
                pass
        
        server.close()
        file_server.close()
        sel.close()
        file_sel.close()
        log_message("SHUTDOWN", "Server to'xtatildi")


if __name__ == "__main__":
    main()
