import streamlit as st
import pandas as pd
import sqlite3
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import os # Importado para manejo de rutas
import json # Added import

# Configuración de la página
st.set_page_config(page_title="Mapa de Densidad Poblacional", layout="wide")

st.title("Mapa Interactivo de Densidad de Población Municipal")

# --- Rutas a los archivos ---
# Se asume que el script se ejecuta desde la raíz del proyecto o Streamlit maneja las rutas relativas desde ahí.
# Si dashboard/pages/ es el CWD, las rutas serían "../../data base/datawarehouse.db", etc.
# Usamos rutas relativas desde la raíz del proyecto, consistentes con el script original.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Raíz del proyecto
DB_PATH = os.path.join(BASE_DIR, "data base", "datawarehouse.db")
# GEOJSON_PATH = os.path.join(BASE_DIR, "ETL", "GeoRef_Spain", "georef-spain-municipio.geojson") # Old path
TOPOJSON_PATH = os.path.join(BASE_DIR, "ETL", "GeoRef_Spain", "TopoJSON", "georef-spain-municipio.topojson") # New path to TopoJSON


# --- Funciones de carga de datos ---
@st.cache_data
def get_available_years(_conn):
    """Obtiene los años disponibles de la tabla de población."""
    try:
        cursor = _conn.cursor()
        cursor.execute("PRAGMA table_info(cifras_poblacion_municipio)")
        columns_info = cursor.fetchall()
        year_columns = sorted([info[1] for info in columns_info if info[1].isdigit()], reverse=True)
        return year_columns
    except sqlite3.Error as e:
        st.error(f"Error al obtener años de la base de datos: {e}")
        return []

@st.cache_data
def load_population_data(_conn, selected_year_str):
    """Carga datos de población para un año específico directamente de cifras_poblacion_municipio."""
    try:
        query_poblacion = f"SELECT mun_code, `{selected_year_str}` AS poblacion FROM cifras_poblacion_municipio WHERE `{selected_year_str}` IS NOT NULL"
        df_pop = pd.read_sql_query(query_poblacion, _conn)
        
        # Corregir mun_code: convertir a string, quitar decimales, y luego zfill
        df_pop['mun_code'] = df_pop['mun_code'].astype(str).str.split('.').str[0].str.zfill(5)
        df_pop['poblacion'] = pd.to_numeric(df_pop['poblacion'], errors='coerce').fillna(0)
        
        return df_pop
    except sqlite3.Error as e:
        st.error(f"Error al cargar datos de población: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Un error inesperado ocurrió al cargar datos de población: {e}")
        return pd.DataFrame()

@st.cache_data
def load_spatial_data(path): # Renamed from load_geojson_data
    """Carga los datos espaciales (TopoJSON) de los municipios y los preprocesa."""
    try:
        if not os.path.exists(path):
            st.error(f"Error: No se encontró el archivo TopoJSON en la ruta: {path}")
            return None

        gdf = gpd.read_file(path)
        
        # Manejo de CRS
        if gdf.crs is None:
            gdf.set_crs("EPSG:4326", inplace=True)
        elif gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")

        # Identificar y estandarizar mun_code
        code_col_options = ['mun_code', 'ine.ine_cod_municipio', 'natcode', 'cartodb_id']
        mun_code_col = None
        for col in code_col_options:
            if col in gdf.columns:
                mun_code_col = col
                break
        
        if not mun_code_col:
            st.error(f"No se pudo encontrar una columna de código municipal adecuada en el TopoJSON. Columnas disponibles: {gdf.columns.tolist()}")
            return None

        if pd.api.types.is_numeric_dtype(gdf[mun_code_col]):
             gdf[mun_code_col] = gdf[mun_code_col].astype(float).astype(int).astype(str).str.zfill(5)
        else:
             gdf[mun_code_col] = gdf[mun_code_col].astype(str).str.split('.').str[0].str.zfill(5)

        if mun_code_col != 'mun_code':
            gdf = gdf.rename(columns={mun_code_col: 'mun_code'})

        # Identificar y estandarizar mun_name
        name_col_options = ['mun_name', 'nameunit', 'nombre']
        mun_name_col = None
        for col in name_col_options:
            if col in gdf.columns:
                mun_name_col = col
                break
        
        if mun_name_col and mun_name_col != 'mun_name':
            gdf = gdf.rename(columns={mun_name_col: 'mun_name'})
        elif not mun_name_col:
            # st.info(f"Columna de nombre de municipio no encontrada. Se usará 'mun_code' como 'mun_name'.") # Optional info
            gdf['mun_name'] = gdf['mun_code']
        
        # Validar geometrías
        gdf = gdf[gdf.is_valid]
        
        # Seleccionar y retornar solo las columnas necesarias para la unión y visualización
        return gdf[['mun_code', 'mun_name', 'geometry']]
        
    except Exception as e:
        st.error(f"Error al cargar o procesar el archivo TopoJSON: {e}")
        return None

