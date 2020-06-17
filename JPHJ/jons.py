import socket
import RPi.GPIO as GPIO
from flask import Flask

from balancer import *
from faceA import *

app = Flask(__name__)

@app.route('/balancer/g')
def op_balancer_g():
    get_W_g()
    return

@app.route('/call/call')
def op_Call_h():
    Call_history_data()
    return

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    hostname = socket.gethostname()
    print('Hostname %s' % hostname)

    h = SerialMeter(6, [19,13,26])
    s = Stepper(14,15,18)

    app.run(host='0.0.0.0', port=5000,debug = True)
    # app.run(host='0.0.0.0', port=80,debug = True)  
