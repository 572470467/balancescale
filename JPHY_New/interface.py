import os
import sys
from balancer import *
from flask import Flask, jsonify
import csv

app = Flask(__name__)

def balancer_test():
    text()
    dic = {}
    for i in range(2):
        dic[str(i)] = str(random.randrange(5))
    return dic[str(i)]

@app.route('/balance/measure/')
def op_balancer_test():
    f = open('data.csv')
    L=list(csv.reader(f))
    for i in range(len(L)-1,len(L)):#第j行
        J = int(L[i][1])
        g = int(L[i][2])
        b0 = int(L[i][4])
        W = int(L[i][12])
        i += 1
        list0 = [{'weight':W,'balance':g,'angle':b0,'J':J}]
        d=list0[int()]
        return jsonify(d)
  
@app.route('/balance/calibrate/')
def op_balancer_get_k():
    get_k()
    f = open('data_k.csv')
    L=list(csv.reader(f))
    for j in range((len(L)-1),len(L)):    #第j行
        W = int(L[j][7])
        j += 1
        list1 = [{'weight':W}]
        d=list1[int()]
        return jsonify(d)

@app.route('/balance/calibrate0/')
def op_balancer_get_k0():
    get_k0()
    f = open('data_k.csv')
    L=list(csv.reader(f))
    for j in range(1,2):    #第j行
        W = int(L[j][7])
        j += 1
        list1 = [{'weight':W}]
        d=list1[int()]
        return jsonify(d)

if __name__ == '__main__':

    app.run(host='0.0.0.0',port=5000)
    #app.run(host='0.0.0.0',port=80)
