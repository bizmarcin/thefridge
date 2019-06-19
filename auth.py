from flask import Blueprint, request, get_flashed_messages, render_template, session, redirect, flash
from werkzeug.security import check_password_hash
import  datetime

from db_utils import get_connection

auth_bp = Blueprint('auth_endpoints', __name__)

@auth_bp.route("/login/", methods=['GET', 'POST'])
def login():
    context = {'now': datetime.datetime.now().year, 'user': None, 'email': None, 'message': None, 'act_alm': 0}

    if request.method == 'GET':
        return render_template('login.html', **context)

    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']

        conn = get_connection()
        c = conn.cursor()

        result = c.execute('SELECT * FROM users WHERE mail = ?', (username,))
        user_data = result.fetchone()
        if user_data:
            hashed_password = user_data['password']
            if check_password_hash(hashed_password, password):
                session['user_id'] = user_data['id']
                session['username'] = user_data['name']
                context['email'] = user_data['name']
                context['user'] = session['username']
                return render_template('dashboard.html', **context)

        context['message']="Wrong user or password"
        return render_template('login.html', **context)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


def login_required(view):
    def wrapped_view(*args, **kwargs):
        if session:
            return view(*args, **kwargs)
        else:
            return redirect('/login')

    wrapped_view.__name__ = view.__name__
    return wrapped_view
