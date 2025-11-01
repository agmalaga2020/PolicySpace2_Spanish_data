"""
PolicySpace2 Dashboard - Aplicación Streamlit para explorar datos socioeconómicos de España

Este dashboard proporciona una interfaz interactiva para visualizar y analizar datos
del proyecto PolicySpace2 adaptado al contexto español. Permite explorar indicadores
demográficos, económicos y sociales a nivel municipal, provincial y autonómico.

Características principales:
- Visualización interactiva de datos
- Filtros dinámicos por múltiples dimensiones
- Exportación de datos en CSV y Excel
- Generación de informes personalizados
- Mapas interactivos geoespaciales

Autor: PolicySpace2 España
Fecha: 2025
Licencia: Ver LICENSE en el repositorio
"""

import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
import json
from io import BytesIO
import plotly.express as px
import logging

# Configuración
MAX_ROWS_DISPLAY = 100  # Número máximo de filas a mostrar en la exploración de datos

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Datos PolicySpace",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de la Base de Datos
DB_FILENAME = "datawarehouse.db"
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data base", DB_FILENAME)

@st.cache_resource
def get_engine():
    """
    Crea y cachea una conexión a la base de datos SQLite.
    
    Returns:
        sqlalchemy.engine.Engine: Motor de conexión a la base de datos o None si falla
        
    Note:
        Esta función utiliza @st.cache_resource para evitar crear múltiples conexiones
        a la base de datos en cada recarga de la aplicación.
    """
    if not os.path.exists(DB_PATH):
        error_msg = f"No se encontró la base de datos en: {DB_PATH}"
        logger.error(error_msg)
        st.error(f"❌ Error: {error_msg}")
        st.info("💡 Asegúrate de que el archivo datawarehouse.db existe en la carpeta 'data base'")
        return None
    try:
        engine = create_engine(f"sqlite:///{DB_PATH}")
        logger.info(f"Conexión establecida con la base de datos: {DB_PATH}")
        return engine
    except Exception as e:
        error_msg = f"Error al conectar con la base de datos: {str(e)}"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None

# Crear menú superior con pestañas
st.write("# PolicySpace2 Dashboard")
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Principal",
    "📊 Informes & Visualizaciones",
    "🔍 Explorar Datos",
    "ℹ️ Documentación"
])

