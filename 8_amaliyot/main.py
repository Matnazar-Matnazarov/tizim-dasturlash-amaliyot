"""
2. Ikki iste'molchi: biri faqat toq, biri faqat juft sonlarni qayta ishlasin.
Quyida threading va queue yordamida ishlab chiqilgan yechim mavjud.
"""
import threading
import queue
import time

numbers = queue.Queue()

for i in range(1, 21):
    numbers.put(i)

def process_odd_numbers(q):
    while not q.empty():
        num = q.get()
        if num % 2 == 1:
            print(f"[Toq Thread] {num} ni qayta ishlayapti...")
            time.sleep(0.1)
        q.task_done()

def process_even_numbers(q):
    while not q.empty():
        num = q.get()
        if num % 2 == 0:
            print(f"[Juft Thread] {num} ni qayta ishlayapti...")
            time.sleep(0.1)
        q.task_done()

odd_thread = threading.Thread(target=process_odd_numbers, args=(numbers,))
even_thread = threading.Thread(target=process_even_numbers, args=(numbers,))

odd_thread.start()
even_thread.start()

odd_thread.join()
even_thread.join()

print("Barcha sonlar qayta ishlanib bo‘ldi!")
