import os
import threading
def A():
    os.system('python3 interface.py')
def B():
    os.system('python3 send.py')
def C():
    os.system('python3 scalegui.py')
def state():
    threads=[]
    threads.append(threading.Thread(target=A))
    threads.append(threading.Thread(target=B))
    threads.append(threading.Thread(target=C))
    for t in threads:
        #t.setDaemon(True)
        t.start()
if __name__ == '__main__':
    state()

