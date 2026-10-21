from flask import Blueprint, render_template, redirect, url_for, session
import secrets
import string


# Blueprint: 라우팅 함수를 체계적으로 관리
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template(
        "index.html"
    )

def generate_room_token(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@bp.route('/create/<game>')
def create(game):
    game_id = generate_room_token()
    return redirect(url_for(f'{game}.get_room', game_id=game_id))
