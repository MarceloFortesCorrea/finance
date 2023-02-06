# routes/roi.py

from flask import Flask, Blueprint, render_template, request, session, url_for, redirect
from datetime import datetime
from util import Get_Data as gd
from finance import Calculate_Finance as cf

roi_bp = Blueprint('roi', __name__)


@roi_bp.route('/roi', methods=['GET', 'POST'])
def roi():
    if not session.get('login_in'):
        return redirect(url_for('login.login'))
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
