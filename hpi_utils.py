import pandas as pd
import json

# Default permissible limits (mg/L) -- check and update with official standards in final submission
LIMITS = {'Pb': 0.01, 'Cd': 0.003, 'As': 0.01, 'Cr': 0.05, 'Hg': 0.001}

def compute_hpi_row(row, limits=LIMITS):
    s = 0.0
    wsum = 0.0
    for metal, limit in limits.items():
        conc = float(row.get(metal, 0) or 0)
        Qi = (conc / limit) * 100.0
        Wi = 1.0 / limit
        s += Qi * Wi
        wsum += Wi
    return s / wsum if wsum else None

def csv_to_geojson(csv_path):
    df = pd.read_csv(csv_path)
    # compute hpi
    df['hpi'] = df.apply(lambda r: compute_hpi_row(r.to_dict()), axis=1)
    features = []
    for _, r in df.iterrows():
        feat = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [float(r['lon']), float(r['lat'])]},
            "properties": {
                "id": int(r['id']),
                "site_name": r.get('site_name', ''),
                "hpi": round(float(r['hpi']), 2),
                "Pb": float(r.get('Pb', 0)),
                "Cd": float(r.get('Cd', 0)),
                "As": float(r.get('As', 0)),
                "Cr": float(r.get('Cr', 0)),
                "Hg": float(r.get('Hg', 0))
            }
        }
        features.append(feat)
    return {"type": "FeatureCollection", "features": features}
