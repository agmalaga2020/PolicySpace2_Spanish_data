import streamlit as st
import streamlit as st
import streamlit as st
import pandas as pd
import numpy as np # Importar numpy
from sqlalchemy import create_engine
import os
import json # Para guardar/cargar configuraciones
from io import BytesIO # Para descarga Excel
import plotly.express as px # Importar plotly aquí

# --- Cargar CSS Personalizado ---
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Archivo CSS '{file_name}' no encontrado. Se usarán estilos por defecto.")

# Configuración de la página (opcional, pero útil)
st.set_page_config(
    page_title="Dashboard de Datos PolicySpace",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar CSS
local_css("assets/style.css")

# Título principal del dashboard
st.title("📊 Dashboard Interactivo de Datos")
st.markdown("Explora y visualiza los datos cargados desde el Data Warehouse.")

# --- Conexión a la Base de Datos ---
DB_FILENAME = "datawarehouse.db"
# La ruta a la DB es relativa a la carpeta raíz del proyecto, no a la carpeta dashboard
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data base", DB_FILENAME)

@st.cache_resource # Cachear el recurso para no reconectar en cada interacción
def get_engine():
    """Crea y retorna una conexión (engine) a la base de datos SQLite."""
    if not os.path.exists(DB_PATH):
        st.error(f"Error: No se encontró el archivo de la base de datos en la ruta esperada: {DB_PATH}")
        st.error("Asegúrate de que el ETL se haya ejecutado y la base de datos exista en 'data base/datawarehouse.db'")
        return None
    try:
        engine = create_engine(f"sqlite:///{DB_PATH}")
        return engine
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return None

engine = get_engine()

if engine:
    st.success(f"Conectado a la base de datos: {DB_FILENAME}")
    
    @st.cache_data # Cachear los datos para no recargar en cada interacción (si no cambian)
    def get_table_names(_engine):
        """Obtiene los nombres de todas las tablas en la base de datos."""
        try:
            with _engine.connect() as connection:
                return pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", connection)['name'].tolist()
        except Exception as e:
            st.error(f"Error al obtener nombres de tablas: {e}")
            return []

    table_names = get_table_names(engine)

    if not table_names:
        st.warning("No se encontraron tablas en la base de datos.")
    else:
        # --- Selección de Tabla ---
        st.sidebar.header("Selección de Tabla")
        selected_table = st.sidebar.selectbox(
            "Elige una tabla para explorar:", 
            table_names, 
            index=None, 
            placeholder="Selecciona una tabla...",
            help="Selecciona la tabla de la base de datos que deseas visualizar y analizar."
        )

        if selected_table:
            st.header(f"🔎 Explorando Tabla: `{selected_table}`")

            @st.cache_data
            def load_data(_engine, table_name):
                """Carga los datos de la tabla seleccionada."""
                try:
                    # Cuidado con tablas muy grandes, podríamos limitar la carga inicial o usar paginación
                    df = pd.read_sql_table(table_name, _engine)
                    return df
                except Exception as e:
                    st.error(f"Error al cargar la tabla '{table_name}': {e}")
                    return pd.DataFrame()

            df = load_data(engine, selected_table)

            if not df.empty:
                st.info(f"Mostrando las primeras 100 filas de {df.shape[0]} totales.")
                st.dataframe(df.head(100))

                # --- Descarga de Datos ---
                st.subheader("📥 Descargar Datos")
                
                # Convertir DataFrame a CSV
                @st.cache_data
                def convert_df_to_csv(df_to_convert):
                    return df_to_convert.to_csv(index=False).encode('utf-8')

                csv_data = convert_df_to_csv(df)
                st.download_button(
                    label="Descargar como CSV",
                    data=csv_data,
                    file_name=f"{selected_table}.csv",
                    mime="text/csv",
                )

                # Convertir DataFrame a Excel (requiere openpyxl)
                from io import BytesIO
                @st.cache_data
                def convert_df_to_excel(df_to_convert):
                    output = BytesIO()
                    # Usar BytesIO como buffer para el archivo Excel
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_to_convert.to_excel(writer, index=False, sheet_name='Datos')
                    # No es necesario llamar a save(), el context manager lo hace
                    processed_data = output.getvalue()
                    return processed_data
                
                excel_data = convert_df_to_excel(df)
                st.download_button(
                    label="Descargar como Excel",
                    data=excel_data,
                    file_name=f"{selected_table}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                # --- Filtros Dinámicos ---
                st.sidebar.header("⚙️ Filtros")
                df_filtered = df.copy() # Empezar con el DF completo

                # Identificar columnas comunes para filtrar
                filter_columns = {
                    'year': 'Año',
                    'mun_code': 'Código Municipio',
                    'cpro': 'Código Provincia',
                    'ccaa_code': 'Código CCAA',
                    'sex': 'Sexo',
                    'CNAE': 'CNAE (Act. Principal)' 
                    # Añadir más columnas si es necesario
                }

                active_filters = {}

                for col_code, col_name in filter_columns.items():
                    if col_code in df_filtered.columns:
                        # Tratar valores NaN antes de obtener únicos y ordenar
                        unique_values = df_filtered[col_code].dropna().unique()
                        try:
                            # Intentar ordenar numéricamente si es posible, si no, alfabéticamente
                            unique_values_sorted = sorted(unique_values, key=lambda x: float(x) if str(x).replace('.','',1).isdigit() else str(x))
                        except:
                             unique_values_sorted = sorted(map(str, unique_values))

                        if len(unique_values_sorted) > 1: # Solo mostrar filtro si hay más de una opción
                             # Usar multiselect para la mayoría de casos
                             selected_values = st.sidebar.multiselect(
                                 f"{col_name}:", 
                                 unique_values_sorted, 
                                 default=[], 
                                 help=f"Selecciona uno o más valores para filtrar la tabla por la columna '{col_name}'."
                              )
                             if selected_values:
                                 # Asegurarse de que los tipos coincidan para el filtro
                                 if pd.api.types.is_numeric_dtype(df_filtered[col_code].dropna()):
                                     try:
                                         selected_values_typed = [type(unique_values[0])(v) for v in selected_values]
                                         df_filtered = df_filtered[df_filtered[col_code].isin(selected_values_typed)]
                                         active_filters[col_name] = selected_values_typed
                                     except: # Fallback a string si la conversión falla
                                         df_filtered = df_filtered[df_filtered[col_code].astype(str).isin(selected_values)]
                                         active_filters[col_name] = selected_values
                                 else:
                                     df_filtered = df_filtered[df_filtered[col_code].astype(str).isin(selected_values)]
                                     active_filters[col_name] = selected_values


                st.subheader("📊 Datos Filtrados")
                if active_filters:
                    st.write("Filtros aplicados:")
                    st.json(active_filters) # Mostrar filtros activos
                else:
                    st.write("No hay filtros activos. Mostrando datos originales.")
                
                st.info(f"Mostrando las primeras 100 filas de {df_filtered.shape[0]} totales (después de filtros).")
                st.dataframe(df_filtered.head(100))
                
                # Actualizar datos para descarga con los filtros aplicados
                csv_data_filtered = convert_df_to_csv(df_filtered)
                st.download_button(
                    label="Descargar Filtrado como CSV",
                    data=csv_data_filtered,
                    file_name=f"{selected_table}_filtrado.csv",
                    mime="text/csv",
                    key='csv_filtered' # Key diferente para evitar conflicto con el botón anterior
                )
                excel_data_filtered = convert_df_to_excel(df_filtered)
                st.download_button(
                    label="Descargar Filtrado como Excel",
                    data=excel_data_filtered,
                    file_name=f"{selected_table}_filtrado.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key='excel_filtered' # Key diferente
                )

                # --- Visualizaciones Básicas con Plotly ---
                st.sidebar.header("📈 Visualización")
                # Usar df_filtered para las visualizaciones
                numeric_cols = df_filtered.select_dtypes(include=np.number).columns.tolist() # Usar np.number
                non_numeric_cols = df_filtered.select_dtypes(exclude=np.number).columns.tolist() # Usar np.number

                if not df_filtered.empty and (numeric_cols or non_numeric_cols):
                    st.subheader("📈 Gráficos Interactivos")
                    
                    # Opciones de ejes (permitir categóricos y numéricos)
                    all_cols = numeric_cols + non_numeric_cols
                    x_axis = st.sidebar.selectbox("Eje X:", all_cols, index=None, placeholder="Selecciona eje X...", help="Columna para el eje horizontal del gráfico.")
                    y_axis = st.sidebar.selectbox("Eje Y:", numeric_cols, index=None, placeholder="Selecciona eje Y (numérico)...", help="Columna numérica para el eje vertical.") # Y suele ser numérico
                    
                    chart_type = st.sidebar.selectbox(
                        "Tipo de Gráfico:", 
                        ["Dispersión (Scatter)", "Líneas", "Barras"], 
                        index=None, 
                        placeholder="Selecciona tipo...",
                        help="Elige el tipo de gráfico para visualizar los datos seleccionados."
                    )

                    if x_axis and y_axis and chart_type:
                        import plotly.express as px
                        
                        try:
                            title = f"{y_axis} vs {x_axis} ({chart_type})"
                            if chart_type == "Dispersión (Scatter)":
                                fig = px.scatter(df_filtered, x=x_axis, y=y_axis, title=title, 
                                                 hover_data=df_filtered.columns) # Mostrar más info al pasar el ratón
                            elif chart_type == "Líneas":
                                # Para líneas, a menudo se ordena por el eje X si es temporal o secuencial
                                df_plot = df_filtered.sort_values(by=x_axis) if x_axis in df_filtered.columns else df_filtered
                                fig = px.line(df_plot, x=x_axis, y=y_axis, title=title)
                            elif chart_type == "Barras":
                                fig = px.bar(df_filtered, x=x_axis, y=y_axis, title=title)
                            
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error al generar el gráfico: {e}")
                    elif x_axis or y_axis or chart_type:
                         st.warning("Por favor, selecciona Eje X, Eje Y (numérico) y Tipo de Gráfico para visualizar.")

                else:
                    st.sidebar.warning("No hay columnas adecuadas o datos filtrados para visualizar.")

            else:
                st.warning(f"La tabla `{selected_table}` está vacía o no se pudo cargar.")
else:
    st.error("No se pudo establecer la conexión con la base de datos. Verifica la configuración y el archivo.")

# --- Guardar Configuración de Informe ---
st.sidebar.header("💾 Guardar Informe")
report_name = st.sidebar.text_input(
    "Nombre para este informe:", 
    placeholder="Ej: Población Madrid 2020", 
    help="Introduce un nombre descriptivo para guardar la configuración actual (tabla, filtros, gráfico)."
)
save_button = st.sidebar.button(
    "Guardar Configuración Actual", 
    help="Guarda la tabla seleccionada, los filtros aplicados y la configuración del gráfico actual como un informe reutilizable."
)

REPORTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_reports.json")

def load_saved_reports():
    """Carga los informes guardados desde el archivo JSON."""
    if os.path.exists(REPORTS_FILE):
        try:
            with open(REPORTS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {} # Archivo corrupto o vacío
    return {}

def save_report_config(name, config):
    """Guarda una nueva configuración de informe en el archivo JSON."""
    reports = load_saved_reports()
    reports[name] = config
    try:
        with open(REPORTS_FILE, 'w') as f:
            json.dump(reports, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error al guardar el informe: {e}")
        return False

if save_button and report_name and selected_table:
    # Recopilar configuración actual
    current_config = {
        "table": selected_table,
        "filters": active_filters, # Ya contiene los filtros aplicados
        "chart_config": {
            "x_axis": x_axis if 'x_axis' in locals() else None,
            "y_axis": y_axis if 'y_axis' in locals() else None,
            "chart_type": chart_type if 'chart_type' in locals() else None
        }
    }
    if save_report_config(report_name, current_config):
        st.sidebar.success(f"Informe '{report_name}' guardado!")
    else:
        st.sidebar.error("No se pudo guardar el informe.")
elif save_button:
    st.sidebar.warning("Por favor, introduce un nombre para el informe y selecciona una tabla.")


st.sidebar.info("Dashboard en desarrollo. Más funcionalidades próximamente.")
