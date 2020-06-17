from drivers import *
import RPi.GPIO as GPIO
import numpy
import math


numpy.set_printoptions(suppress=True)

GPIO.setmode(GPIO.BCM)
h = SerialMeter(6,[13,19,26])
s = Stepper(14,15,18)

global base, k, W, g, Wb,B0

Wb = 896.4

def get_k():
    global base, k , W, g, Wa
    print("请校准平衡器")
    time.sleep(3)
    base = h.getdv(nrep=50)
    print("请在10秒内放上 标准盘")
    time.sleep(10)
    read = (h.getdv(nrep=10)-base)
    k = read/Wb
    print('请在10秒内拿开 标准盘')
    time.sleep(10)
    # print('base:', base, "k:", k)                                                                                                                                                                         
    print("可以测试产品了")
    return k, base

def get_W_g():
    g = W = Wa = B0 = i = j = Ro = 0
    r = 183      # 支撑半径                                                                                                                                                                                 
    R = 200      # 砂轮直径                                                                                                                                                                                 

    print("get_k()",get_k())
    while True:
        try:
            time.sleep(1)
            m = (h.getdv(nrep=10) - base)/k/3
            W = m[0] + m[1] + m[2]
            # print("???/W/Wa:", W, Wa)                                                                                                                                                                     
            if W > 100 and  W - Wa > 100:
                time.sleep(0.5)
                for i in range(1):
                    print("No.", j)
                    time.sleep(0.5)
                    m1 = (h.getdv(nrep=10) - base)/k/3
                    W = m1[0] + m1[1] + m1[2]
                    # print("W",W)        
                    x = (1.5*m1[0]/W-0.5)*r
                    y = r-3*r*m1[1]/W-x
                    # y = r+3*r*w1/W-x                                                                                                                                                                      
                    d = math.sqrt(x*x + y*y)
                    g = d*W/R

                    if x == 0 and y == 0:
                        B0 = 0
                        print("0,y=0")
                    elif x == 0 and y > 0:
                        B0 = math.pi/2
                        print("0,y>0")
                    elif x == 0 and y < 0:
                        B0 = 1.5*math.pi
                        print("0,y<0")
                    elif x > 0 and y >= 0:
                        B0 = math.atan(y/x)
                        print("x>0,y>=0")
                    elif x > 0 and y < 0:
                        B0 = 2*math.pi+math.atan(y/x)
                        print("x>0,Y<0")
                    elif x < 0 and y >=0:
                        B0 = math.pi + math.atan(y/x)
                        print("x<0,y>=0")
                    elif x <0 and y < 0:
                        B0 = math.pi + math.atan(y/x)
                        print("x<0,y<0")
                    else:
                        B0 = math.pi + math.atan(y/x)
                        print("x<0,y<0")
                    else:
                        pass
                    print( "g=", int(g*100)/100, "W:", W, "m1:", m1)
                    print( "B0=", int((B0*10000)/10000*180/math.pi),"x,y:", x,y)

                    Ro = B0 - Ro
                    if Ro >= 0:
                        d = 0
                    else:
                        d = 1
                    print("Ro", Ro, "step:", round(abs(Ro)*100/math.pi))
                    s.rotate(d, round(abs(Ro)*100/math.pi))

                    with open("data.csv", "a") as datafile:
                        datafile.write(time.strftime("%Y-%m-%d-%H-%M-%S"))
                        datafile.write(", %d"%j)
                        datafile.write(", %d"%g)
                        datafile.write(", %.02f"%B0)
                        datafile.write(", %0.2f"%(B0*180/math.pi))
                        datafile.write(", %.01f"%x)
                        datafile.write(", %.01f"%y)
                        datafile.write(", %.01f"%d)
                        datafile.write(", %0.2f"%(g*(math.sin(B0))))
                        datafile.write(", %0.1f"%(int(m1[0])))
                        datafile.write(", %0.1f"%(int(m1[1])))
                        datafile.write(", %0.1f"%(int(m1[2])))
                        datafile.write(", %d\n"%W)
                    i = i +1
                j = j + 1
            else:
                pass
            Wa = W
        except KeyboardInterrupt:
            GPIO.cleanup()

if __name__=='__main__':
    GPIO.setmode(GPIO.BCM)

    h = SerialMeter(6,[13,19,26])
    g = Wa = B0 = 0
    r = 183; R = 200

    get_W_g()



