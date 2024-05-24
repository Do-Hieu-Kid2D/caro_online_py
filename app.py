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

# chơi caro online 2 người
@app.route('/caro-onl')
def onl():
    return render_template('caro-onl.html')


# Tạo phòng chơi để join vào phòng 
@app.route('/create', methods=['POST'])
def create():
    room_code = request.form.get('room_code')
    if room_code in rooms:
        return 'Room already exists', 400
    rooms[room_code] = {'players': []}
    player_count = 0
    return 'Room created successfully'

global_player_count = 0

# Join phòng chơi (check các điều kiện)
@socketio.on('join')
def on_join(data):
      global global_player_count
      room_code = data['room_code']

      if room_code not in rooms or len(rooms[room_code]['players']) >= 2:
        return 'Room is full', 400

      symbol = 'X' if global_player_count == 1 else 'O'
      player = {'id': request.sid, 'symbol': symbol}
      rooms[room_code]['players'].append(player)

      join_room(room_code)

      # Gửi thông tin của cả hai người chơi về client
      emit('join', {'room_code': room_code, 'player': player, 'request_sid': request.sid, 'players': rooms[room_code]['players']}, room=room_code)

      global_player_count += 1

# Xử lý sự kiện disconnect
@socketio.on('disconnect')
def handle_disconnect():
    global global_player_count

    # Lấy thông tin người chơi mất mạng
    disconnected_player = None
    room_code = None

    for room_code, room_data in rooms.items():
        for player in room_data['players']:
            if player['id'] == request.sid:
                disconnected_player = player
                room_data['players'].remove(player)
                break

    # Nếu có người chơi mất mạng, cập nhật thông tin và gửi sự kiện 'leave' đến các client trong phòng
    if disconnected_player:
        leave_room(room_code)
        emit('leave', {
            'room_code': room_code,
            'player': disconnected_player,
            'request_sid': request.sid,
            'players': room_data['players']
        }, room=room_code)

        global_player_count -= 1

        # Gửi thông báo về số người còn lại trong phòng
        emit('playerCountUpdate', {'room_code': room_code, 'player_count': len(room_data['players'])}, room=room_code)

        # Gửi sự kiện thông báo khi đối thủ mất kết nối cho từng người chơi còn lại
        opponent = next((p for p in room_data['players'] if p['id'] != request.sid), None)
        if opponent:
            emit('opponentDisconnected', room=opponent['id'])


# Rời phòng chơi
@socketio.on('leave')
def on_leave(data):
    global global_player_count
    room_code = data['room_code']

    if room_code not in rooms:
        return 'Room does not exist', 400

    player = next((player for player in rooms[room_code]['players'] if player['id'] == request.sid), None)
    if player is None:
        return 'Player not in room', 400

    rooms[room_code]['players'].remove(player)
    leave_room(room_code)

    # Gửi thông tin về việc rời phòng về client
    emit('leave', {'room_code': room_code, 'player': player, 'request_sid': request.sid, 'players': rooms[room_code]['players']}, room=room_code)

    global_player_count -= 1



