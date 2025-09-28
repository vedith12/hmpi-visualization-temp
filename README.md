
# HMPI Mapper - Starter Repo

This starter repo shows a minimal pipeline to compute Heavy Metal Pollution Index (HPI) from a CSV of groundwater samples and visualize them on an interactive map.

Files:
- sample_data.csv : example dataset (id, site_name, lat, lon, Pb, Cd, As, Cr, Hg, date)
- hpi_utils.py : utilities to compute HPI and convert CSV to GeoJSON
- ml_models.py : (starter) train/predict / anomaly detection using scikit-learn
- app_streamlit.py : minimal Streamlit frontend scaffold (upload CSV, show table, link to map)
- hmpi_map.html : static interactive map demo (Leaflet + heatmap + markers)
- requirements.txt : suggested Python packages

## Quick demo (open map)
Open `hmpi_map.html` in a browser to see a demo heatmap + sample markers (interactive).

## Run the Streamlit app (locally)
1. Create a virtualenv and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Run:
   ```bash
   streamlit run app_streamlit.py
   ```

## Notes
- The HPI formula used: for each metal Qi = (Ci / Si) * 100; Wi = 1/Si; HPI = sum(Qi*Wi)/sum(Wi).
  Update `LIMITS` in `hpi_utils.py` to match official standards (BIS/WHO/EPA) for your final report.
- The static map is generated for demo purposes and embeds GeoJSON; no server is required to view it.
- `ml_models.py` contains starter functions to train a RandomForestRegressor and IsolationForest for anomaly detection. With more labeled/temporal data you can develop prediction models (time-series or spatial ML).
