def syntax():
    print('''
    
import numpy as np
import pandas as pd

df= pd.read_csv ('Perrin Freres monthly champagne sales millions.csv')
df

df.isna().sum()

df.dropna(inplace=True)

df.columns=['Month','Sales']
df

df.info()
df['Month']=pd.to_datetime(df['Month'])
df=df.set_index('Month')
df.plot()
df['first_order']=df['Sales']-df['Sales'].shift(1)
df
df['first_order'].plot()

from statsmodels.tsa.stattools import adfuller

adfuller(df['first_order'].dropna())

#first value- adf test statistic should be -ve
#second value is my p value should be less than 0.05
#third value is number of lags

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
plot_acf(df['first_order'].dropna())
plot_pacf(df['first_order'].dropna())
df['season']=df['Sales']-df['Sales'].shift(12)
df

df['season'].plot()

adfuller(df['season'].dropna())
plot_acf(df['season'].dropna())
plot_pacf(df['season'].dropna())

#p is 1
#q is 1

from statsmodels.tsa.ar_model import AutoReg
ar= AutoReg(df['season'].dropna(),lags=1).fit()
ar.aic
df['ar_preds']= ar.predict(start=0,end=93,dynamic=True)
len(df['season'])
df
df[['season','ar_preds']].plot()

from statsmodels.tsa.arima.model import ARIMA
arima= ARIMA(df['season'].dropna(),order=(1,0,1)).fit()
arima.summary()

df['arima_preds']= arima.predict(start=0,end=93,dynamic=True)
df

df[['season','arima_preds']].plot()

from statsmodels.tsa.statespace.sarimax import SARIMAX

sarima = SARIMAX (df['Sales'],order=(1,1,1),seasonal_order=(1,1,1,12)).fit()
sarima.summary()
df['sarima_preds']= sarima.predict(start=100,end=120,dynamic=True)
df
df[['Sales','sarima_preds']].plot()

    
    ''')

syntax()