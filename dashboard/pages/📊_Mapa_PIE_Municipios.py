import streamlit as st
import streamlit.components.v1 as components
import os

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Mapa PIE Municipios",
    page_icon="📊",
    layout="wide"
)

# --- Obtener Años Disponibles ---
# Los mapas pregenerados van de 2007 a 2022
available_years = list(range(2007, 2022 + 1))
default_year = 2022

# --- Selector de Año en la Sidebar ---
st.sidebar.header("Configuración del Mapa")
selected_year = st.sidebar.selectbox(
    "Seleccione el Año:",
    options=available_years,
    index=available_years.index(default_year) # Por defecto el último año
)

# --- Título y Descripción Dinámicos ---
st.title(f"📊 Participación en Ingresos del Estado (PIE) por Municipio ({selected_year})")

st.markdown(f"""
Este mapa visualiza la **Participación en Ingresos del Estado (PIE)** para los municipios españoles correspondiente al año **{selected_year}**. 
La PIE es un componente crucial de la financiación municipal en España, distribuyendo recursos estatales entre los ayuntamientos 
en función de diversos criterios como la población, el esfuerzo fiscal y la capacidad tributaria.
""")

# --- Cargar y Mostrar el Mapa HTML ---
map_sub_dir = os.path.join(os.path.dirname(__file__), "exp", "mapa_pie_anual")
map_html_filename = f"mapa_pie_municipios_{selected_year}.html"
map_html_path = os.path.join(map_sub_dir, map_html_filename)

if os.path.exists(map_html_path):
    with open(map_html_path, 'r', encoding='utf-8') as f:
        html_map_content = f.read()
    
    st.subheader(f"Mapa Coroplético de la PIE Municipal ({selected_year})")
    components.html(html_map_content, height=650, scrolling=True)
    
    st.markdown(f"""
    **Interpretación del Mapa ({selected_year}):**
    - Los colores más oscuros indican una mayor cuantía en la participación de ingresos del estado.
    - **Transformación Logarítmica:** Para una mejor visualización de las diferencias entre municipios, dado el amplio rango de los valores de la PIE, se ha aplicado una transformación logarítmica (log10) a los datos. Esto significa que las diferencias de color representan cambios proporcionales más que absolutos.
    - **Cobertura:** El mapa incluye datos para los municipios españoles para los que se disponía de información de PIE y correspondencia geográfica en {selected_year}. Los municipios sin datos o que no pudieron ser mapeados se muestran en gris claro. (El número exacto de municipios mapeados varía ligeramente por año, típicamente alrededor de 6,500).
    - **Interactividad:** Puede hacer zoom y pasar el cursor sobre los municipios para ver el nombre, el valor original de la PIE y el código del municipio. Haga clic para obtener más detalles como la provincia y la CCAA.
    """)
else:
    st.error(f"No se pudo encontrar el archivo del mapa para el año {selected_year} en la ruta esperada: {map_html_path}")
    st.info(f"Asegúrese de que el archivo '{map_html_filename}' exista en la subcarpeta '{map_sub_dir}'. Puede que necesite ejecutar el script 'pregenerar_mapas_pie.py' (ubicado en la raíz del proyecto) para generar los mapas si fueron movidos o borrados.")

st.markdown("---")
st.markdown("""
**Fuente de los Datos:**
- **Datos PIE:** Los datos de la Participación en Ingresos del Estado (PIE) se han obtenido mediante un proceso de extracción automatizada (web scraping) de los archivos de liquidaciones municipales publicados por el **Ministerio de Hacienda de España**. Posteriormente, estos datos crudos son procesados, limpiados y unificados para su uso en este proyecto.
- **Datos Geoespaciales:** Las geometrías de los municipios provienen de **GeoRef Spain**.

**Proceso de Generación de los Mapas Anuales:**
1. Extracción de datos de la PIE para cada año (2007-2022) desde la base de datos del proyecto.
2. Creación de códigos municipales INE de 5 dígitos para la correcta unión con datos geográficos.
3. Unión de los datos de PIE con las geometrías municipales para cada año.
4. Generación de un mapa coroplético interactivo (archivo HTML) para cada año utilizando Folium.
   Los mapas individuales se almacenan y se cargan según el año seleccionado.
""")

st.sidebar.info(
    f"Esta página muestra la distribución de la Participación en Ingresos del Estado (PIE) "
    f"a nivel municipal para el año {selected_year}."
)
