# 2.ls -l natijasidan faqat .py fayllarni ajratib, yangi faylga yozib qo‘ying.

import os

files = os.listdir(".")

with open("py_files.txt", "w") as f:
    for filename in files:
        if filename.endswith(".py"):
            stat = os.stat(filename)r
            permissions = oct(stat.st_mode)[-3:]
            size = stat.st_size / 1024
            f.write(f"{permissions} {size:>8} {filename}\n")

print("py_files.txt faylga .py fayllar yozildi")
