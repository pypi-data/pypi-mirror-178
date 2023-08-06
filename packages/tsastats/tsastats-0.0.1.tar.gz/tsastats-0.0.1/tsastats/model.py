def model():
    print('''

MA MODEL:
Moving average model uses past forecast errors to predict the next point in time.	
The time Period at T  is Impacted by the unexpected external factors at various
Slots   t-1,t-2,t-3……t-k. These unexpected impacts are known as errors or residuals. The Impact of previous time shots is decided by the coefficient factor alpha() at that particular period of time.
This kind of model calculate the residuals of errors of past time series and calculates the present or future values in the series is known as
Moving Average () Model.
Formula:-
Yt = c + et + sum(j=1,q) phi(j) et-j
Yt = et +phi(1) et-1- order 1
Yt = et +phi(1) et-1+ phi(2)et-2- order 2



AR Model:-
In auto regression model we forecast the variable of interest using a linear combination of past values of the variable.
The term Auto regression indicates that it is a regression of the variable against itself
The time period at t is impacted by the observations  of various slots  t-1, t-2, t-3, the impact of previous time slots is decided by the coefficient factor at that particular period of time.
-it uses the prev steps observations to predict the next time step values
X is yt-1, yt is x+y (value of yt is dependent on yt-1)
Ar model eq
Yt = c+summ i=1 to p theta1 yt-1 + et
Yt- dependent on itself in ar, y dependent on x and x is independent 

Equation
Yt = c+theta1 yt-1 + et- ar model 1

ARMA MODEL
Arma is a model of forecasting in which both autoregression analysis and moving average models are applied to time series data. In Arma it is assumed that time series data is stationary.
Arma model describes the relationship of time series with both random noise(MA MODEL) and also with the prev step of itself(AR MODEL).
Equations of both Ar and Ma model and then the combined equation to form Arma.
Explanation of the equation
ARMA model
Ar-> yt = c + sigma(thetai*yt-i) + Et
Ma-> yt = c + sigma(phij*Et-j) + Et
ARmA-> yt = c + Et+ sigma(thetai*yt-i) + sigma(phij*Et-j) 
P and q are the significant parameters
P -> AR model’s parameter
Q -> mA model’s parameter
ArmA model explains relationship of ts with random noise (mA) and previous step of itself (AR)

Acf and Pacf graphs 
In time series, we sometimes rely on past data points to make estimate about the current or the future values. However sometimes thats not enough. When unexpected events like normal disaster, financial arises or even war happens, it can be a sudden shift in values.
That’s why we need models that simultaneously use past data as foundation for estimates but can also adjust to unpredictable shocks.
ARMA is one such model
It comes from merging 2 simple models AR & MA


ARIMA MODEL
Same as ARMA but it differences the data to make it stationary. The d value is order of differencing. If your data is stationary, use ARMA directly
Drawback of differencing 
1 data point is lost each time we difference. Original x2, differenced x2-x1
formula= y`t= c+et+ summ i=1 to p theta i (y`t-i)+ summ j=1 to q phi, et-j, y`t is differenced parts


SARIMA MODEL

Seasonal Autoregressive Integrated Moving Average, SARIMA or Seasonal ARIMA, is an extension of ARIMA that explicitly supports univariate time series data with a seasonal component.
It adds three new hyperparameters to specify the autoregression (AR), differencing (I) and moving average (MA) for the seasonal component of the series, as well as an additional parameter for the period of the seasonality.
Trend Elements
There are three trend elements that require configuration.
They are the same as the ARIMA model; specifically:
•	p: Trend autoregression order.
•	d: Trend difference order.
•	q: Trend moving average order.
Seasonal Elements
There are four seasonal elements that are not part of ARIMA that must be configured; they are:
•	P: Seasonal autoregressive order.
•	D: Seasonal difference order.
•	Q: Seasonal moving average order.
•	m: The number of time steps for a single seasonal period.
SARIMA(p,d,q)x(P,D,Q,s)



    ''')

model()