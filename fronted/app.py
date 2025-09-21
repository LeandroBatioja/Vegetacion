import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw, TimestampedGeoJson
import pandas as pd
import plotly.express as px
from datetime import date

# --- Configuración de la página ---
st.set_page_config(
    page_title="🌱 Dashboard Vegetación NASA",
    layout="wide",
    page_icon="🌿"
)

# --- Panel lateral de pestañas ---
tab_selection = st.sidebar.radio("Sección", ["Mapa", "NDVI", "Floración"])
st.sidebar.markdown("---")
start_date = st.sidebar.date_input("Fecha inicio", date.today())
end_date = st.sidebar.date_input("Fecha fin", date.today())
ndvi_threshold = st.sidebar.slider("Umbral NDVI", 0.0, 1.0, 0.35)
dark_mode = st.sidebar.checkbox("Modo oscuro", value=False)
update_btn = st.sidebar.button("Actualizar Datos")

# Bounding box inicial
if "bbox" not in st.session_state:
    st.session_state["bbox"] = [-80, -1, -77, 0.1]
if "ndvi_data" not in st.session_state:
    st.session_state["ndvi_data"] = None
if "bloom_data" not in st.session_state:
    st.session_state["bloom_data"] = None

# --- Funciones backend ---
def get_ndvi(bbox, start, end):
    try:
        url = f"http://127.0.0.1:8000/api/ndvi/area?bbox={','.join(map(str,bbox))}&start={start}&end={end}"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error NDVI: {e}")
        return None

def get_bloom(bbox, start, end, threshold):
    try:
        url = f"http://127.0.0.1:8000/api/detect/flower?bbox={','.join(map(str,bbox))}&start={start}&end={end}&ndvi_threshold={threshold}"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error Floración: {e}")
        return None

# --- Actualizar datos ---
if update_btn:
    st.session_state["ndvi_data"] = get_ndvi(st.session_state["bbox"], start_date, end_date)
    st.session_state["bloom_data"] = get_bloom(st.session_state["bbox"], start_date, end_date, ndvi_threshold)

ndvi_data = st.session_state["ndvi_data"]
bloom_data = st.session_state["bloom_data"]

# --- KPIs ---
col1, col2 = st.columns(2)
avg_ndvi = ndvi_data.get("average_ndvi",0) if ndvi_data else 0
bloom_percent = bloom_data.get("bloom_percent",0) if bloom_data else 0
col1.metric("NDVI promedio", f"{avg_ndvi:.2f}")
col2.metric("Floración detectada (%)", f"{bloom_percent:.0f}%")

