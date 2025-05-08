import streamlit as st
import pandas as pd
import sqlite3
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Mapa Interactivo", layout="wide")

st.title("Mapa Interactivo de Municipios")

# Conexión a la base de datos
conn = sqlite3.connect("data base/datawarehouse.db")

# Leer datos de municipios y población
df = pd.read_sql_query(
    "SELECT mun_code, `2023` as poblacion FROM cifras_poblacion_municipio WHERE `2023` IS NOT NULL",
    conn
)

# Leer equivalencias para obtener nombres y coordenadas (si existieran)
equiv = pd.read_sql_query(
    "SELECT mun_code, NOMBRE FROM tabla_equivalencias",
    conn
)

df = df.merge(equiv, on="mun_code", how="left")

# NOTA: Para un mapa real, se necesitan coordenadas de cada municipio.
# Aquí se simulan coordenadas aleatorias para ejemplo.
import numpy as np
np.random.seed(42)
df["lat"] = np.random.uniform(36, 43, size=len(df))
df["lon"] = np.random.uniform(-9, 3, size=len(df))

# Crear mapa base centrado en España
m = folium.Map(location=[40.0, -3.7], zoom_start=6)

# Añadir puntos al mapa
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=5,
        popup=f"{row['NOMBRE']}<br>Población: {int(row['poblacion'])}",
        color="blue",
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

st.markdown("### Mapa de población por municipio (coordenadas simuladas)")
st_folium(m, width=900, height=600)
