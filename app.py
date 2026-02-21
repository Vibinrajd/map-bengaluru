import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide")

st.title("Engine Distribution Map")

# Load Excel from specific sheet
@st.cache_data
def load_data():
    df = pd.read_excel("engine details.xlsx", sheet_name="CAMC")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Sidebar Filters
engine_filter = st.sidebar.multiselect(
    "Select Engine Type",
    df["Engine Type"].unique(),
    default=df["Engine Type"].unique()
)

cluster_filter = st.sidebar.multiselect(
    "Select Cluster",
    df["Cluster"].unique(),
    default=df["Cluster"].unique()
)

filtered_df = df[
    (df["Engine Type"].isin(engine_filter)) &
    (df["Cluster"].isin(cluster_filter))
].copy()

# Remove rows with missing lat-long
filtered_df = filtered_df.dropna(subset=["Latitude", "Longitude"])

# Radius scaling
filtered_df["radius"] = filtered_df["Total Value"] * 3000

# Color mapping
def color_engine(x):
    if x == "HHP":
        return [255, 0, 0, 160]
    else:
        return [0, 0, 255, 160]

filtered_df["color"] = filtered_df["Engine Type"].apply(color_engine)

# Map Layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    get_position='[Longitude, Latitude]',
    get_radius="radius",
    get_fill_color="color",
    pickable=True
)

tooltip = {
    "html": "<b>{Location_Standardized}</b><br/>"
            "Cluster: {Cluster}<br/>"
            "Total Value: {Total Value}<br/>"
            "Engine: {Engine Type}",
}

view_state = pdk.ViewState(
    latitude=filtered_df["Latitude"].mean(),
    longitude=filtered_df["Longitude"].mean(),
    zoom=6,
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip
))
