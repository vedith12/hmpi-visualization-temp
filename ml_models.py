import pandas as pd
from sklearn.ensemble import RandomForestRegressor, IsolationForest
import joblib
from hpi_utils import compute_hpi_row

def train_models(csv_path, model_out='rf_model.pkl', anomaly_out='iso_model.pkl'):
    df = pd.read_csv(csv_path)
    df['hpi'] = df.apply(lambda r: compute_hpi_row(r.to_dict()), axis=1)
    X = df[['Pb','Cd','As','Cr','Hg']].fillna(0)
    y = df['hpi']
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    iso = IsolationForest(contamination=0.05, random_state=42)
    iso.fit(X)
    joblib.dump(rf, model_out)
    joblib.dump(iso, anomaly_out)
    return rf, iso

def predict_hpi(model, row):
    X = [[row.get('Pb',0), row.get('Cd',0), row.get('As',0), row.get('Cr',0), row.get('Hg',0)]]
    return float(model.predict(X)[0])
