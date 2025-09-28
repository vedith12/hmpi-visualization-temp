import streamlit as st
import pandas as pd
import os
from hpi_utils import compute_hpi_from_csv, generate_map
import streamlit.components.v1 as components

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
        uploaded = open("sample_data.csv", "rb")

if uploaded:
    df = pd.read_csv(uploaded)
    st.subheader("Raw data preview")
    st.dataframe(df.head())

    # compute HPI for all rows
    df = compute_hpi_from_csv(df)
    st.subheader("Computed HPI (per-sample)")
    st.dataframe(df[['id','site_name','hpi','Pb','Cd','As','Cr','Hg']].round(3))

    # generate interactive map and embed in Streamlit
    st.subheader("Interactive map")
    map_file = "uploaded_map.html"
    generate_map(df, map_file)

    # embed map directly
    with open(map_file, "r", encoding="utf-8") as f:
        map_html = f.read()
    components.html(map_html, height=600)
