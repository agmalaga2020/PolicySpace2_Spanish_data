import streamlit as st
import pandas as pd
import sqlite3
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import os # Importado para manejo de rutas

# Configuración de la página
st.set_page_config(page_title="Mapa de Densidad Poblacional", layout="wide")

st.title("Mapa Interactivo de Densidad de Población Municipal")

# --- Rutas a los archivos ---
# Se asume que el script se ejecuta desde la raíz del proyecto o Streamlit maneja las rutas relativas desde ahí.
# Si dashboard/pages/ es el CWD, las rutas serían "../../data base/datawarehouse.db", etc.
# Usamos rutas relativas desde la raíz del proyecto, consistentes con el script original.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Raíz del proyecto
DB_PATH = os.path.join(BASE_DIR, "data base", "datawarehouse.db")
GEOJSON_PATH = os.path.join(BASE_DIR, "ETL", "GeoRef_Spain", "georef-spain-municipio.geojson")


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
def load_geojson_data(path):
    """Carga los datos GeoJSON de los municipios y extrae mun_name."""
    try:
        gdf = gpd.read_file(path)
        
        if 'mun_code' not in gdf.columns:
            if 'ine.ine_cod_municipio' in gdf.columns:
                gdf.rename(columns={'ine.ine_cod_municipio': 'mun_code'}, inplace=True)
            elif 'natcode' in gdf.columns:
                gdf.rename(columns={'natcode': 'mun_code'}, inplace=True)
            else:
                st.error("No se encontró una columna de código municipal adecuada ('mun_code', 'ine.ine_cod_municipio', o 'natcode') en el GeoJSON.")
                return None
        
        if 'mun_name' not in gdf.columns:
            st.warning("La columna 'mun_name' no se encontró en el GeoJSON. Los nombres de municipios pueden faltar en los tooltips.")
            gdf['mun_name'] = "Nombre no disponible" 

        gdf['mun_code'] = gdf['mun_code'].astype(str).str.split('.').str[0].str.zfill(5)
        
        # Seleccionar y retornar solo las columnas necesarias
        return gdf[['mun_code', 'mun_name', 'geometry']]
    except Exception as e:
        st.error(f"Error al cargar el archivo GeoJSON: {e}")
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
gdf_municipalities = load_geojson_data(GEOJSON_PATH)

# --- Secciones de diagnóstico (Pre-Unión) ---
st.subheader("Diagnóstico de Datos (Pre-Unión)")
st.write(f"Año seleccionado: {selected_year}")
if not df_population.empty:
    st.write(f"Municipios con datos de población ({selected_year}): {len(df_population)}")
    st.write("Primeras filas de datos de población (df_population):")
    st.dataframe(df_population.head())
    st.write(f"Tipos de datos en df_population['mun_code']: {df_population['mun_code'].dtype}")
    # Mostrar algunos códigos de ejemplo de población
    st.write("Ejemplos de mun_code en df_population:", df_population['mun_code'].sample(min(5, len(df_population))).tolist() if not df_population.empty else "N/A")

else:
    st.warning(f"No se cargaron datos de población para el año {selected_year}.")

if gdf_municipalities is not None:
    st.write(f"Geometrías de municipios cargadas: {len(gdf_municipalities)}")
    st.write("Primeras filas de datos GeoJSON (gdf_municipalities):")
    st.dataframe(gdf_municipalities.head())
    st.write(f"Tipos de datos en gdf_municipalities['mun_code']: {gdf_municipalities['mun_code'].dtype}")
    # Mostrar algunos códigos de ejemplo del GeoJSON
    st.write("Ejemplos de mun_code en gdf_municipalities:", gdf_municipalities['mun_code'].sample(min(5, len(gdf_municipalities))).tolist() if gdf_municipalities is not None and not gdf_municipalities.empty else "N/A")

else:
    st.warning("No se cargaron datos GeoJSON de municipalidades.")


if df_population.empty or gdf_municipalities is None:
    st.warning("No se pudieron cargar los datos necesarios para generar el mapa (población o geometrías).")
    st.stop()

# Unir datos de población con datos geoespaciales
merged_gdf = gdf_municipalities.merge(df_population, on="mun_code", how="left")


# --- Secciones de diagnóstico (Post-Unión) ---
st.subheader("Diagnóstico de Datos (Post-Unión, Antes de dropna)")
if not merged_gdf.empty:
    st.write(f"Filas en merged_gdf ANTES de dropna: {len(merged_gdf)}")
    st.write("Primeras filas de merged_gdf (antes de dropna):")
    st.dataframe(merged_gdf.head())
    st.write(f"Valores nulos en 'poblacion' (antes de dropna): {merged_gdf['poblacion'].isnull().sum()}")
    st.write(f"Valores nulos en 'geometry' (antes de dropna): {merged_gdf['geometry'].isnull().sum()}")
    # Contar cuántos mun_code del GeoJSON encontraron una población
    matches = merged_gdf['poblacion'].notna().sum()
    st.write(f"Número de municipios del GeoJSON que encontraron datos de población: {matches}")

else:
    st.warning("La unión entre datos de población y GeoJSON resultó en un DataFrame vacío.")


merged_gdf.dropna(subset=['poblacion', 'geometry'], inplace=True) 
st.subheader("Diagnóstico de Datos (Post-Unión, Después de dropna)")
st.write(f"Filas en merged_gdf DESPUÉS de dropna: {len(merged_gdf)}")


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
