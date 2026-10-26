from collection import socketio
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_socketio import join_room, leave_room, emit
import random

# Blueprint: 라우팅 함수를 체계적으로 관리
bp = Blueprint('square_goofspiel', __name__, url_prefix='/square_goofspiel')

active_games = {}
default_squares = ['11','12','13','14','15','16','21','22','23','24','25','26','31','32','33','34','35','36','41','42','43','44','45','46','51','52','53','54','55','56','61','62','63','64','65','66']

def initialize_history():
    square_string = "".join(random.sample(default_squares, len(default_squares)))
    x14 = "xxxxxxxxxxxxxx"
    x12 = "xxxxxxxxxxxx"
    initialized_history = "".join([square_string[0:12], x14, square_string[12:24], x14, square_string[24:36], x14, square_string[36:48], x14, square_string[48:60], x14, square_string[60:72], x12])
    return initialized_history

@bp.route('/<game_id>')
def get_room(game_id):
    session['game_id'] = game_id
    return render_template("game/square_goofspiel.html")

@socketio.on('connect')
def on_connect():
    # todo: error handling in case someone manually enters url without creating game
    sid = request.sid
    game_id = session.get('game_id')
    join_room(game_id)
    start = False

    if active_games.get(game_id) is None:
        active_games[game_id] = {
            'red': sid,
            'red_connected': True,
            'red_move': None,
            'blue': '',
            'blue_connected': False,
            'blue_move': None,
            'history': initialize_history()
        }
    else:
        if active_games[game_id]['blue'] == '':
            active_games[game_id]['blue'] = sid

    if active_games[game_id]['red'] != '' and active_games[game_id]['blue'] != '':
        start = True

    if active_games[game_id]['red'] == sid:
        active_games[game_id]['red_connected'] = True
        emit('game_connection', {'message': 'You have connected as Red!', 'color': 'red', 'history': active_games[game_id]['history'], 'start': start})
        emit('game_connection', {'message': 'Your opponent has connected as Red!', 'color': 'blue', 'history': active_games[game_id]['history'], 'start': start}, to=game_id, include_self=False)
    elif active_games[game_id]['blue'] == sid:
        active_games[game_id]['blue_connected'] = True
        emit('game_connection', {'message': 'You have connected as Blue!', 'color': 'blue', 'history': active_games[game_id]['history'], 'start': start})
        emit('game_connection', {'message': 'Your opponent has connected as Blue!', 'color': 'red', 'history': active_games[game_id]['history'], 'start': start}, to=game_id, include_self=False)

    return

@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    game_id = session.get('game_id')
    leave_room(game_id)
    to_remove = []

    for room, room_details in active_games.items():
        if room_details['red'] == sid:
            room_details['red_connected'] = False
            emit('game_connection', {'message': 'Red has disconnected!'}, to=game_id, include_self=False)
        if room_details['blue'] == sid:
            room_details['blue_connected'] = False
            emit('game_connection', {'message': 'Blue has disconnected!'}, to=game_id, include_self=False)
        if room_details['red_connected'] == False and room_details['blue_connected'] == False:
            to_remove.append(room)

    for room in to_remove:
        active_games.pop(room)

    return

@socketio.on('move')
def on_move(move):
    sid = request.sid
    game_id = session.get('game_id')
    if active_games[game_id]['red'] == sid:
        active_games[game_id]['red_move'] = move
    elif active_games[game_id]['blue'] == sid:
        active_games[game_id]['blue_move'] = move

    if active_games[game_id]['red_move'] and active_games[game_id]['blue_move']:
        red_move = active_games[game_id]['red_move']
        blue_move = active_games[game_id]['blue_move']
        history = list(active_games[game_id]['history'])

        index = history.index('x')
        if index % 2 == 1:
            index = index - 1

        history[index] = red_move
        history[index + 1] = blue_move
        history = "".join(history)

        active_games[game_id]['history'] = history
        active_games[game_id]['red_move'] = None
        active_games[game_id]['blue_move'] = None

        emit('game_update', {'history': history}, to=game_id)

    # the game history is stored in a 154 character string where the positions of the characters will be converted to information
    # the first 12 digits means which 6 squares are up for bid at the start of a round. Each pair of numbers is the xy coordinates of squares.
    # 111223336532 means at the start of the round, squares (1,1), (1,2), (2,3), (3,3), (6,5), and (3,2) are up for bid in that order.
    # the next 12 digits means which cards were played by players. Each pair of numbers is red's card and blue's card in that order.
    # 231535026211 means that Red played 2 and Blue played 3 on Round A, Red played 1 and Blue played 5 on Round B, and so on.
    # x means waiting for a submission.
    # the next 2 digits means whether a player has clicked "continue" after the set of 6 rounds have finished.
    # x means waiting on a player, 1 means they have clicked "continue". There won't be a pair at the very end.
    # progress gamestate when both red_move and blue_move are filled then reset values

    return
