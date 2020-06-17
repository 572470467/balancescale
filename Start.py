import os
import threading
def A():
    os.system('python3 interface.py')
def B():
    os.system('python3 scalegui.py')
def state():
    threads=[]
    threads.append(threading.Thread(target=A))
    threads.append(threading.Thread(target=B))
    for t in threads:
        #t.setDaemon(True)
        t.start()
state()
