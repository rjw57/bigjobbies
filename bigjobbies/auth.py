import datetime
from urllib.parse import urlencode

from flask import (
    Blueprint, abort, render_template, request, abort, current_app, session,
    redirect, url_for
)
import jwt

from . import pin

auth = Blueprint('auth', __name__)

AUTH_TOKEN_KEY = 'auth_token'

def is_request_authenticated():
    return False

def new_token():
    payload = {
        'auth': True,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        'nbf': datetime.datetime.utcnow() - datetime.timedelta(seconds=5),
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def check_token(token):
    payload = jwt.decode(token, current_app.config['SECRET_KEY'])
    return payload.get('auth', False)

# Function suitable for passing to before_request.
def check():
    token = session.get(AUTH_TOKEN_KEY)
    if token is None or not check_token(token):
        query = { 'next': request.full_path }
        return redirect(url_for('auth.login') + '?' + urlencode(query))

    # Refresh auth roken
    session[AUTH_TOKEN_KEY] = new_token()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return render_template(
            'needpin.html', next=request.values.get('next', '/'))

    if not pin.compare_pin(request.values.get('pin'), current_app.config['AUTH_PIN']):
        abort(403)

    # All good, set a token
    session[AUTH_TOKEN_KEY] = new_token()

    return redirect(request.values.get('next', '/'))
