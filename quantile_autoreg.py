

import pandas as pd
import numpy as np
import os
import statsmodels.api as sm


def plot_ar1_coef_w_highvol(series, granularity='30Min', vol_window='3600s'):
    """
    plots ar1 coeff 
    input: pandas series of prices
    output: plots graph
    """
    # Groupby granularity
    series = series.groupby(pd.TimeGrouper(freq=granularity)).last().fillna(method = 'ffill')

    # returns and volatility
    ret = series.pct_change()
    vol = ret.rolling(vol_window).std()
    dff = pd.concat([ret, vol], axis=1, join='inner')
    dff.columns = ['ret','vol']

    # high volatility regressor
    dff = dff.assign(high_vol = 0)
    dff.loc[(dff.vol > dff.vol.mean() + 2* dff.vol.std()), 'high_vol'] = 1
    dff.loc[:, 'high_vol'] = dff.high_vol * dff.ret

    # add constant
    dff = sm.add_constant(dff)

    # y-variable
    dff = dff.assign(y = dff.ret.shift(-1))

    # dropna
    dff.replace([np.inf, -np.inf], np.nan)
    dff.dropna(inplace=True)

    from statsmodels.regression.quantile_regression import QuantReg
    mod = QuantReg(endog=dff.y, exog=dff.loc[:,['const','ret', 'high_vol']])

    # 
    quantiles = np.arange(.01, .99, .01)
    def fit_model(q):
        res = mod.fit(q=q)
        return [q, res.params['ret']] + \
                res.conf_int().loc['ret'].tolist() + \
                [res.params['high_vol']]

    models = [fit_model(x) for x in quantiles]
    models = pd.DataFrame(models, columns=['q', 'b','lb','ub', 'high_vol'])

    # plot the quantile regression params
    import matplotlib.pyplot as plt
    plt.title('AR1 Coefficient with {} granularity and {} volatility window'.format(granularity, vol_window))
    plt.plot(models.q, models.b, color='b', label='1st Order AutoRegression')
    plt.plot(models.q, models.ub, linestyle='dotted', color='b')
    plt.plot(models.q, models.lb, linestyle='dotted', color='b')
    plt.plot(models.q, models.b + models.high_vol, color='red', label='High Volatility')
    plt.axhline(y=0, color = 'black', linestyle = '--')
    plt.legend()
    plt.show()

    
def plot_ar1_coef(series, granularity='30Min'):
    """
    plots ar1 coeff 
    input: pandas series of prices
    output: plots graph
    """
    # Groupby granularity
    series = series.groupby(pd.TimeGrouper(freq=granularity)).last().fillna(method = 'ffill')

    # returns and volatility
    ret = series.pct_change()
    vol = ret.rolling(vol_window).std()
    dff = pd.concat([ret, vol], axis=1, join='inner')
    dff.columns = ['ret','vol']

    # add constant
    dff = sm.add_constant(dff)

    # y-variable
    dff = dff.assign(y = dff.ret.shift(-1))

    # dropna
    dff.replace([np.inf, -np.inf], np.nan)
    dff.dropna(inplace=True)

    from statsmodels.regression.quantile_regression import QuantReg
    mod = QuantReg(endog=dff.y, exog=dff.loc[:,['const','ret']])

    # 
    quantiles = np.arange(.01, .99, .01)
    def fit_model(q):
        res = mod.fit(q=q)
        return [q, res.params['ret']] + \
                res.conf_int().loc['ret'].tolist() 
                

    models = [fit_model(x) for x in quantiles]
    models = pd.DataFrame(models, columns=['q', 'b','lb','ub'])

    # plot the quantile regression params
    import matplotlib.pyplot as plt
    plt.title('AR1 Coefficient with {} granularity'.format(granularity))
    plt.plot(models.q, models.b, color='b', label='1st Order AutoRegression')
    plt.plot(models.q, models.ub, linestyle='dotted', color='b')
    plt.plot(models.q, models.lb, linestyle='dotted', color='b')
    #plt.plot(models.q, models.high_vol, color='red', label='High Volatility')
    plt.axhline(y=0, color = 'black', linestyle = '--')
    plt.legend()
    plt.show()
