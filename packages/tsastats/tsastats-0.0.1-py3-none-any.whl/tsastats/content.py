def content():
    print('''
Linear Regression v/s Autoregression
LR -> Equation [ yt = Bo + B1x + Et ] - not dependent on itself
AR -> Equation [ yt = Alpha + Rhot-1 + Et ] - dependent on itself (previous term)

ACF AND PACF

Autocorrelation is the correlation between a time series with a lagged version of itself. The ACF starts at a lag of 0, which is the correlation of the time series with itself and therefore results in a correlation of 1.
The ACF plot can provide answers to the following questions:
Is the observed time series white noise/random?
Is an observation related to an adjacent observation, an observation twice-removed, and so on?
Can the observed time series be modeled with an MA model? If yes, what is the order?
Additionally, you can see a blue area in the ACF and PACF plots. This blue area depicts the 95% confidence interval and is an indicator of the significance threshold. That means, anything within the blue area is statistically close to zero and anything outside the blue area is statistically non-zero.
 
PACF:
Order 1
Yt = c+ et + phi*y(t-1)
 
Order 2:
Yt = c+ et + phi1*y(t-1)+ phi2*y(t-2)
 
PACF for A.R model
Note:
·       PACF gives the correlation between the present value of time series and the residual part of previous lag.
·       If your ACF plot doesn’t give a significant correlation and order then plot the PACF graph.
 
How to determine which model to be used?
Try different combinations of MA and AR models.
Choose the one which has least AIC.
Table:
AR(p)	                  MA(q)	                 ARMA(p,q)
Geometric drop/decay  Sudden drop(q)	     Geometric drop/decay
Sudden drop(p)	      Geometric drop/decay   Geometric drop/decay


HOW TO CHOOSE P,D,Q VALS FOR ARMA MODEL
1.Perform tests for stationarity to check if TS is stationary or not
2.-if ts is stationary(d=0) try to fit arima model - if ts not stationary perform next order of differencing and note the value of d
3.plot acf and pacf graph
4. Acf will give ma order,value of q which represents ma process
5.pacf will give p which represents ar process

STATIONARITY AND ITS TYPES
Stationarity: no change wrt time
Properties of data don’t change w time. There are 2 types of stationarity: Strong & Weak
Strong: The distribution/ joint distribution of a ts doesn’t change time & remains exactly the same throughout Distribution of today will be the same as lag distributions

Weak stationarity: Also referred to as wide sense stationarity. If ts has constant mean and variance throughout time & covariance is dependent upon the lag factor, then ts is weak stationary 
Derivation:
Xt -> Xt+k Where k is the lag factor Lag factor affects data points
Properties of stationarity: Mean is constant, Variance is constant, Covariance is independent of time

AIC 
Akaike’s Information Criteria (AIC) 

AIC is a statistical criteria used to compare the quality of statistical models. Increasing data gives better AIC. 

Assumptions of model 
1.	Some data to be used for all the models 
2.	Measure the same output variables between the model.
3.	Sample size should be infinite. 

Formula 
AIC = -2 Log (L) + 2K 
L = Likelihood of data 
K = No. of parameters.

Note 
#AIC tells us the relative quality of statistical models. (Best among diff models)
#High MLE value will give low AIC and vice versa. Hence MLE is inversely proportional to AIC

Ideal usage of AIC 
1.	Where out of sample data is not accessible. (implementing only on the sample data)
2.	When you decide between multiple models
3.	Where you don’t have to decide between multiple SARIMA models.

Advantages 
1.	If your AIC assumptions are fulfilled then the models need not be nested 
2.	AIC helps compare vast numbers of different models. 

Disadvantages 
1.	AIC becomes inaccurate for small data 
2.	AIC doesn’t say anything about absolute quality of models. (doesn’t give 100% right model’s righteousness) 

What to use when data is small? 
Correlated AIC => AICC => Add a correlated term 


Conditions when AIC is inaccurate
1.	When  no.of data points / no. of parameters < 40, it is inaccurate 
Add correlation when AIC becomes inaccurate 
2.	Correlated AIC => Safest option 
Formula - AICC = AIC + 2K(K+1/(n-k-1) 
After simplifying use residual square/error
AICC = 2k +n log(RSS/N) + 2k(k+1)/n-k-1

Advantages same as AIC 
AIC doesn’t calculate the differentiating order. If done after the model is applied which is only applied after it is stationary. 


Components of Time Series:

A time series consists of four components,generally speaking 
These 4 components are: Trend,Seasonality,Cyclic and Random 
Trend
Trend shows a common tendency of data. It may move upward or increase or go downward or decrease over a certain, long period of time. The trend is a stable and long-term general tendency of movement of the data. To be a trend, it is not mandatory for the data to move in the same direction. The direction or movement may change over the long-term period but the overall tendency should remain the same in a trend.
Some of the examples of trends include – the number of schools, agricultural production, increase in population, etc. It is notable that the trend may move upward, go downward or remain stable over different sections of time.
A Trend can be either linear or non-linear.
Seasonal Variations
Seasonal variations are changes in time series that occur in the short term, usually within less than 12 months. They usually show the same pattern of upward or downward growth in the 12-month period of the time series. These variations are often recorded as hourly, daily, weekly, quarterly, and monthly schedules.
Seasonal variations occur due to natural or manmade forces or variations. The numerous seasons and manmade variations play a vital role in seasonal variations.
Example − The crops depend on the season, the sales of A.C,s going up during the summer and the use of umbrellas skyrocketing during the rainy season - all of these are seasonal variations.
Seasonal variations can be clearly seen in some cases of man-made conventions. The festivals, customs, fashions, habits, and various occasions, such as weddings impact the seasonal variations. An increase in business during the seasonal variation period should not be considered a better business condition.

Cyclical Variations
Variations in time series that occur themselves for the span of more than a year are called Cyclical Variations. Such oscillatory movements of time serious often have a duration of more than a year. One complete period of operation is called either a cycle or a ‘Business Cycle’.
Cyclic variations contain four phases - prosperity, recession, depression, and recovery. It may be regular or non-periodic in nature. Usually, cyclical variations occur due to a combination of two or more economic forces and their interactions.
Random or Irregular Movements
There is another kind of movement that can be seen in the case of time series. It is pure Irregular and Random Movement. As the name suggests, no hypothesis or trend can be used to suggest irregular or random movements in a time series. These outcomes are unforeseen, erratic, unpredictable, and uncontrollable in nature.
Earthquakes, war, famine, and floods are some examples of random time series components.

TS. Modeling Procedure
1. Plot the date and try to usually, find the patters and unique observations.
2. If you notice any trend, remove the fend. Either by differencing or logarithmic function 
3. Check for stationarity: using
> DF,ADF,KPSS
4. If stationary, go ahead otherwise repeat the transformation steps again like differencing
5. Plot ACF and PACF graph, ACF: autocorrelation function, Gives us the order of MA
PACF: Partial autocorrelation function. Gives us the order of AR
6.After getting order of MA and AR apply different combination of orders and select the best model Apart from the order,the quality can be obtained from AIC. Lower the AIC, better the model
7. Check residuals or the error and make sure they look like white noise(check for white noise can be done using ljung box test)
8. Observe and calculate the forecast 




Assignment 1 
Gauss Markov Model 
The gauss markov setup tells us that if a certain set of assumptions are met then two ordinary least squares estimates for regression coefficients gives us the best linear unbiased estimate possible. 
Equation - 
Ỷ= X β+ ĕ
Where E( ĕ) = 0 and V( ĕ)=𝜎^2 I 
Conditions 
 E( ĕi) = 0 
V( ĕi)=𝜎^2  
Where i = 1,2,3,...N

(e1,e2,...en) & (v1,v2,v3,...vn) are independent

Cov (ei,ej)= 0 			i,j = 1,2.. N and i != j 
e=error 
 Assumptions 
1.	Linearity - parameters we estimate using OLS must be linear 
2.	Random - Our data must be randomly sampled from the population
3.	Non - collinearity - The regressors calculated aren’t perfectly correlated to each other 
4.	Exogenity - The resgressors aren’t correlated with the error term 
5.	Homoscedasticity - No matter the values of our regressors, the variance of the error term is constant. 

Application - 
Calibration curve
Curve fitting 
Numerical smoothing and differentiating 
Moving least square 
System identification


Homoscedasticity 
It means having the same variance. In linear regression the main assumption is to have homoscedasticity in the error and the residual term. If the variances of the error and residual term are constant then it is Homoscedasticity. Error term is same across all independent variables. Having the same scatter. Same variance


Heteroscedasticity 
If the variance of the error or residual term varies and is not constant then it is said to be heteroscedasticity. It is said to be of two types - impure and pure. 
When we fit the right model and there is a visible pattern of either a rise or a fall  in variance then it is said to have pure heteroscedasticity. And if we fit the wrong model and a pattern appears then it is impure heteroscedasticity. Error term varies across the independent variables.




Endogenous Variables vs Exogenous Variables 
An endogenous variable in a statistical model is one that can be changed or is determined by other variables studied in the model. A variable as Xj is said to be endogenous if its value is determined or influenced by one or more independent variables X. 
The relation between Xj and X can be positive or negative. As long as there is change in the variable, it is said to be endogenous variable. 
Eg. The price of wheat is dependent on the requirement of wheat by the people. 

Exogenous Variables
Unlike endogenous variables the value of exogenous variables are not dependent on any other variables in a model. Rather, the variables on which endogenous variables are dependent are exogenous variables. 
Eg.  My personal income has no relationship with my favorite colour. 
Endogenous vs. Exogenous Variables
In contrast to endogenous variables, exogenous variables are considered independent. In other words, one variable within the formula doesn't dictate or directly correlate to a change in another. Exogenous variables have no direct or formulaic relationship. For example, personal income and color preference, rainfall and gas prices, education obtained and favorite flower would all be considered exogenous factors.



TIME SERIES AND ASSUMPTIONS
Ts- Analysing data over time, forecasting/predicting future value based on past data value,weak stationary,depending on time-t and s-continuity of data(series)
Assumption- 1. Linearity (data should be linear) ols:- 1/2m summ(y-ybar)^2
2.variance=constan  t mean=0
3. Non colinearity- variables should not be colinear, independent variable, iid(identically independent normally distributed)
4. No serial correlation-should not be correlated
5. Randomness- data should be random 
6. Exogenety- Tests independency/dependency between x and y
-sequential-et not related to xi(not dependent,et not affected)
-strict-xi is completely unaffected by y and et will not be affected




WHAT IS LINEAR REGRESSION + EQUATIONS. DIFFERENCE BETWEEN LR AND AR

linear regression is a regression model that estimates the relationship between one independent variable and one dependent variable using a straight line. Both variables should be quantitative.

Y = beta0 + beta1.x1 + et
Yt = f(xi,bi) + et

WHAT IS WHITE NOISE,RANDOM WALK

White noise is conceptually essential for ts analysis and forecasting.white noise is a series that is not predictable as it is a sequence of random numbers.if you build a model and its residual (diff b/w actual and predicted values)look like a white noise,then model is as good as possible.on the other side if the residuals show a pattern then better model can be implemented
Properties- mean is 0,varience is constant,not correlated, normally distributed,ramdomness present,identically independent distributed variables i.e et~iid N(0,sigma^2)
So if we plot acf for white noise,we want all the spikes to be low showing there is no correlation

Random walk- just like white noise, random walk series is also not predictable, what makes it diff from white noise is that random walk is not a list of random numbers. The current value depends on the previous one A random walk is a time series model xt such that xt=xt−1+wt, where wt is a discrete white noise series.


DF AND ADF TESTS

DF
Assumptions- ts should be hetroscedastic, ar model should have parameters(no of lags), white noise should be non autocorrelated 

Advantages- useful for testing stationarity
Disadvantage-Not applicable for auto-correlated data, the power of this test is very low

Null and alternate hypothesis of DF:
Null hypo: mod of rho should be equal to one or sigma should be equal to zero
Alt hypo: mod of rho should be less than one or sigma should be less than zero
The null hypo suggests that there exists a unit root which implies that the data is not stationary.
The alt hypo suggests that there does not exist a unit root and time series is stationary


Rejection/Decision criteria:
If Tcal>Tcritical, where Tcritical is DF distribution’s critical value then reject null hypothesis and accept alternate hypo, therefore ts is stationary
If tcal<tcritical, where tcritical is df distribution’s critical/cutoff point then reject alternate and accept null hypo , therefore ts is not stationary
Derivation:
Xt=rho*Xt-1+Et
Where rho is coefficient of Xt-1 and lies b/w -1&1
Xt-1 -> lag
Et -> residuals where Et is a iid belongs to normal dist w means zero and var as sigma square
Can’t use t-test directly
Xt – Xt-1=rho*Xt-1 - Xt+Et            Subtracting Xt-1
Delta Xt= Xt-1 (Rho -1) +Et
Delta Xt is classically first order differencing, second order is delta square Xt
Hence (rho -1 ) is the only term independent on time 
Let rho-1 = sigma
Delta Xt= Sigma (Xt-1) + Et
Hypothesis Testing:
Formulation of hypothesis:  
Level of significance Is 5%
Calculate Tstatistic 
Tcal from program/code
Tcritical from DF distribution table


ADF
The Augmented Dickey Fuller Test (ADF) is unit root test for stationarity. Unit roots can cause unpredictable results in your time series analysis.
The Augmented Dickey-Fuller test can be used with serial correlation. The ADF test can handle more complex models than the Dickey-Fuller test, and it is also more powerful. That said, it should be used with caution because—like most unit root tests—it has a relatively high Type I error rate.
Hypotheses
The hypotheses for the test:
●	The null hypothesis for this test is that there is a unit root.
●	The alternate hypothesis differs slightly according to which equation you’re using. The basic alternate is that the time series is stationary (or trend-stationary).
Choosing Models and Lags
Before you run an ADF test, inspect your data to figure out an appropriate regression model. For example, a nonzero mean indicates the regression will have a constant term. The three basic regression models are:
●	No constant, no trend: Δyt = γyt-1 + vt
●	Constant, no trend: Δyt = α + γyt-1 + vt
●	Constant and trend: Δyt = α + γyt-1 + λt + vt
The Augmented Dickey Fuller adds lagged differences to these models:
●	No constant, no trend: Δyt = γyt-1 +  asΔyt-s + vt
●	Constant, no trend: Δyt = α + γyt-1 +  asΔyt-s + vt
●	Constant and trend: Δyt = α + γyt-1 + λt +  asΔyt-s + vt
You need to choose a lag length to run the test. The lag length should be chosen so that the residuals aren’t serially correlated. You’ve got several options for choosing lags: Minimize Akaike’s information criterion (AIC) or Bayesian information criterion (BIC), or drop lags until the last lag is statistically significant.
    
    ''')

content()