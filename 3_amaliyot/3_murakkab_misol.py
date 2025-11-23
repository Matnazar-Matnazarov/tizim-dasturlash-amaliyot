"""
1.Project nomli papka yarating va unga barcha foydalanuvchilarga Read & Execute huquqi bering.
"""


import os
import stat
import shutil

folder = "Project"

if os.path.exists(folder):
    shutil.rmtree(folder)

os.makedirs(folder)

before_mode = os.stat(folder).st_mode
print("Oldin (ls uslubida):", stat.filemode(before_mode))

# 755 huquq berish -> owner: rwx, group: r-x, others: r-x
os.chmod(folder, 0o755)

after_mode = os.stat(folder).st_mode
print("Keyin (ls uslubida):", stat.filemode(after_mode))


