import folium
from folium.plugins import HeatMap
import pandas as pd

# -----------------------------
# HPI computation functions
# -----------------------------
# Example permissible limits (mg/L), adjust as needed
LIMITS = {'Pb': 0.01, 'Cd': 0.003, 'As': 0.01, 'Cr': 0.05, 'Hg': 0.001}

def compute_hpi_row(row, limits=LIMITS):
    """Compute HPI for a single row (dict or Series)."""
    s = 0.0
    wsum = 0.0
    for metal, limit in limits.items():
        conc = float(row.get(metal, 0) or 0)
        Qi = (conc / limit) * 100
        Wi = 1 / limit
        s += Qi * Wi
        wsum += Wi
    return round(s / wsum, 2) if wsum else None

def compute_hpi_from_csv(df):
    """Compute HPI for all rows in a DataFrame."""
    df['hpi'] = df.apply(lambda r: compute_hpi_row(r.to_dict()), axis=1)
    return df

# -----------------------------
# Map generation functions
# -----------------------------
def classify_hpi(hpi_value):
    """Classify water quality based on HPI."""
    if hpi_value <= 50:
        return "Excellent", "green"
    elif hpi_value <= 100:
        return "Good", "blue"
    elif hpi_value <= 150:
        return "Poor", "orange"
    else:
        return "Unsuitable", "red"

def generate_map(df, output_path="hmpi_map.html"):
    """
    Generate interactive Folium map with:
    - Weighted heatmap (intensity = HPI value)
    - Color-coded markers with popups
    - Layer control + legend
    """
    # Center map around average coords
    m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=12)

    # --- Heatmap layer ---
    heat_data = [[row["lat"], row["lon"], row["hpi"]] for _, row in df.iterrows()]
    heat_layer = HeatMap(
        heat_data,
        name="Pollution Heatmap",
        min_opacity=0.5,
        radius=25,
        blur=15,
        max_zoom=12
    )
    heat_layer.add_to(m)

    # --- Marker layer ---
    marker_group = folium.FeatureGroup(name="Sample Sites")
    for _, row in df.iterrows():
        category, color = classify_hpi(row["hpi"])
        popup_html = f"""
        <b>Site:</b> {row['site_name']}<br>
        <b>Coordinates:</b> ({row['lat']}, {row['lon']})<br>
        <b>HPI:</b> {row['hpi']:.2f}<br>
        <b>Category:</b> {category}
        """
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=6,
            popup=popup_html,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
        ).add_to(marker_group)

    marker_group.add_to(m)

    # --- Layer control ---
    folium.LayerControl().add_to(m)

    # --- Legend ---
    legend_html = """
     <div style="
         position: fixed; 
         bottom: 50px; left: 50px; width: 180px; height: 140px; 
         border:2px solid grey; z-index:9999; font-size:14px;
         background-color:white; padding: 10px;">
         <b>Water Quality Legend</b><br>
         <i style="background:green; width:10px; height:10px; float:left; margin-right:5px;"></i> Excellent (≤50)<br>
         <i style="background:blue; width:10px; height:10px; float:left; margin-right:5px;"></i> Good (≤100)<br>
         <i style="background:orange; width:10px; height:10px; float:left; margin-right:5px;"></i> Poor (≤150)<br>
         <i style="background:red; width:10px; height:10px; float:left; margin-right:5px;"></i> Unsuitable (>150)<br>
     </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save output
    m.save(output_path)
    return output_path
