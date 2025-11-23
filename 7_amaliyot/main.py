"""
4.Thread’lar yordamida bir nechta URL’dan parallel ma’lumot yuklab oling (requests + threading).
"""
import requests
import time
from concurrent.futures import ThreadPoolExecutor

urls = ["https://www.google.com", "https://www.youtube.com", "https://www.facebook.com"] * 10

def download_url(url):
    response = requests.get(url, timeout=5)
    return response.status_code

def thread_func():
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(download_url, urls))
    return results

def func():
    return [download_url(url) for url in urls]

start_time = time.time()
thread_func()
end_time = time.time()
print(f"Threaded time: {end_time - start_time:.2f} seconds")

start_time = time.time()
func()
end_time = time.time()
print(f"oddiy funksiya time: {end_time - start_time:.2f} seconds")
