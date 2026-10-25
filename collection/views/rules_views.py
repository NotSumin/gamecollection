from flask import Blueprint, render_template, redirect, url_for, session
import secrets
import string


# Blueprint: 라우팅 함수를 체계적으로 관리
bp = Blueprint('rules', __name__, url_prefix='/rules')

@bp.route('/square_goofspiel')
def square_goofspiel():
    return render_template(
        "rules/square_goofspiel.html"
    )