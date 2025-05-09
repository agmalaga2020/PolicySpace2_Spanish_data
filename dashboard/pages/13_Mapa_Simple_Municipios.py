import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import st_folium
import os
import pandas as pd # Added import

# Configuración de la página
st.set_page_config(page_title="Mapa Simple de Municipios", layout="wide")

st.title("🗺️ Mapa Simple de Municipios de España")
st.markdown("Este mapa muestra los polígonos de los municipios de España directamente desde el archivo GeoJSON.")

# --- Constantes ---
GEOJSON_FILENAME = "georef-spain-municipio.geojson"
# La ruta al GeoJSON es relativa a la carpeta raíz del proyecto
GEOJSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
    "ETL", 
    "GeoRef_Spain", 
    GEOJSON_FILENAME
)

# --- Funciones de Carga de Datos ---
@st.cache_data
def load_geojson_data(path):
    """Carga los datos GeoJSON de los municipios."""
    try:
        if not os.path.exists(path):
            st.error(f"Error: No se encontró el archivo GeoJSON en la ruta: {path}")
            return None
        
        gdf = gpd.read_file(path)
        
        # Estandarizar CRS a EPSG:4326 si es necesario
        if gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")

        # Identificar columnas de código y nombre del municipio
        # Comprobamos posibles nombres para la columna de código municipal
        code_col_options = ['mun_code', 'ine.ine_cod_municipio', 'natcode', 'cartodb_id'] # Añadido cartodb_id por si acaso
        name_col_options = ['mun_name', 'nameunit', 'nombre']

        mun_code_col = None
        for col in code_col_options:
            if col in gdf.columns:
                mun_code_col = col
                break
        
        mun_name_col = None
        for col in name_col_options:
            if col in gdf.columns:
                mun_name_col = col
                break

        if not mun_code_col:
            st.error(f"No se pudo encontrar una columna de código municipal adecuada en el GeoJSON. Columnas disponibles: {gdf.columns.tolist()}")
            return None
        # if not mun_name_col: # Comentado para permitir que mun_name se cree a partir de mun_code si no existe
        #     st.warning(f"No se pudo encontrar una columna de nombre municipal en el GeoJSON. Se usará el código. Columnas disponibles: {gdf.columns.tolist()}")


        # Estandarizar el código municipal a string de 5 dígitos con ceros a la izquierda si es numérico
        # Primero asegurar que es string, luego quitar decimales si los tiene, finalmente zfill
        if pd.api.types.is_numeric_dtype(gdf[mun_code_col]):
             gdf[mun_code_col] = gdf[mun_code_col].astype(float).astype(int).astype(str).str.zfill(5)
        else:
             gdf[mun_code_col] = gdf[mun_code_col].astype(str).str.split('.').str[0].str.zfill(5)


        # Renombrar columnas para consistencia si es necesario y existen
        if mun_code_col != 'mun_code':
            gdf = gdf.rename(columns={mun_code_col: 'mun_code'})
        
        if mun_name_col and mun_name_col != 'mun_name':
            gdf = gdf.rename(columns={mun_name_col: 'mun_name'})
        elif not mun_name_col: # Si no hay columna de nombre, crear una a partir del código
            st.info(f"Columna de nombre de municipio no encontrada ('{name_col_options}'). Se usará 'mun_code' como 'mun_name'.")
            gdf['mun_name'] = gdf['mun_code']


        # Asegurarse de que la geometría es válida
        gdf = gdf[gdf.is_valid]
        
        st.success(f"GeoJSON cargado correctamente con {len(gdf)} municipios.")
        st.write("Primeras filas del GeoDataFrame (para depuración):")
        st.dataframe(gdf[['mun_code', 'mun_name', 'geometry']].head())
        st.write(f"Columnas encontradas y usadas: Código original='{mun_code_col}' (renombrada a 'mun_code'), Nombre original='{mun_name_col if mun_name_col else 'No encontrada'}' (renombrada/creada como 'mun_name')")
        return gdf

    except Exception as e:
        st.error(f"Error al cargar o procesar el archivo GeoJSON: {e}")
        return None

# --- Cargar Datos ---
gdf_municipios = load_geojson_data(GEOJSON_PATH)

if gdf_municipios is not None and not gdf_municipios.empty:
    st.subheader("Visualización del Mapa de Municipios")

    # Crear mapa base centrado en España
    # Coordenadas aproximadas del centro de España
    map_center = [40.416775, -3.703790] 
    m = folium.Map(location=map_center, zoom_start=6, tiles="cartodbpositron")

    # Añadir capa GeoJSON al mapa
    # Usar 'mun_name' y 'mun_code' si están disponibles después del preprocesamiento
    tooltip_fields = []
    if 'mun_name' in gdf_municipios.columns:
        tooltip_fields.append('mun_name')
    if 'mun_code' in gdf_municipios.columns:
        tooltip_fields.append('mun_code')
    
    if not tooltip_fields: # Fallback si ninguna columna esperada está
        st.warning("Columnas 'mun_name' o 'mun_code' no encontradas para el tooltip. Usando las primeras dos columnas disponibles.")
        tooltip_fields = list(gdf_municipios.columns[:2]) 

    try:
        folium.GeoJson(
            gdf_municipios,
            name="Municipios de España",
            style_function=lambda feature: {
                'fillColor': '#FFEDA0', # Color de relleno amarillo claro
                'color': 'black',       # Color del borde
                'weight': 0.5,          # Grosor del borde
                'fillOpacity': 0.7,
            },
            tooltip=folium.features.GeoJsonTooltip(
                fields=tooltip_fields,
                aliases=[f"{field.replace('_',' ').title()}:" for field in tooltip_fields],
                localize=True,
                sticky=False,
                labels=True,
                style="""
                    background-color: #F0EFEF;
                    border: 2px solid black;
                    border-radius: 3px;
                    box-shadow: 3px;
                """,
                max_width=800,
            ),
            highlight_function=lambda x: {'weight':3, 'fillColor':'grey'},
        ).add_to(m)

        # Mostrar el mapa en Streamlit
        st_folium(m, width=None, height=700, use_container_width=True)
        st.caption("Pasa el ratón sobre un municipio para ver su nombre y código.")

    except Exception as e:
        st.error(f"Error al generar la capa GeoJson para Folium: {e}")
        st.error("Esto podría deberse a problemas con los nombres de las columnas para los tooltips o con los datos de geometría.")
        st.error(f"Columnas disponibles en gdf_municipios: {gdf_municipios.columns.tolist()}")
        st.error(f"Campos seleccionados para tooltip: {tooltip_fields}")


else:
    st.warning("No se pudieron cargar los datos geoespaciales de los municipios o el archivo está vacío.")
    st.info(f"Ruta intentada para el GeoJSON: {GEOJSON_PATH}")

st.sidebar.info("Este es un mapa de prueba para verificar la carga y visualización de polígonos municipales.")
