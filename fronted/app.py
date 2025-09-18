import streamlit as st
import folium
from streamlit_folium import st_folium
from utils import get_ndvi, get_flowering

st.set_page_config(page_title="NDVI & Flowering Map", layout="wide")
st.title("Visualización NDVI y Floración")

# Entradas del usuario
bbox_input = st.text_input("BBox (lon_min,lat_min,lon_max,lat_max)", "-78.6,-0.2,-78.5,0.0")
start_date = st.date_input("Fecha inicio")
end_date = st.date_input("Fecha fin")
ndvi_threshold = st.slider("NDVI threshold para floración", 0.0, 1.0, 0.35)

# Estado inicial
if "ndvi_data" not in st.session_state:
    st.session_state.ndvi_data = None
if "flowering_data" not in st.session_state:
    st.session_state.flowering_data = None

# Botones
col1, col2 = st.columns(2)
with col1:
    if st.button("Obtener NDVI"):
        st.session_state.ndvi_data = get_ndvi(bbox_input, start_date, end_date)

with col2:
    if st.button("Detectar Floración"):
        st.session_state.flowering_data = get_flowering(bbox_input, start_date, end_date, ndvi_threshold)

# --- MAPA BASE (siempre visible) ---
lon_min, lat_min, lon_max, lat_max = map(float, bbox_input.split(","))
m = folium.Map(location=[(lat_min + lat_max)/2, (lon_min + lon_max)/2], zoom_start=10)

# Pintar NDVI (verde)
if st.session_state.ndvi_data:
    for point in st.session_state.ndvi_data.get("values", []):
        folium.CircleMarker(
            location=[point["lat"], point["lon"]],
            radius=5,
            color="green",
            fill=True,
            fill_opacity=point.get("ndvi", 0.5),
            popup=f"NDVI: {point.get('ndvi', 'N/A')}"
        ).add_to(m)

# Pintar Floración (rojo)
if st.session_state.flowering_data:
    for point in st.session_state.flowering_data:
        folium.CircleMarker(
            location=[point["lat"], point["lon"]],
            radius=5,
            color="red",
            fill=True,
            fill_opacity=0.7,
            popup="Floración detectada"
        ).add_to(m)

# Mostrar el mapa SIEMPRE
st_folium(m, width=700, height=500)
