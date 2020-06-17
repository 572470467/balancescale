from tkinter import *
import pygame
import datetime
import os
import threading
import time
import math
import csv
import json
from point import Point
from pygame.locals import *
import urllib.request
from pygame.color import THECOLORS
import socket
from balancer import *
pygame.init()
page=1
start=0
degree=0
scope='当日'
dg = 4; Wb = 896.4; dW = 4
J=0
Black=[0,0,0]
White=[255,255,255]
Green=[0,255,0]
Red=[255,0,0]
Blue=[5,39,175]
list0=[120,100,80,60,40,20]
list1=[['400',50,30],['230',140,120],['180',230,210],['150',320,300],['125',410,390]]
list2=[[120,200,360,200],[240,80,240,320],[180,96.08,300,303.9],[136.08,140,343.92,260],[300,96.08,180,303.92],[343.92,140,136.08,260]]
list3 = [['a',30],['b',120],['c',210],['d',300],['e',390]]
list4=[['0°',235,55],['30°',297,72],['60°',350,120],['90°',365,190],['120°',350,250],['150°',295,305],['180°',220,320],['210°',150,305],['240°',95,255],['270°',70,190],['300°',95,120],['330°',155,72]]
condition0=[["砂轮重量(w)：",400,395],["平 衡 值 (g)：",460,455],["重 点 角 度：",520,515],["数    量   (j)：",580,575]]
button0=[["测  试",30,46,350],["默认校准",140,142,350],["标准校准",250,252,350],["统  计",360,376,350],["查看异常",195,197,410]]
button1=[["开始测试",80,715,110,94,719],["返回主界面",280,715,110,286,719]]
button2=[["当日数据",30,32],["本周数据",140,142],["本月数据",250,252],["本年数据",360,362]]
text_0=pygame.font.Font("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",24)
text_1=pygame.font.Font("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",20)
text_2=pygame.font.Font("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",18)
text_3=pygame.font.Font("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",16)
os.environ['SDL_VIDEO_WINDOW_POS']= "%d,%d" % (67,27)
screen = pygame.display.set_mode((480,800))
screen.fill(White)
pygame.display.update()
s = socket.socket()
s.connect((socket.gethostname(),50053))
class Balance(object):
    def Main(): #静平衡仪主界面部分
        pygame.draw.rect(screen,White,[0,0,480,800],0)
        pygame.draw.rect(screen,Black,[0,200,480,300],0)
        text_fmt=text_0.render("静平衡仪主控制界面",2,White)
        screen.blit(text_fmt,(130,220))
        for z in button0:
            pygame.draw.rect(screen,Green,[z[1],z[3],85,30],0)
            text_fmt=text_1.render(z[0],2,Black)
            screen.blit(text_fmt,(z[2],z[3]+2))
        pygame.display.update()
    def Test():#静平衡仪测试界面部分
        pygame.draw.rect(screen,Black,[0,0,480,800],0)
        text_fmt=text_0.render("静平衡仪测试界面",2,White)
        screen.blit(text_fmt,(153,23))
        pygame.draw.circle(screen,White,(240,200),118,0)
        for g in list4:
            text_fmt=text_1.render(g[0],2,White)
            screen.blit(text_fmt,(g[1],g[2]))
        for c in list2:
            pygame.draw.aaline(screen,Black,(c[0],c[1]),(c[2],c[3]))
        for i in list0:
            pygame.draw.circle(screen,Blue,(240,200),i,2)
        text_fmt=text_1.render("砂轮情况：",2,White)
        screen.blit(text_fmt,(20,360))
        for v in condition0:
            text_fmt=text_1.render(v[0],2,White)
            screen.blit(text_fmt,(90,v[1]))
            pygame.draw.rect(screen,White,[230,v[2],90,35],2)
        text_fmt=text_1.render("选择砂轮直径:",2,White)
        screen.blit(text_fmt,(20,620))
        for f in list1:
            text_fmt=text_1.render(f[0],2,White)
            screen.blit(text_fmt,(f[1],645))
            pygame.draw.circle(screen,White,(f[2],658),10,1)
            #screen.blit(text_fmt,(f[1],665))
            #pygame.draw.circle(screen,White,(f[2],678),10,1)
        #pygame.draw.rect(screen,Green,[170,735,110,35],0)
        pygame.draw.rect(screen,Green,[170,675,110,35],0)
        text_fmt=text_1.render("返回主界面",2,Black)
        screen.blit(text_fmt,(176,679))
        #screen.blit(text_fmt,(176,739))
        #pygame.draw.circle(screen,White,(30,678),4,0)
        pygame.draw.circle(screen,White,(30,658),4,0)
        pygame.display.update()
    def Show():
        response=urllib.request.urlopen("http://localhost:5000/balance/measure/")
        html=response.read().decode()
        text=json.loads(html)
        list=[[text['weight'],395],[text['balance'],455],[text['angle'],515],[text['J'],575]]
        pygame.draw.circle(screen,White,(240,200),118,0)
        for t in list2:
            pygame.draw.aaline(screen,Black,(t[0],t[1]),(t[2],t[3]))
        for i in list0:
            pygame.draw.circle(screen,Blue,(240,200),i,2)
        degree=float(text['angle'])
        Balance.Radar(degree)
        for g in list:
            pygame.draw.rect(screen,Black,[232,g[1]+2,86,31],0)
            text_fmt=text_1.render('{}'.format(g[0]),2,White)
            screen.blit(text_fmt,(240,g[1]))
        pygame.draw.rect(screen,Black,[365,390,80,250],0)
        if Wb + dW < int(float(text['weight'])):
            pygame.draw.rect(screen,Red,[365,395,80,35],0)
            text_fmt=text_2.render("重量超重",2,Black)
            screen.blit(text_fmt,(369,400))
            pygame.display.update()
        if int(float(text['weight'])) < Wb - dW:
            pygame.draw.rect(screen,Red,[365,395,80,35],0)
            text_fmt=text_2.render("重量超轻",2,Black)
            screen.blit(text_fmt,(369,400))
            pygame.display.update()
        if int(float(text['balance'])) > dg:
            pygame.draw.rect(screen,Red,[365,450,80,35],0)
            text_fmt=text_2.render("平衡超差",2,Black)
            screen.blit(text_fmt,(369,455))
            pygame.display.update()
        elif int(float(text['balance']))<=dg and Wb - dW<=int(float(text['weight']))<=Wb + dW:
            pygame.draw.rect(screen,Green,[365,470,80,35],0)
            text_fmt=text_2.render("正常砂轮",2,Black)
            screen.blit(text_fmt,(369,475))
            pygame.display.update()
    def Calibration():#静平衡仪校准界面部分
        pygame.draw.rect(screen,Black,[0,0,480,800],0)
        text_fmt=text_0.render("静平衡仪校准界面",2,White)
        screen.blit(text_fmt,(153,23))
        pygame.draw.circle(screen,White,(240,200),118,0)
        for g in list4:
            text_fmt=text_1.render(g[0],2,White)
            screen.blit(text_fmt,(g[1],g[2]))
        for c in list2:
            pygame.draw.aaline(screen,Black,(c[0],c[1]),(c[2],c[3]))
        for i in list0:
            pygame.draw.circle(screen,Blue,(240,200),i,2)
        text_fmt=text_1.render("标准砂轮情况：",2,White)
        screen.blit(text_fmt,(20,360))
        text_fmt=text_1.render("标准砂轮重量(w)：",2,White)
        screen.blit(text_fmt,(90,400))
        pygame.draw.rect(screen,White,[270,395,90,35],2)
        pygame.draw.rect(screen,Green,[170,605,110,35],0)
        text_fmt=text_1.render("返回主界面",2,Black)
        screen.blit(text_fmt,(176,609))
        pygame.display.update()
    def Statistics(jm,sj):#静平衡仪查看界面部分或查看砂轮异常数据
        pygame.draw.rect(screen,Black,[0,0,480,800],0)
        text_fmt=text_0.render(jm,2,White)
        screen.blit(text_fmt,(153,23))
        text_fmt=text_1.render(sj,2,White)
        screen.blit(text_fmt,(20,73))
        pygame.draw.rect(screen,White,[40,120,400,500],0)
        list=[["测试日期",55],["砂轮重量",160],["平衡值",265],["重点角度",355]]
        for i in list:
            text_fmt=text_2.render(i[0],2,Black)
            screen.blit(text_fmt,(i[1],125))
        for q in button2:
            pygame.draw.rect(screen,Green,[q[1],677,85,30],0)
            text_fmt=text_1.render(q[0],2,Black)
            screen.blit(text_fmt,(q[2],679))
        pygame.draw.rect(screen,Green,[170,715,110,35],0)
        text_fmt=text_1.render("返回主界面",2,Black)
        screen.blit(text_fmt,(176,719))
        pygame.display.update()
    def flip_over(page,lt):#翻页
        for i in range(len(lt)):
            if len(lt)%19!=0:
                n=(len(lt)+1)//19+1
            elif len(lt)%19==0:
                n=(len(lt)+1)//19
            if int((page-1)*19)<=i<=int(page*19-1) and 1<page<=n and n!=1:
                text_fmt=text_3.render('{}/{}页'.format(page,n),2,White)
                screen.blit(text_fmt,(270,635))
                ls=[["{}".format(lt[i][0][0:10]),55],["{}".format(lt[i][12]),175],["{}".format(lt[i][2]),285],["{}".format(lt[i][4]),375]]
                for t in ls:
                    text_fmt=text_3.render(t[0],2,Black)
                    screen.blit(text_fmt,(t[1],150+(i-(page-1)*19)*25))
                pygame.draw.rect(screen,Green,[335,634,55,24],0)
                text_fmt=text_3.render('上一页',2,Black)
                screen.blit(text_fmt,(337,636))
            elif page>n and int((n-1)*19)<=i<=int(n*19-1) and n!=1:
                text_fmt=text_3.render('{}/{}页'.format(n,n),2,White)
                screen.blit(text_fmt,(270,635))
                ls=[["{}".format(lt[i][0][0:10]),55],["{}".format(lt[i][12]),175],["{}".format(lt[i][2]),285],["{}".format(lt[i][4]),375]]
                for t in ls:
                    text_fmt=text_3.render(t[0],2,Black)
                    screen.blit(text_fmt,(t[1],150+(i-(n-1)*19)*25))
                pygame.draw.rect(screen,Green,[335,634,55,24],0)
                text_fmt=text_3.render('上一页',2,Black)
                screen.blit(text_fmt,(337,636))
            elif page==1 and int((page-1)*19)<=i<=int(page*19-1):
                text_fmt=text_3.render('{}/{}页'.format(page,n),2,White)
                screen.blit(text_fmt,(340,635))
                ls=[["{}".format(lt[i][0][0:10]),55],["{}".format(lt[i][12]),175],["{}".format(lt[i][2]),285],["{}".format(lt[i][4]),375]]
                for t in ls:
                    text_fmt=text_3.render(t[0],2,Black)
                    screen.blit(text_fmt,(t[1],150+(i-(page-1)*19)*25))
            elif n==1:
                text_fmt=text_3.render('{}/{}页'.format(1,1),2,White)
                screen.blit(text_fmt,(340,635))
                ls=[["{}".format(lt[i][0][0:10]),55],["{}".format(lt[i][12]),175],["{}".format(lt[i][2]),285],["{}".format(lt[i][4]),375]]
                for t in ls:
                    text_fmt=text_3.render(t[0],2,Black)
                    screen.blit(text_fmt,(t[1],150+i*25))
            pygame.draw.rect(screen,Green,[400,634,55,24],0)
            text_fmt=text_3.render('下一页',2,Black)
            screen.blit(text_fmt,(402,636))
    def Radar(degree):#雷达图
        radar = (240,200)
        radar_len = 118
        x = radar[0] + math.sin(math.radians(degree)) * radar_len
        y = radar[1] - math.cos(math.radians(degree)) * radar_len
        pygame.draw.line(screen, Color("red"), radar, (x,y), 2)
        pygame.display.flip()
    def Today(page):#当日数据
        pygame.draw.rect(screen,Black,[40,630,480,30],0)
        pygame.draw.rect(screen,White,[40,150,400,470],0)
        day=time.strftime("%Y-%m-%d")
        y=open('data.csv','r')
        reader=csv.reader(y)
        lt=[]
        if start==3:
            for a in reader:
                if a[0][0:10]==day:
                    lt.append(a)
        elif start==4:
            for a in reader:
                if a[0][0:10]==day:
                    if int(a[4]) > dg or Wb + dW < int(a[12]) or int(a[12]) < Wb - dW:
                        lt.append(a)            
        Balance.flip_over(page,lt)
    def Week(page):#本周数据
        pygame.draw.rect(screen,Black,[40,630,480,30],0)
        pygame.draw.rect(screen,White,[40,150,400,470],0)
        today = datetime.date.today()
        week_start_day =today-datetime.timedelta(days=today.weekday())     
        week_end_day =today+datetime.timedelta(days=today.weekday())
        y=open('data.csv','r')
        reader=csv.reader(y)
        lt=[]
        if start==3:
            for a in reader:
                if str(week_start_day)<=a[0][0:10]<=str(week_end_day):
                    lt.append(a)
        elif start==4:
            for a in reader:
                if str(week_start_day)<=a[0][0:10]<=str(week_end_day):
                    if int(a[4]) > dg or Wb + dW < int(a[12]) or int(a[12]) < Wb - dW:
                        lt.append(a)
        Balance.flip_over(page,lt)
    def Moon(page):#本月数据
        pygame.draw.rect(screen,Black,[40,630,480,30],0)
        pygame.draw.rect(screen,White,[40,150,400,470],0)
        week=time.strftime("%Y-%m")
        y=open('data.csv','r')
        reader=csv.reader(y)
        lt=[]
        if start==3:
            for a in reader:
                if a[0][0:7]==week:
                    lt.append(a)
        elif start==4:
            for a in reader:
                if a[0][0:7]==week:
                    if int(a[4]) > dg or Wb + dW < int(a[12]) or int(a[12]) < Wb - dW:
                        lt.append(a)
        Balance.flip_over(page,lt)
    def Year(page):#本年数据
        pygame.draw.rect(screen,Black,[40,630,480,30],0)
        pygame.draw.rect(screen,White,[40,150,400,470],0)
        year=time.strftime("%Y")
        y=open('data.csv','r')
        reader=csv.reader(y)
        lt=[]
        if start==3:
            for a in reader:
                if a[0][0:4]==year:
                    lt.append(a)
        if start==4:
            for a in reader:
                if a[0][0:4]==year:
                    if int(a[4]) > dg or Wb + dW < int(a[12]) or int(a[12]) < Wb - dW:
                        lt.append(a)
        Balance.flip_over(page,lt)      
