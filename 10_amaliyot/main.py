"""
10 ta og‘ir CPU-bound vazifani (masalan, fibonacci(n) yoki matrix multiplication) ProcessPoolExecutor orqali bajaring va umumiy vaqtni solishtiring.
"""

import time
from concurrent.futures import ProcessPoolExecutor

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

if __name__ == "__main__":
    tasks = [50, 52, 53, 51, 54, 55, 56, 57, 58, 59]

    start_seq = time.perf_counter()
    seq_results = [fibonacci(n) for n in tasks]
    end_seq = time.perf_counter()

    start_par = time.perf_counter()
    with ProcessPoolExecutor(max_workers=8) as executor:
        par_results = list(executor.map(fibonacci, tasks))
    end_par = time.perf_counter()

    print(f"Ketma-ket bajarish vaqti: {end_seq - start_seq:.4f} s")
    print(f"Parallel bajarish vaqti:   {end_par - start_par:.4f} s")
    print("Natijalar to‘g‘ri:", seq_results == par_results)
