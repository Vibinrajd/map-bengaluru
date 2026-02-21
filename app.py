import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide")

st.title("Bengaluru Region Engine Distribution")
@st.cache_data
def load_data():
    df = pd.read_excel("engine details.xlsx", sheet_name="Sheet7")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Drop rows without coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# Scale bubble size
df["radius"] = df["Grand Total"] * 80  # adjust multiplier if needed

# Color logic (more HHP = redder, more LHP = bluer)
def color_logic(row):
    if row["HHP"] > row["LHP"]:
        return [255, 0, 0, 160]
    elif row["LHP"] > row["HHP"]:
        return [0, 0, 255, 160]
    else:
        return [128, 128, 128, 160]

df["color"] = df.apply(color_logic, axis=1)

# Layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[Longitude, Latitude]',
    get_radius="radius",
    get_fill_color="color",
    pickable=True,
)

tooltip = {
    "html": "<b>{Region}</b><br/>"
            "HHP: {HHP}<br/>"
            "LHP: {LHP}<br/>"
            "Total: {Grand Total}",
}

view_state = pdk.ViewState(
    latitude=df["Latitude"].mean(),
    longitude=df["Longitude"].mean(),
    zoom=10,
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip
))
