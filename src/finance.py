# finande.py

import pandas as pd
import numpy as np
from scipy.stats import norm


class Calculate_Finance:
    global data
    global t_intervals
    global interations

    def simulator_mc(self, db_data, t_intervals, interations):
        # calcula o retorno log historico apartir da base de dados
        data = db_data
        log_return = np.log(1 + data.pct_change())
        # Retorno logaritimo médio
        u = log_return.mean()
        # Variancia logarítma
        var = log_return.var()
        # Melhor aproximação de taxas futuras
        drift = u - (0.5 * var)
        # Desvio padrão dos retornos logatimos
        stdev = log_return.std()

        # -- Movimento Browniano --
        # x = np.random.rand(10, 2) # norm.ppf(x)
        # (z) é a váriavel aleatoria corresponde a
        # distãncia entre a média dos eventos,
        # expresso pelo número de desvios padrão
        # z = norm.ppf(np.random.rand(10, 2))

        daily_returns = np.exp(drift + stdev *
                               norm.ppf(np.random.rand(t_intervals,
                                                       interations)))

        # preço da ação HJ
        s0 = data.iloc[-1]

        # cria um objeto com as mesmas dimenção de outro objeto
        price_list = np.zeros_like(daily_returns)
        # define o primeiro valor da matriz
        price_list[0] = s0
        for t in range(1, t_intervals):
            price_list[t] = price_list[t-1]*daily_returns[t]

        return price_list

    # obtaining_efficient_frontier
    def obtaining_efficient_frontier(self, tickers, db_data):

        log_returns = np.log(db_data / db_data.shift(1))

        num_assets = len(tickers)
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)

        print('Expected Porfolio Return')
        epret = np.sum(weights * log_returns.mean()) * 250
        print(epret)

        print('Expected Porfolio Variance')
        epvar = np.dot(weights.T, np.dot(log_returns.cov() * 250, weights))
        print(epvar)

        print('Expected Porfolio Volatility')
        epvol = np.sqrt(np.dot(weights.T, np.dot(
            log_returns.cov() * 250, weights)))
        print(epvol)

        pfolio_return = [0]
        pfolio_volatilities = [0]

        for x in range(10000):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            pfolio_return.append(np.sum(weights * log_returns.mean()) * 250)
            pfolio_volatilities.append(
                np.sqrt(np.dot(weights.T, np.dot(log_returns.cov()
                                                 * 250, weights))))

        pfolio_return = np.array(pfolio_return)
        pfolio_volatilities = np.array(pfolio_volatilities)
        # print(pfolio_return)
        # print(pfolio_volatilities)

        portfolios = pd.DataFrame(
            {'Return': pfolio_return, 'Volatility': pfolio_volatilities})
        return portfolios

    def return_on_index(self, tickers, db_data):

        mydata = db_data

        ind_returns = (mydata / mydata.shift(1)) - 1
        ind_returns.tail()
        annual_ind_returns = ind_returns.mean() * 250

        mydataplot = (mydata / mydata.iloc[0] * 100)

        return mydataplot, annual_ind_returns
