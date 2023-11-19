import random
from pathlib import Path

_PWD_PATH = Path('./pwd.txt')
if _PWD_PATH.exists():
    PASSWORD = _PWD_PATH.read_text().strip()
else:
    PASSWORD = str(random.randrange(10**5, 10**6))

print(PASSWORD)
