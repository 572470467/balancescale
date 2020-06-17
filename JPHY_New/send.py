import socket
import RPi.GPIO as GPIO
from balancer import *
import csv
s = socket.socket()
s.bind((socket.gethostname(), 50053))
s.listen(5)
conn, addr = s.accept()
def op_balancer_test():
    jj=0
    while True:
        data=conn.recv(1024)
        n=(data).decode('utf-8')
        if int(n)==1:
            jj+=1
            con_end()
            con_f()
            get_g(jj)
if __name__=='__main__':
    op_balancer_test()


