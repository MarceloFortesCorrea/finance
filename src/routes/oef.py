# routes/oef.py

from flask import Flask, Blueprint, render_template, request, session, url_for, redirect
from datetime import datetime
from util import Get_Data as gd
from finance import Calculate_Finance as cf

oef_bp = Blueprint('oef', __name__)


@oef_bp.route('/oef', methods=['GET', 'POST'])
def oef():
    if not session.get('login_in'):
        return redirect(url_for('login.login'))
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
