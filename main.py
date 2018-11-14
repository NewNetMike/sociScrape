import threading
from config import *
from importlib import import_module

threads = []
for c in configs.items():
    threads.append(threading.Thread(target=import_module(c[1]['script_loc']).go, args=[c[1]]))

for t in threads:
    t.start()