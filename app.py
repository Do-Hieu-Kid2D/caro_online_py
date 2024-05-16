# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from flask import jsonify

app = Flask(__name__)
socketio = SocketIO(app)
rooms = {}

# Trang home
@app.route('/')
def index():
    return render_template('index.html')

# Trang chơi caro online 2 người
@app.route('/caro-onl')
def onl():
    return render_template('caro-onl.html')

# Trang chơi caro offline 2 người
@app.route('/caro-off')
def off():
    return render_template('caro-off.html')

# Trang chơi caro người - máy
@app.route('/caro-computer')
def computer():
    return render_template('caro-computer.html')

# Trang chơi caro máy - máy
@app.route('/caro-2computer')
def twocomputer():
    return render_template('caro-2computer.html')
