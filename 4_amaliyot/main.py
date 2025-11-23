"""
8.rayonning PID sini olib, uni kill (Linux) yoki taskkill (Windows) bilan to‘xtatadigan dastur yozing.
"""

import platform
import subprocess
import time

if platform.system().lower() == "windows":
    proc = subprocess.Popen(["timeout", "30"], shell=True)
else:
    proc = subprocess.Popen(["sleep", "30"])

print(f"Jarayon ishga tushdi, PID: {proc.pid}")

time.sleep(2)

pid = proc.pid
cmd = ["taskkill", "/PID", str(pid), "/F"] if platform.system().lower() == "windows" else ["kill", "-TERM", str(pid)]

try:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"PID {pid} muvaffaqiyatli to'xtatildi.")
    else:
        print(result.stdout or result.stderr or f"Buyruq xatolik kodi: {result.returncode}")
except FileNotFoundError:
    tool = "taskkill" if platform.system().lower() == "windows" else "kill"
    print(f"Xatolik: '{tool}' utilitasi topilmadi.")
except Exception as e:
    print(f"Kutilmagan xatolik: {e}")
