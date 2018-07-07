# =============================================================================
# This is the authentication file
# =============================================================================
import functools

from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for
                   )
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db =get_db()
        error = None

        if not username:
            error: 'Username is required'
        if not password:
            error: 'Password is required'
        else:
            db.execute(
            "INSERT INTO user(username, password) VALUES(?, ?)",
            (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth_login'))
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
                    "SELECT * FROM user where username =?",(username,)
                ).fetchone()

        if user in None:
            error = "Incurrecr username"
        elif not check_password_hash(user['password'], password):
            error = "Incorrecr password"

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

    return render_template('auth/register.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is  None:
        g.user = None
    else:
        g.user = get_db().execute(
                "SELECT * FROM user WHERE user=?", (user_id,)
                ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwags):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwags)
    return wrapped_view





