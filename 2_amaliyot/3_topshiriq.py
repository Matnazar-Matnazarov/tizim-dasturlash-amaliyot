"""
8.subprocess yordamida tashqi buyruqni bajarish va natijasini faylga yozish.
"""

import subprocess

subprocess.run(input("Buyruqni kiriting: ").split(), stdout=open("output.txt", "w"))