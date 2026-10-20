from flask import Blueprint, render_template, request, redirect, url_for
from collection import socketio


# Blueprint: 라우팅 함수를 체계적으로 관리
bp = Blueprint('square_goofspiel', __name__, url_prefix='/square_goofspiel')

active_games = {}

@bp.route('/<game_id>')
def get_room(game_id):
    return render_template(
        "game/square_goofspiel.html", game_id=game_id
    )

@socketio.on('connect')
def on_connect():
    sid = request.sid
    game_id = request.get('game_id')
    if active_games.get(game_id) is None:
        active_games[game_id]['red'] = sid
        active_games[game_id]['red_connected'] = True
        active_games[game_id]['red_move'] = ''
        active_games[game_id]['blue'] = ''
        active_games[game_id]['blue_connected'] = False
        active_games[game_id]['blue_move'] = ''
        active_games[game_id]['history'] = ''
    else:
        if active_games[game_id]['blue'] == '':
            active_games[game_id]['blue'] = sid
    # emit opponent has joined the game
    return

@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    to_remove = []
    for room, room_details in active_games.items():
        if room_details['red'] == sid:
            room_details['red_connected'] = False
        if room_details['blue'] == sid:
            room_details['blue_connected'] = False
        if room_details['red_connected'] == False and room_details['blue_connected'] == False:
            to_remove.append(room)

    for room in to_remove:
        active_games.pop(room)

    # emit opponent has left the game
    return

@socketio.on('move')
def on_move():
    sid = request.sid
    # red_move = request.get('move')
    # update room['history']
    # progress gamestate when both red_move and blue_move are filled then reset values
    return
