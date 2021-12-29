import numpy as np
from statsmodels.tsa.arima_model import ARIMA,ARMA
from sklearn.metrics import mean_squared_error


def data_split(dataset, n_test_set=30):
    """
    split data into train and test sets

    Arguments:
    ----------
    dataset: pd.DataFrame
        - time series dataset
    n_test_set: int
        - the last n data points

    Returns:
    --------
    X_train : pd.DataFrame
        - training set
    X_test : pd.DataFrame
        - test set
    """
    X_train, X_test = dataset[:-n_test_set], dataset[-n_test_set::]

    return X_train, X_test

def rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))


def evaluate_arima_model(X_train, X_test, arima_order):
    """
    Train, predict and evaluate ARIMA model

    Arguments:
    ----------
    - X_train: numpy array
        - train set
    - X_test: numpy array
        - test set
    - arima_order: tuple
        - (p,d,q)

    Returns:
    --------
    - error: float
        - RMSE
    - predictions: numpy array
        - output predictions
    """

    history = [x for x in X_train]
    # make predictions
    predictions = list()

    for t in range(len(X_test)):
        model = ARIMA(history, order=arima_order)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat[0])
        history.append(X_test.values[t])

    # calculate out of sample error
    error = rmse(X_test, predictions)

    return error, predictions


# evaluate combinations of p, d and q values for an ARIMA model
def arima_grid_search(X_train, X_test, p_values, d_values, q_values):
    """
    grid search of arguments

    Arguments:
    ----------
    - X_train: numpy array
        - train set
    - X_test: numpy array
        - test set
    - p_values: numpy_array
        - a list of values for p parameter
    - d_values: numpy_array
        - a list of values for d parameter
    - q_values: numpy_array
        - a list of values for q parameter

    Returns:
    --------
    - best_cfg: tuple
        - best model parameter (p,d,q)
    - best_score: numpy array
        -  best rmse score
    """

    best_score, best_cfg = float("inf"), None

    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p, d, q)
                try:
                    rmse, _ = evaluate_arima_model(X_train, X_test, order)
                    if rmse < best_score:
                        best_score, best_cfg = rmse, order
                    print("ARIMA(%d,%d,%d) RMSE=%.3f" % (p, d, q, rmse))

                except:
                    continue

    print("Best ARIMA%s MSE=%.3f" % (best_cfg, best_score))

    return best_cfg, best_score


# ARMA 
def evaluate_arma_model(X_train, X_test, arma_order):
    """
    Train, predict and evaluate ARIMA model

    Arguments:
    ----------
    - X_train: numpy array
        - train set
    - X_test: numpy array
        - test set
    - arma_order: tuple
        - (p,q)

    Returns:
    --------
    - error: float
        - RMSE
    - predictions: numpy array
        - output predictions
    """

    history = [x for x in X_train]
    # make predictions
    predictions = list()

    for t in range(len(X_test)):
        model = ARMA(history, order=arma_order)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat[0])
        history.append(X_test.values[t])

    # calculate out of sample error
    error = rmse(X_test, predictions)

    return error, predictions


def arma_grid_search(X_train, X_test, p_values,q_values):
    """
    grid search of arguments

    Arguments:
    ----------
    - X_train: numpy array
        - train set
    - X_test: numpy array
        - test set
    - p_values: numpy_array
        - a list of values for p parameter
    - q_values: numpy_array
        - a list of values for q parameter

    Returns:
    --------
    - best_cfg: tuple
        - best model parameter (p,d,q)
    - best_score: numpy array
        -  best rmse score
    """

    best_score, best_cfg = float("inf"), None

    for p in p_values:
        for q in q_values:
            order = (p,q)
            try:
                rmse, _ = evaluate_arma_model(X_train, X_test, order)
                if rmse < best_score:
                    best_score, best_cfg = rmse, order
                print("ARIMA(%d,%d,%d) RMSE=%.3f" % (p,q, rmse))

            except:
                continue

    print("Best ARMA%s MSE=%.3f" % (best_cfg, best_score))

    return best_cfg, best_score