import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import plotly.express as px

st.set_page_config(page_title="Mortalidad por CCAA y Sexo", page_icon="⚰️")

st.title("⚰️ Mortalidad por Comunidad Autónoma y Sexo")
st.markdown(
    """
    Este informe visualiza la evolución de la mortalidad por comunidad autónoma, sexo y grupo de edad.
    Puedes comparar tendencias y diferencias entre regiones y sexos a lo largo del tiempo.
    """
)

DB_FILENAME = "datawarehouse.db"
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data base", DB_FILENAME)

@st.cache_resource
def get_engine():
    if not os.path.exists(DB_PATH):
        st.error(f"Error: No se encontró el archivo de la base de datos: {DB_PATH}")
        return None
    try:
        engine = create_engine(f"sqlite:///{DB_PATH}")
        return engine
    except Exception as e:
        st.error(f"Error al conectar: {e}")
        return None

engine = get_engine()

def load_mortalidad_data(_engine):
    if not _engine:
        return pd.DataFrame()
    try:
        df_mort = pd.read_sql_table('df_mortalidad_ccaa_sexo', _engine)
        st.subheader("Vista previa de datos de mortalidad")
        st.dataframe(df_mort.head())
        return df_mort
    except Exception as e:
        st.error(f"Error crítico al cargar datos de mortalidad: {e}")
        return pd.DataFrame()

if engine:
    df_mort = load_mortalidad_data(engine)

    if not df_mort.empty:
        st.header("Evolución de la mortalidad por CCAA y sexo")
        ccaa = sorted(df_mort['ccaa_name'].dropna().unique())
        selected_ccaa = st.selectbox("Selecciona una comunidad autónoma:", ccaa)
        sexos = sorted(df_mort['sex'].dropna().unique())
        selected_sexo = st.selectbox("Selecciona sexo:", sexos)
        edades = sorted(df_mort['Edad'].dropna().unique())
        selected_edades = st.multiselect("Selecciona grupo(s) de edad:", edades, default=edades)

        df_filtered = df_mort[
            (df_mort['ccaa_name'] == selected_ccaa) &
            (df_mort['sex'] == selected_sexo) &
            (df_mort['Edad'].isin(selected_edades))
        ].copy() # Usar .copy() para evitar SettingWithCopyWarning al modificar df_filtered

        if not df_filtered.empty:
            # Asegurar que 'year' y 'Edad' son numéricos para una correcta ordenación y graficación
            # Si 'Edad' es un rango o texto, se necesitaría un preprocesamiento más complejo para ordenarlo lógicamente.
            # Por ahora, intentaremos convertir a numérico. Si falla, se tratará como categoría.
            try:
                df_filtered['year'] = pd.to_numeric(df_filtered['year'])
                df_filtered['Edad'] = pd.to_numeric(df_filtered['Edad']) # Asumiendo que 'Edad' puede ser numérico
                # Ordenar los datos para que las líneas se dibujen correctamente
                df_filtered = df_filtered.sort_values(by=['Edad', 'year'])
            except ValueError:
                st.warning("No se pudo convertir 'Edad' a numérico. Se tratará como categoría. El orden en la leyenda podría no ser el esperado.")
                # Si 'Edad' no es numérico, ordenar solo por año, y Plotly tratará 'Edad' como categórico.
                # Para un orden específico de categorías de edad, se necesitaría pd.CategoricalDtype.
                df_filtered = df_filtered.sort_values(by=['year'])


            fig = px.line(
                df_filtered,
                x='year',
                y='total_muertes',
                color='Edad', # Plotly tratará 'Edad' como categórica si no es numérica o si tiene muchos valores discretos
                category_orders={"Edad": sorted(df_filtered['Edad'].unique())}, # Asegura un orden consistente en la leyenda si 'Edad' es tratada como categoría
                labels={'total_muertes': 'Total Muertes (Absoluto)', 'year': 'Año', 'Edad': 'Grupo de Edad'},
                title=f"Evolución de la mortalidad en {selected_ccaa} ({selected_sexo})"
            )
            fig.update_layout(legend_title_text='Grupo de Edad')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
            **Nota sobre los datos:** "Total Muertes" representa el número absoluto de defunciones registradas para cada grupo.
            No es una tasa de mortalidad, por lo que los grupos de edad con mayor población pueden mostrar un mayor número de muertes.
            """)

            st.header("Datos detallados (filtrados)")
            st.dataframe(df_filtered)
        else:
            st.warning("No hay datos para la selección actual.")
    else:
        st.warning("No se pudieron cargar los datos de mortalidad.")
else:
    st.error("No se pudo conectar a la base de datos.")
