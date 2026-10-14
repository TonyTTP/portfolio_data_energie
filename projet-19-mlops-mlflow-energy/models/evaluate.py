import numpy as np 
from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_percentage_error
from train import train_model

def evaluate_model():
    model, X_test, y_test = train_model()
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_pred,y_test))
    r2 = r2_score(y_test,y_pred)
    mask = y_test != 0 
    if mask.any():
        mape = mean_absolute_percentage_error(y_test[mask],y_pred[mask]) * 100
    else:
        mape = float("Nan")
    print(f"RMSE : {rmse:.4f} MW")
    print(f"R2 : {r2:.2f} MW")
    return {"rmse" : float(rmse), "r2" : float(r2), "mape" : float(mape),}

if __name__ == "__main__":
    evaluate_model()
