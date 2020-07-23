import csv
from drivers import *
import RPi.GPIO as GPIO
import numpy
import math
import time
import socket
numpy.set_printoptions(suppress=True)
GPIO.setmode(GPIO.BCM)
h = SerialMeter(6,[19,26,13])
global base, k, W, g, Wb,B0,Ro,jj
Wb = 896.4
g = W = Wa = B0 = i = j = Ro = jj = k =0
r = 183      # 支撑半径                                                                                                                                                                                     
R = 200      # 砂轮直径                                                                                                                                                                                     
base = [1, 1, 1]
def get_k():
    global base, k, W, g, Wb,B0,Ro,jj
    print("请校准平衡器")
    time.sleep(3)
    base = h.getdv(nrep=50)
    print("请在10秒内放上 标准盘")
    time.sleep(10)
    read = (h.getdv(nrep=10)-base)
    k = read/Wb
    print('请在10秒内拿开 标准盘')
    time.sleep(10)
    print('base:', base, "k:", k)
    print("可以测试产品了")
    with open("data_k.csv", "a") as datafile:
        datafile.write(time.strftime("%Y-%m-%d-%H-%M-%S"))
        datafile.write(", %d"%k[0])
        datafile.write(", %d"%k[1])
        datafile.write(", %d"%k[2])
        datafile.write(", %d"%base[0])
        datafile.write(", %d"%base[1])
        datafile.write(", %d"%base[2])
        datafile.write(", %d\n"%Wb)
    return k, base

def get_k0():
    global base, k, W, g, Wb,B0,Ro,jj
    print("校准平衡器中")
    f = open('data_k.csv')
    L=list(csv.reader(f))
    for j in range(1, 2):    #第j行                                                                                                                                                                         
        k = [int(L[j][1]), int(L[j][2]), int(L[j][3])]
        base = [int(L[j][4]), int(L[j][5]), int(L[j][6])]
        list1 = [{'weight', k[0]}]
        # list1 = [{'weight':W}]                          
        W = int(L[j][7])
        j += 1
    print(k,base)
    print("k[0]", k[0])
    return k, base
def con_f():
    global base, k, W, g, Wb, B0, jj
    con = True
    try:
        while con:
            m = (h.getdv(nrep=10) - base)/k/3
            W = m[0] + m[1] + m[2]
            if W > 0.8 * Wb:
                con = False
    except KeyboardInterrupt:
        return

def con_end():
    global base, k, W, g, Wb, B0, jj
    con = True
    try:
        while con:
            m = (h.getdv(nrep=10) - base)/k/3
            W = m[0] + m[1] + m[2]
            if W < 0.3 * Wb:
                con = False
    except KeyboardInterrupt:
        return

def get_g(jj):
    global base, k, W, g, Wb, B0
    time.sleep(0.5)
    m1 = (h.getdv(nrep=10) - base)/k/3
    W = m1[0] + m1[1] + m1[2]
    x = (1.5*m1[0]/W-0.5)*r
    y = r*(3*m1[2]/W-1)/math.sqrt(3)-x/math.sqrt(3)
    d = math.sqrt(x*x + y*y)
    g = d*W/R
    if x == 0 and y == 0:
        B0 = 0
        # print("0,y=0")                                                                                                                                                                                    
    elif x == 0 and y > 0:
        B0 = math.pi/2
        # print("0,y>0")                                                                                                                                                                                    
    elif x == 0 and y < 0:
        B0 = 1.5*math.pi
        # print("0,y<0")                                                                                                                                                                                    
    elif x > 0 and y >= 0:
        B0 = math.atan(y/x)
        # print("x>0,y>=0")                                                                                                                                                                                 
    elif x > 0 and y < 0:
        B0 = 2*math.pi+math.atan(y/x)
        # print("x>0,Y<0")                                                                                                                                                                                  
    elif x < 0 and y >=0:
        B0 = math.pi + math.atan(y/x)
        # print("x<0,y>=0")                                                                                                                                                                                 
    elif x < 0 and y < 0:
        B0 = math.pi + math.atan(y/x)
        # print("x<0,y<0")                                                                                                                                                                                  
    else:
        pass
    print( "g=", int(g*100)/100, "W:", W, "B0=", int((B0*10000)/10000*180/math.pi))
    with open("data.csv", "a") as datafile:
        datafile.write(time.strftime("%Y-%m-%d-%H-%M-%S"))
        datafile.write(", %d"%jj)
        datafile.write(", %d"%g)
        datafile.write(", %.02f"%B0)
        datafile.write(", %d"%(round(B0*180/math.pi)))
        datafile.write(", %.01f"%x)
        datafile.write(", %.01f"%y)
        datafile.write(", %.01f"%d)
        datafile.write(", %0.2f"%(g*(math.sin(B0))))
        datafile.write(", %0.1f"%(int(m1[0])))
        datafile.write(", %0.1f"%(int(m1[1])))
        datafile.write(", %0.1f"%(int(m1[2])))
        datafile.write(", %d\n"%W)
    return

if __name__=='__main__':
    GPIO.setmode(GPIO.BCM)

    h = SerialMeter(6,[19,26,13])

