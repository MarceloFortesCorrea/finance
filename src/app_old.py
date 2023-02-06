# app.py
from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import flask_session
from settings import config_by_name
from database import Database
from cardano import Cardano
from myapp_forms import LoginForm
from datetime import datetime
from util import Get_Data as gd
from finance import Calculate_Finance as cf


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.secret_key = app.config.get('SECRET_KEY', 'mysecretkey')
    app.config['SESSION_TYPE'] = 'filesystem'
    db = Database(app.config['SQLALCHEMY_DATABASE_URI'])
    flask_session.Session(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route("/get_balance/<address>", methods=["GET"])
    def balance(address):
        bc = Cardano()
        balance = bc.get_balance(address)
        json_balance = jsonify({"balance": balance})
        return render_template('cardano.html', json=json_balance)

    @app.route('/smc', methods=['GET', 'POST'])
    def smc():

        if not session.get('login_in'):
            return redirect(url_for('login'))

        if request.method == 'GET':
            return render_template('smc.html')

        ticker = request.form['ticker']
        t_intervals = int(request.form['t_intervals'])
        interations = int(request.form['interations'])

        s_date = datetime(2014, 1, 2)

        db_yahoo = gd().get_yahoo(ticker, s_date, datetime.now())
        price_list = cf().simulator_mc(db_yahoo, t_intervals, interations)
        gd().create_graf_smc(ticker, price_list)
        img_url = url_for('static', filename=ticker + '_grafico.png')

        return render_template('plot.html', img_url=img_url, ticker=ticker)

    @app.route('/oef', methods=['GET', 'POST'])
    def oef():
        if not session.get('login_in'):
            return redirect(url_for('login'))
        if request.method == 'GET':
            return render_template('oef.html')

        tickers = []
        tickers.append(request.form['ticker1'])
        tickers.append(request.form['ticker2'])

        s_date = datetime(2014, 1, 2)

        db_data = gd().get_yahoo_list(tickers, s_date, datetime.now())
        price_list = cf().obtaining_efficient_frontier(tickers, db_data)
        gd().create_graf_oef(tickers, price_list)
        img_url = url_for('static', filename='oef_grafico.png')

        return render_template('plot.html', img_url=img_url,
                               ticker=tickers)

    @app.route('/roi', methods=['GET', 'POST'])
    def roi():
        if not session.get('login_in'):
            return redirect(url_for('login'))
        if request.method == 'GET':
            return render_template('roi.html')

        tickers = []
        tickers.append(request.form['ticker1'])
        tickers.append(request.form['ticker2'])

        s_date = datetime(2014, 1, 2)

        db_data = gd().get_yahoo_list(tickers, s_date, datetime.now())
        data, annual_ind_returns = cf().return_on_index(tickers, db_data)
        gd().create_graf_roi(tickers, data)
        img_url = url_for('static', filename='roi_grafico.png')

        return render_template('plot.html', img_url=img_url,
                               ticker=tickers,
                               annual_ind_returns=annual_ind_returns)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if request.method == 'POST':

            email = request.form['username']
            password = request.form['password']

            if db.check_user(email, password):
                session['email'] = email
                return redirect('/')
            else:
                error = 'Email ou Senha inválidos'
                return render_template('login.html', error=error,
                                       form=form)
        else:
            return render_template('login.html', form=form)

    @app.route('/logout')
    def logout():
        session.pop('login_in', None)
        return redirect(url_for('index'))

    return app


env_name = "dev"  # or "prod"
app = create_app(env_name)

if __name__ == '__main__':
    app.run(debug=True)