# --- Conexión a la base de datos ---
try:
    conn = sqlite3.connect(DB_PATH)
except sqlite3.Error as e:
    st.error(f"Error al conectar con la base de datos: {e}")
    st.stop() 

# --- Sidebar para selección de año ---
available_years = get_available_years(conn)
if not available_years:
    st.sidebar.error("No hay años disponibles para mostrar.")
    st.stop()

selected_year = st.sidebar.selectbox("Seleccione Año:", available_years)

# --- Carga y procesamiento de datos ---
df_population = load_population_data(conn, selected_year)
gdf_municipalities = load_spatial_data(TOPOJSON_PATH) # Updated function call and path

if df_population.empty or gdf_municipalities is None:
    st.warning("No se pudieron cargar los datos necesarios para generar el mapa (población o geometrías).")
    st.stop()

# Unir datos de población con datos geoespaciales
merged_gdf = gdf_municipalities.merge(df_population, on="mun_code", how="left")


# --- Secciones de diagnóstico (Post-Unión) ---
merged_gdf.dropna(subset=['poblacion', 'geometry'], inplace=True) 

if merged_gdf.empty:
    st.warning(f"No hay datos combinados para el año {selected_year} después de la unión y limpieza.")
    st.stop()

# --- Cálculo de Área y Densidad ---
try:
    merged_gdf_projected = merged_gdf.to_crs(epsg=25830)
    merged_gdf['area_km2'] = merged_gdf_projected.area / 1_000_000
except Exception as e:
    st.error(f"Error al calcular el área: {e}. Usando una aproximación si es posible.")
    merged_gdf['area_km2'] = merged_gdf.area * 10000 

merged_gdf['densidad_poblacion'] = merged_gdf['poblacion'] / merged_gdf['area_km2']
merged_gdf['densidad_poblacion'].fillna(0, inplace=True) 
merged_gdf.loc[merged_gdf['area_km2'] == 0, 'densidad_poblacion'] = 0 

# --- Creación del Mapa con Folium ---
st.markdown(f"### Densidad de Población por Municipio ({selected_year})")

merged_gdf = merged_gdf[merged_gdf.is_valid & ~merged_gdf.is_empty]

if merged_gdf.empty:
    st.warning(f"No hay geometrías válidas para mostrar en el mapa para el año {selected_year}.")
    st.stop()

map_center = [40.416775, -3.703790] 
m = folium.Map(location=map_center, zoom_start=6, tiles="cartodbpositron")

merged_gdf.replace([float('inf'), float('-inf')], 0, inplace=True)

try:
    # Asegurar que solo se pasan las columnas necesarias y que mun_code está en properties
    geojson_data_for_map = merged_gdf[['mun_code', 'geometry']].to_json()
    data_for_map = merged_gdf[['mun_code', 'densidad_poblacion']]

    folium.Choropleth(
        geo_data=geojson_data_for_map,
        name='Densidad Poblacional',
        data=data_for_map,
        columns=['mun_code', 'densidad_poblacion'],
        key_on='feature.properties.mun_code', 
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Densidad de Población (hab/km²) - {selected_year}',
        highlight=True
    ).add_to(m)
except Exception as e:
    st.error(f"Error al crear la capa Choropleth: {e}")
    st.error("Detalles del error: Es posible que haya problemas con los datos GeoJSON o los valores de densidad.")
    st.dataframe(merged_gdf[['mun_code', 'mun_name', 'poblacion', 'area_km2', 'densidad_poblacion']].head())


tooltip_data = merged_gdf[['geometry', 'mun_name', 'poblacion', 'area_km2', 'densidad_poblacion']]
tooltip_layer = folium.features.GeoJson(
    tooltip_data.to_json(), 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['mun_name', 'poblacion', 'area_km2', 'densidad_poblacion'], # Usar mun_name
        aliases=['Municipio:', f'Población ({selected_year}):', 'Área (km²):', 'Densidad (hab/km²):'],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """
    ),
    style_function=lambda x: {'fillOpacity': 0, 'weight': 0} 
)
tooltip_layer.add_to(m)

folium.LayerControl().add_to(m)

st_folium(m, width='100%', height=700)

if conn:
    conn.close()

st.markdown("---")
st.markdown("#### Notas:")
st.markdown("- La densidad de población se calcula como `población / área_km2`.")
st.markdown("- El área se calcula reproyectando las geometrías a EPSG:25830 (ETRS89 / UTM Zone 30N). Esto es más preciso para la península. Las islas pueden tener ligeras distorsiones.")
st.markdown("- Los municipios sin datos de población para el año seleccionado o sin geometría válida no se muestran.")

# Código original comentado para referencia (mapa de puntos simulados)
# ... (se omite el código anterior de puntos simulados)
