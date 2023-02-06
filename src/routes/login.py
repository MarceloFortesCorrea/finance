# routes/login.py

from flask import Flask, Blueprint, render_template, request, session, redirect
from myapp_forms import LoginForm
from database import Database
from settings import config_by_name


login_bp = Blueprint('login', __name__)

app = Flask(__name__)
app.config.from_object(config_by_name['dev'])
db = Database(app.config['SQLALCHEMY_DATABASE_URI'])


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':

        email = request.form['username']
        password = request.form['password']

        if db.check_user(email, password):
            session['login_in'] = True
            session['email'] = email
            return redirect('/')
        else:
            error = 'Email ou Senha inválidos'
            return render_template('login.html', error=error,
                                   form=form)
    else:
        return render_template('login.html', form=form)
