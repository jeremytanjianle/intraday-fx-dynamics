# intraday_fx_dynamics
Simple Function to examine "Intra-day dynamics of exchange rates" by Kuck &amp; Maderitsch (2018)

Kuck & Maderitsch examine intraday dynamics of major USD pairs. 
One particularly interesting finding is that the EURUSD experiences negative autocorrelation at time of low volatility and positive autocorrelation in times of high volatility. 
We can verify this with a single line of code below.

```
import quantile_autoreg as QAR
# type(data['EURUSD'] # pandas time series in ticks
QAR.plot_ar1_coef_w_highvol(data['EURUSD'], granularity = '10Min') 
```
![alt text](https://github.com/vinitrinh/intraday_fx_dynamics/blob/master/images/EURUSD%20Quantile%20Regression.png)

Paper can be found at:
https://www.sciencedirect.com/science/article/abs/pii/S1062976918300322?dgcid=rss_sd_all
