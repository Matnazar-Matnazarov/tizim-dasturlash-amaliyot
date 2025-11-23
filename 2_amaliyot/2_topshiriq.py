"""
7.Papkadagi fayllarni hajmiga qarab saralash va ro‘yxatini chiqarish.
"""

import os

files = os.listdir(".")
files.sort(key=lambda x: os.path.getsize(x), reverse=True)

for file in files:
    print(file, os.path.getsize(file), "bytes")