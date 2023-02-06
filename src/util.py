
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from flask import current_app
import os


class Get_Data:
    global ticker
    global tickers
    global s_date
    global e_date
    global img_path

    def __init__(self):
        yf.pdr_override()

    def get_yahoo(self, ticker, s_date, e_date):
        data = pdr.get_data_yahoo_actions(
            ticker, start=s_date, end=e_date)['Adj Close']
        return data

    def get_yahoo_list(self, tickers, s_date, e_date):
        data = pd.DataFrame()
        for ticker in tickers:
            data[ticker] = pdr.get_data_yahoo_actions(
                ticker, start=s_date, end=e_date)['Adj Close']
        return data

    def create_graf_smc(self, ticker, price_list):
        img_path = os.path.join(current_app.root_path,
                                'static', ticker + '_grafico.png')
        plt.figure(figsize=(10, 6))
        plt.plot(price_list)
        plt.xlabel('Tempo (Dias)')
        plt.ylabel(ticker)
        plt.savefig(img_path)
        plt.close()

    def create_graf_oef(self, tickers, db_data):
        img_path = os.path.join(current_app.root_path,
                                'static', 'oef_grafico.png')
        db_data.plot(x='Volatility', y='Return',
                     kind='scatter', figsize=(10, 6))
        plt.xlabel('Expected Valotility')
        plt.ylabel('Expected Return')
        plt.savefig(img_path)
        plt.close()

    def create_graf_roi(self, tickers, db_data):
        img_path = os.path.join(current_app.root_path,
                                'static', 'roi_grafico.png')
        plt.figure(figsize=(10, 6))
        plt.plot(db_data)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.savefig(img_path)
        plt.close()

    def create_graf_euler_discretization(self, ticker, db_data):
        img_path = os.path.join(current_app.root_path,
                                'static', 'euler_grafico.png')
        plt.figure(figsize=(10, 6))
        plt.plot(db_data)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.savefig(img_path)
        plt.close()
