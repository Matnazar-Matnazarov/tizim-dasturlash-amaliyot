"""
9.Disk bo‘sh joyini aniqlash – joriy disk bo‘sh joyini aniqlash va foiz ko‘rinishida ko‘rsatish.
"""

import shutil

# Disk haqida ma'lumot olish (joriy katalog joylashgan disk)
total, used, free = shutil.disk_usage(".")

# Byte -> GB aylantirish
total_gb = total / (1024**3)
used_gb = used / (1024**3)
free_gb = free / (1024**3)

# Bo‘sh joy foizini hisoblash
free_percent = (free / total) * 100

print(f"Umumiy hajm: {total_gb:.2f} GB")
print(f"Ishlatilgan: {used_gb:.2f} GB")
print(f"Bo‘sh joy: {free_gb:.2f} GB")

print(f"Bo‘sh joy foizi: {free_percent:.2f}%")
