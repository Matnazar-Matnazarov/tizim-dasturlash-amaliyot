"""
2.Parallel hisoblash jarayonida CPU foydalanuvchi vaqtini o‘lchang (time.perf_counter()).
"""

import time
from multiprocessing import Pool

def square(x):
    return x * x

if __name__ == "__main__":
    n = 1_100_000  
    data = range(n)

    start_time = time.perf_counter()  

    with Pool(8) as p:
        result = p.map(square, data)

    end_time = time.perf_counter() 
    elapsed = end_time - start_time

    print(f"⏱ CPU foydalanuvchi vaqti (Pool(8)): {elapsed:.4f} soniya")