if __name__ == '__main__':
    Balance.Main()
    while True:
        if start==1:
            s.sendall(str(1).encode('utf-8'))
            Balance.Show()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
            elif event.type == QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                pos = pygame.mouse.get_pos()
                for c in list3:
                    #c[0]=Point().area([pos[0],pos[1]],[c[1],678])
                    c[0]=Point().area([pos[0],pos[1]],[c[1],658])
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index==0:
                            if 140<=pos[0]<=225 and 350<=pos[1]<=380 and start==0:#默认测试按钮
                                response=urllib.request.urlopen("http://localhost:5000/balance/calibrate0/")
                            elif 250<=pos[0]<=335 and 350<=pos[1]<=380 and start==0:#标准校准按钮
                                start=2
                                Balance.Calibration()
                                Balance.Radar(degree)
                                response=urllib.request.urlopen("http://localhost:5000/balance/calibrate/")
                                html=response.read().decode()
                                text=json.loads(html)
                                pygame.draw.rect(screen,Black,[272,397,86,31],0)
                                text_fmt=text_1.render('{}'.format(text['weight']),2,White)
                                screen.blit(text_fmt,(290,395))
                            elif 30<=pos[0]<=115 and 350<=pos[1]<=380 and start==0:#测试按钮
                                start=1
                                Balance.Test()
                                #con_end()
                                #con_f()
                                #get_g(0)
                                
                            elif 360<=pos[0]<=445 and 350<=pos[1]<=380 and start==0:#查看按钮
                                start=3
                                jm="静平衡仪统计界面"
                                sj="砂轮历史数据："
                                Balance.Statistics(jm,sj)
                            elif 195<=pos[0]<=280 and 410<=pos[1]<=440 and start==0:#查看异常按钮
                                start=4
                                jm="砂轮异常统计界面"
                                sj="砂轮异常数据："
                                Balance.Statistics(jm,sj)
                            elif 170<=pos[0]<=280 and 605<=pos[1]<=640 and start==2:#校准界面返回按钮
                                start=0
                                Balance.Main()
                            elif 170<=pos[0]<=280 and 675<=pos[1]<=700 and start==1:#测试界面返回按钮
                            #elif 170<=pos[0]<=280 and 735<=pos[1]<=760 and start==1:#测试界面返回按钮
                                start=0
                                Balance.Main()                                
                            elif start==3 or start==4:
                                if 180<=pos[0]<=290 and 715<=pos[1]<=750:#查看界面返回按钮
                                    start=0
                                    Balance.Main()
                                elif 55<=pos[0]<=140 and 677<=pos[1]<=707:#当日数据按钮
                                    page=1
                                    scope='当日'
                                    Balance.Today(page)
                                elif 140<=pos[0]<=225 and 677<=pos[1]<=707:#本周数据按钮
                                    page=1
                                    scope='本周'
                                    Balance.Week(page)
                                elif 250<=pos[0]<=335 and 677<=pos[1]<=707:#本月数据按钮
                                    page=1
                                    scope='本月'
                                    Balance.Moon(page)
                                elif 360<=pos[0]<=445 and 677<=pos[1]<=707:#本年数据按钮
                                    page=1
                                    scope='本年'
                                    Balance.Year(page)
                            if 400<=pos[0]<=455 and 634<=pos[1]<=658:#下一页按钮
                                if start==3 or start==4:
                                    page+=1
                                    if scope=='当日':
                                        Balance.Today(page)
                                    elif scope=='本周':
                                        Balance.Week(page)
                                    elif scope=='本月':
                                        Balance.Moon(page)
                                    elif scope=='本年':
                                        Balance.Year(page)
                            elif 337<=pos[0]<=392 and 634<=pos[1]<=658 and page!=1:#上一页按钮
                                if start==3 or start==4:
                                    page-=1
                                    if scope=='当日':
                                        Balance.Today(page)
                                    elif scope=='本周':
                                        Balance.Week(page)
                                    elif scope=='本月':
                                        Balance.Moon(page)
                                    elif scope=='本年':
                                        Balance.Year(page)
                            for e in list3:
                                if e[0]<=10 and start==1:
                                    #pygame.draw.circle(screen,Black,(30,678),4,0)
                                    #pygame.draw.circle(screen,Black,(120,678),4,0)
                                    #pygame.draw.circle(screen,Black,(210,678),4,0)
                                    #pygame.draw.circle(screen,Black,(300,678),4,0)
                                    #pygame.draw.circle(screen,Black,(390,678),4,0)
                                    #pygame.draw.circle(screen,White,(e[1],678),4,0)
                                    pygame.draw.circle(screen,Black,(30,658),4,0)
                                    pygame.draw.circle(screen,Black,(120,658),4,0)
                                    pygame.draw.circle(screen,Black,(210,658),4,0)
                                    pygame.draw.circle(screen,Black,(300,658),4,0)
                                    pygame.draw.circle(screen,Black,(390,658),4,0)
                                    pygame.draw.circle(screen,White,(e[1],658),4,0)
            pygame.display.update()