# Contenido de la pestaña Documentación
with tab4:
    st.header("ℹ️ Documentación del Proyecto")
    
    doc_tab1, doc_tab2 = st.tabs(["📖 Visión General", "📑 Categorización de Datos"])
    
    # Pestaña Visión General
    with doc_tab1:
        st.subheader("🎯 Objetivo")
        st.markdown("""
        Adaptar el proyecto PolicySpace2 al mercado español, recopilando datos equivalentes 
        a los utilizados en el contexto brasileño original.
        """)
        
        # Fuentes de Datos
        st.subheader("📊 Fuentes de Datos")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### INE
            **Instituto Nacional de Estadística**
            
            Proporciona datos demográficos, económicos y sociales oficiales de España a través de su API JSON.
            
            [Acceder a la API](https://www.ine.es/dyngs/DAB/index.htm?cid=1099)
            """)
            
        with col2:
            st.markdown("""
            #### DataBank
            **Banco Mundial**
            
            Proporciona indicadores económicos y de desarrollo para España y otros países.
            
            [Acceder a DataBank](https://datos.bancomundial.org/)
            """)
            
        with col3:
            st.markdown("""
            #### Ministerio de Hacienda
            **Gobierno de España**
            
            Proporciona datos de financiación municipal y otros indicadores fiscales.
            
            [Ver datos](https://www.hacienda.gob.es/)
            """)
    
    # Pestaña Categorización de Datos
    with doc_tab2:
        st.subheader("Categorización de Datos")
        
        # Añadir contenido del archivo categorias_documentos.md
        with open("home/ubuntu/categorias_documentos.md", "r", encoding="utf-8") as f:
            contenido_md = f.read()
            st.markdown(contenido_md)

# Contenido de la pestaña Principal
with tab1:
    st.title("📊 Dashboard PolicySpace2 España")
    
    # Introducción
    st.markdown("""
    Este dashboard proporciona acceso interactivo a los datos socioeconómicos de España utilizados en el modelo PolicySpace2.
    Explora indicadores demográficos, económicos y sociales a nivel municipal, provincial y autonómico.
    """)
    
    # Crear 3 columnas para las tarjetas informativas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📈 Datos Disponibles
        - Población municipal
        - Índice de Desarrollo Humano
        - Estadísticas vitales
        - Datos económicos
        - Indicadores educativos
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 Funcionalidades
        - Visualización interactiva
        - Filtros dinámicos
        - Exportación de datos
        - Generación de informes
        - Mapas interactivos
        """)
    
    with col3:
        st.markdown("""
        ### 📊 Análisis
        - Comparativas municipales
        - Tendencias temporales
        - Correlaciones
        - Rankings y clasificaciones
        - Indicadores compuestos
        """)
    
    # Guía Rápida
    st.markdown("---")
    st.header("🚀 Guía Rápida")
    
    guide_col1, guide_col2 = st.columns(2)
    
    with guide_col1:
        st.info("""
        #### Para comenzar:
        1. Explora los informes predefinidos en la pestaña "📊 Informes"
        2. Visualiza datos geográficos en el "🗺️ Mapa Interactivo"
        3. Crea tus propios análisis en "🔍 Explorar Datos"
        """)
    
    with guide_col2:
        st.warning("""
        #### Consejos útiles:
        - Usa los filtros del sidebar para refinar las visualizaciones
        - Guarda tus análisis favoritos en "Informes Guardados"
        - Exporta los datos en formato CSV o Excel
        """)
    
    # Estadísticas del proyecto
    st.markdown("---")
    st.subheader("📈 Estadísticas del Proyecto")
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.metric(label="Municipios", value="8.131")
    with stats_col2:
        st.metric(label="Provincias", value="50")
    with stats_col3:
        st.metric(label="CC.AA.", value="17 + 2")
    with stats_col4:
        st.metric(label="Años de datos", value="2013-2022")

# Contenido de la pestaña Informes
with tab2:
    st.header("📊 Informes Disponibles")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Informes Demográficos")
        st.markdown("""
        - [👥 Población](./Informe_Poblacion_Nuevo)
        - [👶 Fecundidad](./Fecundidad_Envejecimiento)
        - [⚰️ Mortalidad](./Mortalidad_CCAA_Sexo)
        """)
        
        st.subheader("Desarrollo")
        st.markdown("""
        - [🏆 IDH Municipal](./Ranking_IDH_Municipios)
        - [🏢 Empresas](./Empresas_vs_IDH)
        """)

    with col2:
        st.subheader("Análisis Socioeconómico")
        st.markdown("""
        - [🏙️ Urbanización](./Urbanizacion_vs_Crecimiento)
        - [💶 Factores Económicos](./Interes_vs_Socioeconomico)
        - [🎓 Educación y Renta](./Nivel_Educativo_vs_Renta_IDH)
        """)
        
        st.subheader("Visualización")
        st.markdown("""
        - [🗺️ Mapa Interactivo](./Mapa_Interactivo)
        - [🗂️ Informes Guardados](./Informes_Guardados)
        """)

# Contenido de la pestaña Explorar Datos
with tab3:
    st.header("🔍 Explorar Base de Datos")
    
    engine = get_engine()
    if engine:
        st.success(f"Conectado a la base de datos: {DB_FILENAME}")
        
        @st.cache_data
        def get_table_names(_engine):
            """
            Obtiene la lista de nombres de tablas disponibles en la base de datos.
            
            Args:
                _engine: Motor de conexión SQLAlchemy (con _ para evitar hash en cache)
                
            Returns:
                list: Lista de nombres de tablas o lista vacía si hay error
            """
            try:
                with _engine.connect() as conn:
                    query = "SELECT name FROM sqlite_master WHERE type='table';"
                    tables = pd.read_sql_query(query, conn)['name'].tolist()
                    logger.info(f"Se encontraron {len(tables)} tablas en la base de datos")
                    return tables
            except Exception as e:
                error_msg = f"Error al obtener tablas: {str(e)}"
                logger.error(error_msg)
                st.error(f"❌ {error_msg}")
                return []

        # Selección de tabla en el sidebar
        table_names = get_table_names(engine)
        if table_names:
            selected_table = st.selectbox(
                "Selecciona una tabla para explorar:",
                table_names,
                index=None,
                placeholder="Elige una tabla..."
            )

            if selected_table:
                @st.cache_data
                def load_data(_engine, _table):
                    """
                    Carga datos de una tabla específica de la base de datos.
                    
                    Args:
                        _engine: Motor de conexión SQLAlchemy
                        _table: Nombre de la tabla a cargar
                        
                    Returns:
                        pd.DataFrame: DataFrame con los datos de la tabla
                    """
                    logger.info(f"Cargando datos de la tabla: {_table}")
                    return pd.read_sql_table(_table, _engine)

                try:
                    df = load_data(engine, selected_table)
                    st.write(f"### Tabla: {selected_table}")
                    st.info(f"📊 Mostrando las primeras {MAX_ROWS_DISPLAY} filas de {len(df):,} registros totales")
                    st.dataframe(df.head(MAX_ROWS_DISPLAY), use_container_width=True)

                    # Filtros en el sidebar
                    with st.sidebar:
                        st.header("⚙️ Filtros")
                        filters = {}
                        for col in df.columns:
                            if df[col].nunique() < 50:  # Solo mostrar filtro para columnas con pocos valores únicos
                                values = df[col].unique()
                                selected = st.multiselect(f"Filtrar por {col}:", values)
                                if selected:
                                    filters[col] = selected

                        # Aplicar filtros
                        df_filtered = df.copy()
                        for col, values in filters.items():
                            df_filtered = df_filtered[df_filtered[col].isin(values)]

                        # Visualización
                        st.header("📈 Visualización")
                        numeric_cols = df.select_dtypes(include=[np.number]).columns
                        
                        if len(numeric_cols) > 0:
                            x_col = st.selectbox("Eje X:", df.columns)
                            y_col = st.selectbox("Eje Y:", numeric_cols)
                            plot_type = st.selectbox("Tipo de gráfico:", ["Líneas", "Barras", "Dispersión"])
                            
                            if x_col and y_col:
                                if plot_type == "Líneas":
                                    fig = px.line(df_filtered, x=x_col, y=y_col)
                                elif plot_type == "Barras":
                                    fig = px.bar(df_filtered, x=x_col, y=y_col)
                                else:
                                    fig = px.scatter(df_filtered, x=x_col, y=y_col)
                                st.plotly_chart(fig, use_container_width=True)

                except Exception as e:
                    st.error(f"Error al cargar los datos: {e}")
        else:
            st.warning("No se encontraron tablas en la base de datos.")
    else:
        st.error("No se pudo establecer la conexión con la base de datos.")

# Información adicional en el sidebar
st.sidebar.markdown("---")
st.sidebar.info("🚧 Dashboard en desarrollo. Más funcionalidades próximamente.")