# --- Mapa interactivo ---
if tab_selection == "Mapa":
    min_lon, min_lat, max_lon, max_lat = st.session_state["bbox"]
    center_lat = (min_lat + max_lat)/2
    center_lon = (min_lon + max_lon)/2
    tiles = "CartoDB positron" if not dark_mode else "CartoDB dark_matter"
    m = folium.Map(location=[center_lat, center_lon], zoom_start=7, tiles=tiles)

    draw = Draw(export=True, filename="bbox.geojson", draw_options={'rectangle': True})
    draw.add_to(m)

    # NDVI animado y permanente
    if ndvi_data and "time_series" in ndvi_data:
        features = []
        for date_str, points in ndvi_data["time_series"].items():
            for p in points:
                ndvi_val = p.get("ndvi", 0)
                color = "#ff4c4c" if ndvi_val < 0.2 else "#ffa500" if ndvi_val < 0.5 else "#2c6f3c"

                features.append({
                    "type":"Feature",
                    "geometry":{"type":"Point","coordinates":[p["lon"], p["lat"]]},
                    "properties":{
                        "time":date_str,
                        "style":{"color":color,"radius":6,"fillColor":color,"fillOpacity":0.8},
                        "popup":f"<b style='color:black;'>📅 {date_str}</b><br><b style='color:black;'>🌿 NDVI: {ndvi_val:.2f}</b>"
                    }
                })

                folium.CircleMarker(
                    location=[p["lat"], p["lon"]],
                    radius=6,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.8,
                    tooltip=folium.Tooltip(f"🌿 NDVI: {ndvi_val:.2f}", sticky=True, style="background-color:white; color:black; font-weight:bold;")
                ).add_to(m)

        TimestampedGeoJson(
            {"type":"FeatureCollection","features":features},
            period="P1D",
            add_last_point=True,
            auto_play=False,
            loop=False,
            max_speed=1,
            loop_button=True,
            date_options='YYYY-MM-DD',
            time_slider_drag_update=True
        ).add_to(m)

    # Floración
    if bloom_data and "flowers" in bloom_data:
        for f in bloom_data["flowers"]:
            folium.CircleMarker(
                location=[f["lat"], f["lon"]],
                radius=7,
                color="#ff69b4",
                fill=True,
                fill_color="#ff69b4",
                fill_opacity=0.9,
                tooltip=folium.Tooltip(f"🌸 Floración NDVI: {f['ndvi']:.2f}", sticky=True, style="background-color:white; color:black; font-weight:bold;")
            ).add_to(m)

    # Leyenda profesional
    legend_bg = "#ffffff" if not dark_mode else "#2c2c2c"
    legend_color = "black" if not dark_mode else "white"
    legend_html = f'''
    <div style="
        position: fixed;
        bottom: 80px; left: 10px; width: 230px; height: 160px;
        border:2px solid grey; z-index:9999; font-size:14px;
        background-color: {legend_bg}; padding: 10px;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        color: {legend_color};
        border-radius: 8px;
        ">
    <b>🔎 Leyenda</b><br>
    <span style="display:inline-block;width:16px;height:16px;background:#ff4c4c;margin-right:5px;"></span> Bajo (&lt;0.2)<br>
    <span style="display:inline-block;width:16px;height:16px;background:#ffa500;margin-right:5px;"></span> Medio (&lt;0.5)<br>
    <span style="display:inline-block;width:16px;height:16px;background:#2c6f3c;margin-right:5px;"></span> Alto (&ge;0.5)<br>
    <span style="display:inline-block;width:16px;height:16px;background:#ff69b4;margin-right:5px;"></span> Floración 🌸<br>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    draw_data = st_folium(m, width=950, height=500, returned_objects=['last_active_drawing'])
    if draw_data and draw_data.get("last_active_drawing"):
        coords = draw_data["last_active_drawing"]["geometry"]["coordinates"][0]
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        st.session_state["bbox"] = [min(lons), min(lats), max(lons), max(lats)]

# --- Sección NDVI ---
elif tab_selection == "NDVI":
    st.subheader("📈 NDVI Temporal")
    if ndvi_data and "time_series" in ndvi_data:
        df_list=[]
        for date_str, points in ndvi_data["time_series"].items():
            for p in points:
                df_list.append({"date":date_str,"ndvi":p["ndvi"]})
        df = pd.DataFrame(df_list)
        df_avg = df.groupby("date").mean().reset_index()
        fig_ndvi = px.line(df_avg, x="date", y="ndvi", title="NDVI Promedio Temporal",
                           markers=True, template="plotly_dark" if dark_mode else "plotly_white")
        st.plotly_chart(fig_ndvi, use_container_width=True)
        # CSV NDVI
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar NDVI CSV", csv, "ndvi_data.csv", "text/csv")

# --- Sección Floración ---
elif tab_selection == "Floración":
    st.subheader("🌸 Floración Detectada")
    if bloom_data and "flowers" in bloom_data:
        df_flowers = pd.DataFrame(bloom_data["flowers"])
        if not df_flowers.empty:
            df_flowers["count"] = 1
            fig_bloom = px.bar(df_flowers, x=df_flowers.index, y="count",
                               title="Número de Floraciones Detectadas",
                               template="plotly_dark" if dark_mode else "plotly_white")
            st.plotly_chart(fig_bloom, use_container_width=True)
            csv_f = df_flowers.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Descargar Floración CSV", csv_f, "flowers_data.csv", "text/csv")
    else:
        st.info("No se detectaron floraciones en las fechas seleccionadas.")
