import pandas as pd
import geopandas as gpd
import folium
import numpy as np # Para np.log10
import branca.colormap as branca_cm # Importar branca.colormap
import argparse
import os

# --- Argumentos de línea de comandos ---
parser = argparse.ArgumentParser(description="Genera un mapa HTML de PIE para un año específico.")
parser.add_argument("year", type=int, help="Año para el cual generar el mapa.")
args = parser.parse_args()
selected_year = args.year

# --- Configuración de Rutas ---
# datos_pie_path y output_map_path son relativos a la ubicación de este script.
# geojson_path es relativo al CWD (raíz del proyecto) desde donde se llama este script.
datos_pie_path = f'datos_pie_mapa_{selected_year}.csv'
geojson_path = 'ETL/GeoRef_Spain/georef-spain-municipio.geojson' 
output_map_path = f'mapa_pie_municipios_{selected_year}.html'

map_tiles = 'CartoDB positron'
map_location = [40.416775, -3.703790] # Centro de España
map_zoom_start = 6

# --- Cargar Datos ---
print(f"Cargando datos de PIE para el año {selected_year} desde: {datos_pie_path}")
df_pie = pd.read_csv(datos_pie_path)

print(f"Cargando datos GeoJSON desde: {geojson_path}")
gdf_municipios = gpd.read_file(geojson_path)

# --- Preprocesamiento y Unión ---
# Asegurar que los códigos de municipio sean del mismo tipo (string) para la unión
df_pie['mun_code'] = df_pie['mun_code'].astype(str)
# La columna 'mun_code' ya existe en el GeoJSON y parece estar en el formato correcto.
# Solo necesitamos asegurarnos de que sea de tipo string.
gdf_municipios['mun_code'] = gdf_municipios['mun_code'].astype(str)


# Verificar algunos códigos para asegurar la correspondencia
print("\nEjemplo de mun_code en df_pie:", df_pie['mun_code'].head().tolist())
print("Ejemplo de mun_code en gdf_municipios (original):", gdf_municipios['mun_code'].head().tolist())

# Unir los datos de PIE con el GeoDataFrame
print("\nRealizando la unión de los datos...")
# Usaremos la columna 'mun_code' que ya existe en gdf_municipios y la que creamos en df_pie
merged_gdf = gdf_municipios.merge(df_pie, on='mun_code', how='left')

# Verificar cuántos municipios se unieron correctamente
print(f"Municipios en GeoDataFrame original: {len(gdf_municipios)}")
print(f"Municipios en datos PIE: {len(df_pie)}")
print(f"Municipios en GeoDataFrame unido: {len(merged_gdf)}")
print(f"Municipios unidos con datos de PIE (valor_mapa no nulo): {merged_gdf['valor_mapa'].notna().sum()}")

# Manejar valores faltantes o infinitos si los hubiera (aunque ya se filtraron en el script anterior)
merged_gdf['valor_mapa'].fillna(0, inplace=True) # Rellenar NaNs con 0 para el mapa, o decidir otra estrategia

# Aplicar transformación logarítmica si el rango de datos es muy amplio
# Esto ayuda a una mejor visualización en el mapa coroplético
# Se suma 1 para evitar log(0) si hay valores de 0
if merged_gdf['valor_mapa'].min() >= 0 and merged_gdf['valor_mapa'].max() > 0 :
    merged_gdf['valor_mapa_log'] = np.log10(merged_gdf['valor_mapa'] + 1)
    choropleth_column = 'valor_mapa_log'
    legend_name = f'Log10 (Total Participación Variables PIE {selected_year} + 1)'
    print("\nSe aplicó transformación logarítmica a 'valor_mapa'.")
else:
    choropleth_column = 'valor_mapa'
    legend_name = f'Total Participación Variables PIE {selected_year}'
    print("\nNo se aplicó transformación logarítmica.")


# --- Crear Mapa ---
print(f"\nCreando mapa Folium...")
m = folium.Map(location=map_location, zoom_start=map_zoom_start, tiles=map_tiles)

# Añadir capa coroplética
if merged_gdf[choropleth_column].notna().sum() > 0:
    # Preparar datos para el tooltip/popup
    # Asegurarse de que 'mun_name' y 'valor_mapa' (original) estén en merged_gdf
    # 'mun_name' viene del GeoJSON, 'valor_mapa' de los datos PIE (antes de log)
    
    # Crear un GeoJson layer para tener más control sobre tooltips/popups
    # Esto reemplaza el folium.Choropleth simple para permitir tooltips personalizados
    
    # Redondear valor_mapa para el tooltip
    merged_gdf['valor_mapa_display'] = merged_gdf['valor_mapa'].round(2)

    geojson_layer = folium.GeoJson(
        merged_gdf,
        name=f'Participación Ingresos del Estado (PIE) {selected_year}',
        style_function=lambda feature: {
            'fillColor': branca_cm.linear.YlGnBu_09.scale(
                merged_gdf[choropleth_column].min(),
                merged_gdf[choropleth_column].max()
            )(feature['properties'][choropleth_column]) if pd.notna(feature['properties'][choropleth_column]) else 'lightgray',
            'color': 'black', # Color del borde
            'weight': 0.5, # Grosor del borde
            'fillOpacity': 0.7,
        },
        highlight_function=lambda x: {'weight':2, 'fillOpacity':0.8},
        tooltip=folium.features.GeoJsonTooltip(
            fields=['mun_name', 'valor_mapa_display', 'mun_code'],
            aliases=['Municipio:', 'PIE (Valor Original):', 'Cód. Municipio:'],
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
        popup=folium.features.GeoJsonPopup(
            fields=['mun_name', 'valor_mapa_display', choropleth_column, 'mun_code', 'prov_name', 'acom_name'],
            aliases=['Municipio:', 'PIE (Valor Original):', f'{legend_name}:', 'Cód. Municipio:', 'Provincia:', 'CCAA:'],
            localize=True,
            labels=True,
            style="width:300px;"
        )
    )
    
    # Añadir la leyenda manualmente ya que Choropleth no se usa directamente
    colormap = branca_cm.linear.YlGnBu_09.scale(
        merged_gdf[choropleth_column].min(),
        merged_gdf[choropleth_column].max()
    )
    colormap.caption = legend_name
    m.add_child(colormap)
    
    geojson_layer.add_to(m)
    print("Capa GeoJson con tooltips/popups añadida.")
else:
    print("No hay datos válidos en la columna para el coroplético después de la unión.")

# Añadir control de capas
folium.LayerControl().add_to(m)

# --- Guardar Mapa ---
m.save(output_map_path)
print(f"\nMapa guardado en: {output_map_path}")
print("Proceso completado.")
