import streamlit as st
import pandas as pd
import pydeck as pdk

# Load your data (replace with your file)
df = pd.read_excel("engine details.xlsx")

# Clean column names if needed
df.columns = df.columns.str.strip()

# Optional filter
engine_filter = st.selectbox(
    "Select Engine Type",
    options=df["Engine Type"].unique()
)

filtered_df = df[df["Engine Type"] == engine_filter]

# Scale radius based on Total Value
filtered_df["radius"] = filtered_df["Total Value"] * 5000

# Create PyDeck layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    get_position='[Longitude, Latitude]',
    get_radius="radius",
    get_fill_color="[200, 30, 0, 160]",
    pickable=True
)

# Tooltip
tooltip = {
    "html": "<b>Location:</b> {Location_Standardized}<br/>"
            "<b>Cluster:</b> {Cluster}<br/>"
            "<b>Total Value:</b> {Total Value}",
    "style": {"backgroundColor": "steelblue", "color": "white"}
}

# Map
st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=12.9716,
        longitude=77.5946,
        zoom=6,
        pitch=0,
    ),
    layers=[layer],
    tooltip=tooltip
))
