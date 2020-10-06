def genforecast(data):
    from sktime.forecasting.model_selection import temporal_train_test_split
    import numpy as np
    import math
    y_train, y_test = temporal_train_test_split(data)
    fh = np.arange(1, len(y_test) + 1)
    testct=len(y_test)

    from sktime.forecasting.naive import NaiveForecaster
    forecaster = NaiveForecaster(strategy="drift")
    forecaster.fit(y_train)
    y_pred_naive=forecaster.predict(fh)
    from sktime.performance_metrics.forecasting import smape_loss
    naive_acc=round(smape_loss(y_pred_naive,y_test),4)
    #full model dev and forecast next 5 days
    forecaster.fit(data)
    futurewin=np.arange(1,6) # 5 day in future prediction
    fut_pred=forecaster.predict(futurewin)
    min_naive=round(min(fut_pred),2)
    max_naive=round(max(fut_pred),2)

    from sktime.forecasting.trend import PolynomialTrendForecaster
    forecaster = PolynomialTrendForecaster(degree=1)
    forecaster.fit(y_train)
    y_pred_poly=forecaster.predict(fh)
    from sktime.performance_metrics.forecasting import smape_loss
    poly_acc=round(smape_loss(y_pred_poly,y_test),4)
    #full model dev and forecast next 5 days
    forecaster.fit(data)
    futurewin=np.arange(1,6) # 5 day in future prediction
    fut_pred=forecaster.predict(futurewin)
    min_poly=round(min(fut_pred),2)
    max_poly=round(max(fut_pred),2)

    from sktime.forecasting.compose import EnsembleForecaster
    from sktime.forecasting.exp_smoothing import ExponentialSmoothing
    sp1=math.floor(len(y_test)/4)
    sp2=min(sp1,12)
    spval=max(2,sp2)
    forecaster = EnsembleForecaster([
        ("ses", ExponentialSmoothing(seasonal="multiplicative", sp=spval)),
        ("holt", ExponentialSmoothing(trend="add", damped=False, seasonal="multiplicative", sp=spval)),
        ("damped", ExponentialSmoothing(trend="add", damped=True, seasonal="multiplicative", sp=spval))
        ])
    forecaster.fit(y_train)
    y_pred_ensem = forecaster.predict(fh)
    ensem_acc=round(smape_loss(y_test, y_pred_ensem),4)
    #full model dev and forecast next 5 days
    forecaster.fit(data)
    futurewin=np.arange(1,6) # 5 day in future prediction
    fut_pred=forecaster.predict(futurewin)
    min_ensem=round(min(fut_pred),2)
    max_ensem=round(max(fut_pred),2)

    from sklearn.neighbors import KNeighborsRegressor
    regressor = KNeighborsRegressor(n_neighbors=1)
    from sktime.forecasting.compose import ReducedRegressionForecaster
    forecaster = ReducedRegressionForecaster(regressor=regressor, window_length=15, strategy="recursive")
    param_grid = {"window_length": [5, 10, 15]}
    from sktime.forecasting.model_selection import SlidingWindowSplitter
    from sktime.forecasting.model_selection import ForecastingGridSearchCV
    # we fit the forecaster on the initial window, and then use temporal cross-validation to find the optimal parameter
    cv = SlidingWindowSplitter(initial_window=int(len(y_train) * 0.5))
    gscv = ForecastingGridSearchCV(forecaster, cv=cv, param_grid=param_grid)
    gscv.fit(y_train)
    y_pred_redreg = gscv.predict(fh)
    redreg_acc=round(smape_loss(y_test, y_pred_redreg),4)
    #full model dev and forecast next 5 days
    gscv.fit(data)
    futurewin=np.arange(1,6) # 5 day in future prediction
    fut_pred=gscv.predict(futurewin)
    min_redreg=round(min(fut_pred),2)
    max_redreg=round(max(fut_pred),2)

    return min_naive, max_naive, min_poly, max_poly, min_ensem, max_ensem, min_redreg, max_redreg, y_test, testct, y_pred_naive, naive_acc, y_pred_poly, poly_acc, y_pred_ensem, ensem_acc, y_pred_redreg, redreg_acc

