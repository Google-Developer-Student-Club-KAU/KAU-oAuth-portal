import sys; sys.dont_write_bytecode = True
from flask import session, redirect, request, abort, url_for, render_template, flash
from flask_login import login_required, current_user, login_user, logout_user
from .src import create_app
from .src.base import db
from .src.user import User


app, login_manager = create_app()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route("/test")
def test():
    return "hi."

@app.route("/")
@login_required
def index():
    return render_template("index.html", user=current_user)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)