# intraday_fx_dynamics
Replicate findings "Intra-day dynamics of exchange rates" by Kuck &amp; Maderitsch (2018). 

Kuck & Maderitsch examine intraday dynamics of major USD pairs with Quantile Regression. See diagram below.   
![alt text](https://github.com/vinitrinh/intraday_fx_dynamics/blob/master/images/EURUSD%20Quantile%20Regression.png)  
How do we interpret this? The EURUSD experiences negative autocorrelation at time of low volatility and positive autocorrelation in times of high volatility. Practically, low volatility regimes favor mean reversion trading strategies with high volatility regimes favor momentum strategies.   


The findings in this repo is consistent with that in their paper.  
The heart of the repo is the code snippet below. 

```
import quantile_autoreg as QAR
# type(data['EURUSD'] # pandas time series in ticks
QAR.plot_ar1_coef_w_highvol(data['EURUSD'], granularity = '10Min') 
```

Paper can be found at:
https://www.sciencedirect.com/science/article/abs/pii/S1062976918300322?dgcid=rss_sd_all
