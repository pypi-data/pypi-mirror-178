def arch():
    print('''
    
ARCH
Auto regressive conditional heteroscedasticity
It is a variance model. It is used to analyse the volatility to forecast future volatility. Arch modelling shows period or clusters of high volatility followed by high volatility and vice versa. They are dynamic in nature i.e. they respond to changes in the dataset.
Application:
They are useful when considering risk of holding an asset over different time periods.
Components of Arch Model:
·       Autoregressive-current value can be expressed as a function of past values or previous value. Current values are correlated with past values.
·       Conditional- In arch model, variance depends on past values.
·       Heteroskedasticity – Different volatility at time different time periods.
Volatility:
Numeric measures of uncertainty and depends on the volume of changes. Cannot be observed directly. Keeps evolving continuously.
Note: Less dispersed data results in capturing variance easily
 
Equation for arch – mean,variance
Variance = var(yt|yt-1) = var^2(t) (conditional variance) = alpha0 (constant)+summation from i=1 to p,alpha1(coefficient of first lagged term)*e^2(t-1)(squared error term of the previous period)
Conditional variance is dependent on past error term value
Mean(u) equation: xt(variable) = ut(mean-function of past value and past error)+et(residual value left)
Mean or ut can be modelled using arima/arma, et does not have autocorrelation in this eq, contrasting with variance eq in which e^2(t-1) had autocorrelation. Because et is system error of arch model
Observe the mean, if mean is time dependent, cannot apply older arma models. Then we apply arma-arch model.
How do we use arma-arch?
We model the variable using arma model. Apply arch model on the variance caused by unexpected shock.
3 equation vs 2 equation setup:
Xt = ut+et, ,xt = c0+phi1*(u(t-1))+et
Ut = c+phi1*u(t-1), , sigma^2(t) = alpha0+alpha1*(e^2(t-1))
Sigma^2t= alpha0+alpha1e^2(t-1)
When to use arch model?
The incapacity or failure of armodel, arima,sarima to incorporate volatility or heteroscedastic.
When u have volatility. Arch should only be applied to t.s that do not have any trends or any seasonal effects.
Only applied to time series that does not have trends or seasonal affects
#plot pacf
Why use arch
In capacity or failure of ar,ma,arma etc to incorporate heteroscedasticity or volatility wrt time 
The error is heteroscedastic 
Pacf: wont give you exact lags but closter of lags
#pacf plot of xt: draw normal lines up and down 
In x^2t: draw tall lines first and mark high volatility then small lines low volatility 
 
GARCH(p,q):
Arch and garch dont explain the trend in the error term, it only captures the error term 
It is a statistical model used to analyse time series where variance error is serially correlated. Model assumes :variance of error term follows arma process;variance of error term is not constant. Whenever there is heteroscedasticity, observations do not confirm linear pattern instead they tend to cluster. Model has conditional heteroscedastic(follows arma process pattern) i.e it is a function of an average of its own past values
Garch Model is an extension of arch model that incorporates MA components with AR components. It allows garch to model both: conditional change in variance over time. Changes in time dependent variance.
An extension of the arch model, all components of the arch could be present in garch as well.
Denotation: Garch (p,q)
p= AR process, ARCH effect, past values like y(t-1),y(t-2) etc
q= garch term: past e^2t values
Why is ma incorporated?- Incorporation of MA component allows garch model to model both:
-conditional change in variance over time
-changes in time dependent variance
Since garch is an extension of arch,all components of arch could be present in garch 
Arch: xt=ut+et
The same equation remains for Garch
Garch variance: sigma t^2= alpha(0)+ summation i=1 to p, alpha i*e^2(t-1)+summation j=1 to q,beta j * sigma(t-j)^2



    ''')


arch()