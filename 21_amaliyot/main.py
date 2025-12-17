"""
24.C kutubxonasidan pow funksiyasini chaqirib, haqiqiy sonning darajasini hisoblang. shuni ishla
"""

from ctypes import CDLL, c_double
from ctypes.util import find_library
import sys

if sys.platform.startswith(("linux", "darwin")):
    libm_path = find_library("m")   # Linux/macOS
    if not libm_path:
        raise RuntimeError("libm topilmadi!")
    lib = CDLL(libm_path)
else:  # Windows
    lib = CDLL("msvcrt")

lib.pow.argtypes = [c_double, c_double]
lib.pow.restype  = c_double

a = 2
b = 3
c = lib.pow(a, b)
print(f"{a}^{b} = {c}")
