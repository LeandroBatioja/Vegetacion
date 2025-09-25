# 🌱 Proyecto de Monitoreo de Vegetación con NDVI y Floración

Este proyecto integra un **backend en FastAPI** y un **frontend en Streamlit** para procesar imágenes satelitales y generar análisis de **índice de vegetación (NDVI)** y **detección de floración**.  

El objetivo es proveer una interfaz simple e interactiva para visualizar datos geoespaciales procesados en tiempo real.

---

## 📌 Estructura del proyecto

    proyecto-vegetacion/
    ├─ backend/
    │ ├─ app/
    │ │ ├─ main.py # Punto de entrada FastAPI
    │ │ ├─ api/
    │ │ │ ├─ login.py # Autenticación
    │ │ │ ├─ ndvi.py # Endpoint NDVI
    │ │ │ └─ detect.py # Endpoint detección de flores
    │ │ ├─ services/
    │ │ │ ├─ ndvi_service.py # Lógica de NDVI
    │ │ │ └─ flower_service.py # Lógica detección floración
    │ │ ├─ models/
    │ │ │ └─ user_model.py # Modelo de usuarios
    │ │ └─ utils/
    │ │ └─ auth.py # Manejo de autenticación JWT
    │ └─ requirements.txt
    │
    └─ fronted/
    ├─ app.py # Interfaz Streamlit
    └─ requirements.txt


📊 Flujo de la aplicación

1.-El usuario selecciona un área en el mapa.

2.- El backend (FastAPI):

    a.- Procesa las imágenes para calcular NDVI.

    b.- Detecta la floración en áreas específicas.

    c.- Retorna los datos procesados como JSON o imágenes.


3.-El frontend (Streamlit):

    a.- Muestra un mapa interactivo con capas de NDVI y floración.

    b.- Incluye una leyenda de colores:

        🔴 Bajo (<0.2)

        🟡 Medio (<0.5)

        🟢 Alto (≥0.5)

        🌸 Floración

    c.- Permite descargar y visualizar los resultados.

🗺️ Mapa en el Frontend

El mapa se genera con Folium y se incrusta en Streamlit.

Capas:

    NDVI → puntos coloreados según el rango.

    Floración → puntos en rosado.

La leyenda aparece en un recuadro para fácil interpretación.



🚀 Endpoints principales (FastAPI)

    POST /api/login → Autenticación de usuario.

    POST /api/ndvi → Procesamiento de NDVI.

    POST /api/detect → Detección de floración.

📦 Requisitos principales

    Python 3.10+

    FastAPI

    Uvicorn

    Pandas

    NumPy

    Pillow

    Streamlit

    Folium


📌 Notas

    Ejecutar backend primero y luego el frontend.

    Si necesitas conectarlo desde otra máquina en la red local, cambia API_URL en fronted/app.py:

    API_URL = "http://<IP_DEL_SERVIDOR>:8000/api"


✨ Autor
    👨‍💻 Desarrollado por Leandro – Escuela de Sistemas, PUCE Esmeraldas.