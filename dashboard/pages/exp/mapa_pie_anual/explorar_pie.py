import sqlite3
import pandas as pd
import argparse
import os

# --- Argumentos de línea de comandos ---
parser = argparse.ArgumentParser(description="Extrae y procesa datos PIE para un año específico.")
parser.add_argument("year", type=int, help="Año para el cual procesar los datos PIE.")
args = parser.parse_args()
selected_year = args.year

# --- Configuración de Rutas ---
# db_path es relativo al CWD (raíz del proyecto) desde donde se llama este script.
db_path = 'data base/datawarehouse.db'
# El output_csv_path será en el mismo directorio que este script.
output_csv_path = f'datos_pie_mapa_{selected_year}.csv'

# Conectarse a la base de datos
conn = sqlite3.connect(db_path)

# Cargar la tabla PIE en un DataFrame de pandas
try:
    df_pie = pd.read_sql_query("SELECT * FROM PIE", conn)
    print("Primeras 5 filas de la tabla PIE:")
    print(df_pie.head())
    print("\nInformación general de la tabla PIE:")
    print(df_pie.info())
    print("\nEstadísticas descriptivas de la tabla PIE:")
    print(df_pie.describe(include='all'))

    if 'year' not in df_pie.columns:
        print("\nLa columna 'year' no se encuentra en la tabla PIE.")
        conn.close()
        exit()

    available_years = sorted(df_pie['year'].unique())
    print(f"\nAños disponibles en la tabla PIE: {available_years}")

    if selected_year not in available_years:
        print(f"\nEl año {selected_year} no tiene datos en la tabla PIE. Años disponibles: {available_years}")
        conn.close()
        exit()
        
    print(f"\nProcesando datos de PIE para el año: {selected_year}")
    df_pie_year = df_pie[df_pie['year'] == selected_year].copy() # Usar .copy() para evitar SettingWithCopyWarning
    
    if df_pie_year.empty:
        print(f"No se encontraron datos para el año {selected_year}.")
        conn.close()
        exit()

    print(df_pie_year.head())
    print(f"\nNúmero de municipios con datos de PIE para {selected_year}: {len(df_pie_year)}")
    
    target_column = 'total_participacion_variables'
    if target_column not in df_pie_year.columns:
        print(f"La columna '{target_column}' no existe en los datos filtrados para {selected_year}.")
        conn.close()
        exit()

    print(f"\nEstadísticas de '{target_column}' para {selected_year}:")
    print(df_pie_year[target_column].describe())
    
    non_null_imports = df_pie_year[target_column].notna().sum()
    print(f"Número de municipios con '{target_column}' no nulo para {selected_year}: {non_null_imports}")

    if non_null_imports > 0:
        print(f"Preparando datos para el mapa del año {selected_year}...")
        
        # Crear mun_code_ine de 5 dígitos
        df_pie_year.loc[:, 'codigo_provincia_str'] = df_pie_year['codigo_provincia'].astype('Int64').astype(str).str.zfill(2)
        df_pie_year.loc[:, 'mun_code_temp'] = df_pie_year['mun_code'].astype(str).str.split('.').str[0]
        df_pie_year.loc[:, 'mun_code_str'] = df_pie_year['mun_code_temp'].astype(str).str.zfill(3)
        df_pie_year.loc[:, 'mun_code_ine'] = df_pie_year['codigo_provincia_str'] + df_pie_year['mun_code_str']
        
        print("\nEjemplo de mun_code_ine generados:")
        print(df_pie_year[['codigo_provincia', 'mun_code', 'mun_code_ine']].head())

        map_data = df_pie_year[['mun_code_ine', target_column]].copy()
        map_data.rename(columns={target_column: 'valor_mapa', 'mun_code_ine': 'mun_code'}, inplace=True)
        
        map_data.to_csv(output_csv_path, index=False)
        print(f"Datos para el mapa del año {selected_year} guardados en: {output_csv_path}")
    else:
        print(f"No hay valores '{target_column}' para el año {selected_year}, no se generará archivo CSV para el mapa.")

except pd.io.sql.DatabaseError as e:
    print(f"Error al leer la tabla PIE: {e}")
    print("Verificando si la tabla existe...")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='PIE';")
    table_exists = cursor.fetchone()
    if table_exists:
        print("La tabla 'PIE' existe.")
        cursor.execute("PRAGMA table_info(PIE);")
        columns = cursor.fetchall()
        print("Columnas en la tabla 'PIE':")
        for col in columns:
            print(col)
    else:
        print("La tabla 'PIE' NO existe en la base de datos.")
        print("Tablas disponibles:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(table[0])


# Cerrar la conexión
conn.close()
