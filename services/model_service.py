import pickle
import numpy as np

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def predict(data):
    arr = np.array([[ 
        data.age,
        data.session_duration,
        data.pages_visited,
        data.purchase_amount,
        data.is_mobile
    ]])

    pred = model.predict(arr)[0]
    prob = model.predict_proba(arr)[0][1]

    return pred, prob