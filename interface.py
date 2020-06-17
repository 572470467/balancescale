
from flask import Flask, jsonify
import random
import time
import csv
app = Flask(__name__)

@app.route('/balance/measure/')
def op_balancer_test():
    get_text_one()
    y=open('data.csv','r')
    reader=csv.reader(y)
    lt=[]
    for a in reader:
        lt.append(a)
    d={'weight':a[11],'balance':a[1],'angle':a[3]}
    return jsonify(d)

@app.route('/balance/calibrate/')
def op_balancer_get_k():
    get_k()
    y=open('data_k.csv','r')
    reader=csv.reader(y)
    lt=[]
    for a in reader:
        lt.append(a)
    d=[{'weight':a[7],'k0':a[1],'k1':a[2],'k2':a[3]}]
    return jsonify(d)

@app.route('/balance/calibrate0/')
def op_balancer_get_k_original():
    get_k_original()
    y=open('data_k.csv','r')
    reader=csv.reader(y)
    lt=[]
    for a in reader:
        lt.append(a)
    d=[{'weight':a[7],'k0':a[1],'k1':a[2],'k2':a[3]}]
    return jsonify(d)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

    
    
