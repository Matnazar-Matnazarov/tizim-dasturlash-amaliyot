#1.Faylni 4 ta bo‘lakka bo‘lib, har bir bo‘lakda thread orqali qidiruv qiling.

import mmap
from concurrent.futures import ThreadPoolExecutor

def search_chunk(mm, pat, start, end):
    res = []
    pos = mm.find(pat, start, end)
    while pos != -1:
        res.append(pos)
        pos = mm.find(pat, pos + 1, end)
    return res

def parallel_search(file, a, workers=4):
    a = a.encode()
    with open(file, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        size = mm.size()

        chunk = size // workers
        re = len(a) - 1
        ranges = []

        for i in range(workers):
            s = i * chunk
            e = s + chunk if i < workers - 1 else size
            if i > 0: s -= re
            if i < workers - 1: e += re
            ranges.append((s, e))

        results = []
        with ThreadPoolExecutor(workers) as ex:
            for r in ex.map(lambda x: search_chunk(mm, a, x[0], x[1]), ranges):
                results.extend(r)

        mm.close()
        return sorted(set(results))

if __name__ == "__main__":
    offs = parallel_search("big.txt", "ERROR")
    print("Topildi:", offs)
    with open("big.txt", "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        for off in offs:
            mm.seek(off)
            print(mm.readline().decode().rstrip())

        mm.close()

