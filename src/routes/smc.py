# routes/smc.py

from flask import Flask, Blueprint, render_template, request, session, url_for, redirect
from datetime import datetime
from util import Get_Data as gd
from finance import Calculate_Finance as cf

smc_bp = Blueprint('smc', __name__)


@smc_bp.route('/smc', methods=['GET', 'POST'])
def smc():

    if not session.get('login_in'):
        return redirect(url_for('login.login'))

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
