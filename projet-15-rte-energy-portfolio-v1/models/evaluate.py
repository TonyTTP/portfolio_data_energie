import numpy as np
from sklearn.metrics import mean_squared_error

def calculate_rmse(y_true,y_pred):
    rmse = np.sqrt(mean_squared_error(y_true,y_pred))
    return rmse

def calculate_mape(y_true,y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    mask = y_true != 0

    mape = np.mean(np.abs((y_true[mask] - y_pred[mask])/ y_true[mask]))*100
    return mape

def evaluate(y_true,y_pred):
    rmse = calculate_rmse(y_true,y_pred)
    mape = calculate_mape(y_true,y_pred)

    print(f"rmse : {rmse:.2f} MW")
    print(f"mape : {mape:.2f} %")

    return {"rmse": rmse,"mape": mape}

if __name__ == "__main__":
    y_true = [50000, 52000, 48000, 0]
    y_pred = [51000, 51000, 49000, 100]
    evaluate(y_true,y_pred)