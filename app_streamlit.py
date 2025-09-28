import streamlit as st
import pandas as pd
import json, os
from hpi_utils import csv_to_geojson, compute_hpi_row

st.set_page_config(layout="wide", page_title="HMPI Mapper - Demo")
st.title("HMPI Mapper — CSV upload, HPI computation & map visualization (Demo)")

st.markdown('''
Upload a CSV file with columns: id, site_name, lat, lon, Pb, Cd, As, Cr, Hg, date
- The app computes HPI per sample and shows interactive visualizations (heatmap + color-coded points).
- Example CSV provided in the repository as `sample_data.csv`.
''')

uploaded = st.file_uploader("Upload CSV", type=["csv"])
if uploaded is None:
    if st.button("Use sample data (provided)"):
        uploaded = open("sample_data.csv","rb")

if uploaded:
    df = pd.read_csv(uploaded)
    st.subheader("Raw data preview")
    st.dataframe(df.head())

    # compute HPI
    df['hpi'] = df.apply(lambda r: compute_hpi_row(r.to_dict()), axis=1)
    st.subheader("Computed HPI (per-sample)")
    st.dataframe(df[['id','site_name','hpi','Pb','Cd','As','Cr','Hg']].round(3))

    # create geojson for frontend map (simple inline map using leaflet)
    st.markdown("### Map preview (opens in new tab as HTML)")
    html_file = "hmpi_map.html"
    if os.path.exists(html_file):
        st.markdown(f"[Open interactive map HTML]({html_file})")
    else:
        st.write("Map HTML not available locally in this Streamlit demo. Use the provided hmpi_map.html in the repo.")
