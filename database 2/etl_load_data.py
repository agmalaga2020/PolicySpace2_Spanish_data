import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

# Configuración de paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Esto apuntará a 'database 2'
DB_PATH = os.path.join(BASE_DIR, "datawarehouse_v2.db") # Nueva base de datos
LOG_PATH = os.path.join(BASE_DIR, "etl_load_log_v2.txt") # Nuevo log

def log(msg):
    print(msg)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")

# Limpiar log anterior
if os.path.exists(LOG_PATH):
    os.remove(LOG_PATH)
with open(LOG_PATH, "w", encoding="utf-8") as f:
    f.write(f"LOG ETL LOAD DATA V2 - {datetime.now()}\n\n")

# Crear motor de base de datos (SQLite)
engine = create_engine(f"sqlite:///{DB_PATH}")

# --- Helper function to filter by year range ---
def filter_by_year_range(df, year_column='year', start_year=2014, end_year=2020):
    """Filtra un DataFrame para incluir solo los años dentro del rango especificado."""
    if year_column in df.columns:
        # Asegurarse de que la columna de año sea numérica para la comparación
        df[year_column] = pd.to_numeric(df[year_column], errors='coerce')
        df_filtered = df[(df[year_column] >= start_year) & (df[year_column] <= end_year)].copy()
        log(f"Filtrado por años: {start_year}-{end_year}. Filas antes: {len(df)}, Filas después: {len(df_filtered)}")
        return df_filtered
    else:
        log(f"ADVERTENCIA: La columna '{year_column}' no se encontró en el DataFrame. No se aplicó filtro de año.")
        return df

# --- Helper function for household size imputation ---
def impute_household_size(df_hogares_raw, years_to_impute):
    """
    Imputa el tamaño medio de los hogares para los años especificados utilizando regresión lineal
    por comunidad autónoma.
    """
    log("Iniciando imputación de tamaño medio de hogares...")
    df_hogares_raw['year'] = pd.to_numeric(df_hogares_raw['year'])
    df_hogares_raw['tamano_medio_hogar'] = pd.to_numeric(df_hogares_raw['tamano_medio_hogar'])
    
    all_imputed_data = []
    
    for ccaa_code in df_hogares_raw['ccaa_code'].unique():
        df_ccaa = df_hogares_raw[df_hogares_raw['ccaa_code'] == ccaa_code].sort_values(by='year')
        
        if df_ccaa.empty or len(df_ccaa) < 2: # Necesitamos al menos 2 puntos para la regresión
            log(f"  CCAA {ccaa_code}: No hay suficientes datos para imputar ({len(df_ccaa)} puntos). Saltando.")
            continue
            
        X = df_ccaa[['year']]
        y = df_ccaa['tamano_medio_hogar']
        
        model = LinearRegression()
        model.fit(X, y)
        
        imputed_values = model.predict(pd.DataFrame(years_to_impute, columns=['year']))
        
        df_imputed_ccaa = pd.DataFrame({
            'ccaa_code': ccaa_code,
            'year': years_to_impute,
            'tamano_medio_hogar': imputed_values,
            'imputed': 1 # Marcar como imputado
        })
        all_imputed_data.append(df_imputed_ccaa)
        log(f"  CCAA {ccaa_code}: Imputación completada para {len(years_to_impute)} años.")

    if not all_imputed_data:
        log("No se generaron datos imputados. Verifique los datos de entrada.")
        return pd.DataFrame()

    df_imputed_total = pd.concat(all_imputed_data, ignore_index=True)
    
    # Combinar con datos originales no imputados (los que ya están en el rango START_YEAR-END_YEAR)
    df_original_in_range = df_hogares_raw[df_hogares_raw['year'].isin(years_to_impute)].copy()
    df_original_in_range['imputed'] = 0
    
    # Priorizar datos originales si existen para los años a imputar
    df_final = pd.concat([df_original_in_range, df_imputed_total]).drop_duplicates(subset=['ccaa_code', 'year'], keep='first')
    
    log(f"Imputación completada. Total de filas generadas/mantenidas para años {min(years_to_impute)}-{max(years_to_impute)}: {len(df_final)}")
    return df_final

try:
    # --- Constantes para el rango de años ---
    START_YEAR = 2014
    END_YEAR = 2020

    # 1. Tabla de equivalencias (municipios)
    # Esta tabla no tiene dimensión temporal directa en su forma actual, se usa para mapeos.
    df_eq_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/tabla_equivalencias/data/df_equivalencias_municipio_CORRECTO.csv')
    df_eq = pd.read_csv(df_eq_path, dtype=str)
    # Normalizar CODAUTO para que tenga dos dígitos con cero a la izquierda si es necesario
    df_eq['CODAUTO'] = df_eq['CODAUTO'].astype(str).str.zfill(2)
    # Asegurar que CPRO también tenga dos dígitos (ya debería estar así por el dtype=str, pero por si acaso)
    df_eq['CPRO'] = df_eq['CPRO'].astype(str).str.zfill(2)
    df_eq.to_sql('tabla_equivalencias', engine, if_exists='replace', index=False)
    log(f"[tabla_equivalencias] OK: {df_eq.shape[0]} filas, {df_eq.shape[1]} columnas. Path: {df_eq_path}")
    log(f"Ejemplo CODAUTO normalizado en df_eq: {df_eq['CODAUTO'].unique()[:5]}")
    
    # Cargar códigos de provincias (para el merge de fecundidad)
    df_prov_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/indicadores_fecundidad_municipio_provincias/codigos_ccaa_provincias.csv')
    df_prov = pd.read_csv(df_prov_path, dtype=str)
    # Renombrar columna de provincia para el merge
    df_prov = df_prov.rename(columns={'Provincia': 'provincia_name'})
    log(f"\n[codigos_ccaa_provincias] Cargado: {df_prov.shape[0]} filas, {df_prov.shape[1]} columnas. Path: {df_prov_path}")
    log(f"Columnas: {', '.join(df_prov.columns)}")
    log(df_prov.head().to_string())

    # 2. Cifras población municipio
    df_cif_pob_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/cifras_poblacion_municipio/cifras_poblacion_municipio.csv')
    df_cif_pob = pd.read_csv(df_cif_pob_path, dtype={'mun_code': str})
    # Esta tabla ya tiene una columna 'year', aplicar filtro
    df_cif_pob = filter_by_year_range(df_cif_pob, year_column='year', start_year=START_YEAR, end_year=END_YEAR)
    df_cif_pob.to_sql('cifras_poblacion_municipio', engine, if_exists='replace', index=False)
    log(f"\n[cifras_poblacion_municipio] OK: {df_cif_pob.shape[0]} filas, {df_cif_pob.shape[1]} columnas. Path: {df_cif_pob_path}")

    # 3. Mortalidad CCAA por sexo
    df_mort_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/df_mortalidad_ccaa_sexo/df_mortalidad_final.csv')
    df_mort = pd.read_csv(df_mort_path, dtype={'ccaa_code': str})
    df_mort = df_mort.rename(
        columns={
            'ccaa_code': 'ccaa_code', # Mantener por si se usa para mapear a CCAA
            'Sexo': 'sex',
            'Periodo': 'year',
            'Total': 'total_muertes'
        }
    )
    df_mort = filter_by_year_range(df_mort, year_column='year', start_year=START_YEAR, end_year=END_YEAR)
    # Mapear mortalidad a municipios
    df_mortalidad_municipio = pd.merge(df_mort, df_eq[['mun_code', 'NOMBRE', 'CODAUTO']], left_on='ccaa_code', right_on='CODAUTO', how='left')
    if df_mortalidad_municipio['mun_code'].isna().any():
        log(f"ADVERTENCIA en mortalidad_municipio: {df_mortalidad_municipio['mun_code'].isna().sum()} filas no pudieron mapear mun_code.")
    df_mortalidad_municipio = df_mortalidad_municipio.drop(columns=['CODAUTO']) # Eliminar columna redundante del merge
    df_mortalidad_municipio.to_sql('mortalidad_municipio_sexo', engine, if_exists='replace', index=False)
    log(f"\n[mortalidad_municipio_sexo] OK (mapeada): {df_mortalidad_municipio.shape[0]} filas, {df_mortalidad_municipio.shape[1]} columnas.")
    # Guardar también la original a nivel CCAA por si se necesita
    df_mort.to_sql('df_mortalidad_ccaa_sexo_original', engine, if_exists='replace', index=False)
    log(f"[df_mortalidad_ccaa_sexo_original] OK: {df_mort.shape[0]} filas, {df_mort.shape[1]} columnas. Path: {df_mort_path}")

    # 4. Distribución urbana (2003-2022)
    df_urb_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/distribucion_urbana/data_final/distribucion_urbana_municipios_2003_to_2022.csv')
    df_urb = pd.read_csv(df_urb_path, dtype={'municipio_code': str})
    years_cols = [c for c in df_urb.columns if c.isdigit()]
    df_urb_long = df_urb.melt(
        id_vars=['municipio_code'],
        value_vars=years_cols,
        var_name='year',
        value_name='proporcion_urbana'
    )
    df_urb_long = df_urb_long.rename(columns={'municipio_code': 'mun_code'})
    df_urb_long = filter_by_year_range(df_urb_long, year_column='year', start_year=START_YEAR, end_year=END_YEAR)
    df_urb_long.to_sql('distribucion_urbana', engine, if_exists='replace', index=False)
    log(f"\n[distribucion_urbana] OK: {df_urb_long.shape[0]} filas, {df_urb_long.shape[1]} columnas. Path: {df_urb_path}")

    # 5. Empresas Municipio
    df_emp_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/empresas_municipio_actividad_principal/preprocesados/empresas_municipio_actividad_principal.csv')
    df_emp = pd.read_csv(df_emp_path, dtype={'municipio_code': str})
    df_emp = df_emp.rename(
        columns={
            'municipio_code': 'mun_code',
            'Periodo': 'year', # Ya se llama 'year' en el CSV original si 'Periodo' es el año
            'Total': 'total_empresas'
        }
    )
    df_emp = filter_by_year_range(df_emp, year_column='year', start_year=START_YEAR, end_year=END_YEAR)
    df_emp.to_sql('empresas_municipio_actividad_principal', engine, if_exists='replace', index=False)
    log(f"\n[empresas_municipio_actividad_principal] OK: {df_emp.shape[0]} filas, {df_emp.shape[1]} columnas. Path: {df_emp_path}")

    # 6. Estimativas población
    df_estpop_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/estimativas_pop/preprocesados/cifras_poblacion_municipio.csv')
    df_estpop = pd.read_csv(df_estpop_path, dtype={'mun_code': str})
    # Asumiendo que esta tabla también tiene una columna 'year' o similar
    df_estpop = filter_by_year_range(df_estpop, year_column='year', start_year=START_YEAR, end_year=END_YEAR) # Ajustar 'year_column' si es diferente
    df_estpop.to_sql('estimativas_pop', engine, if_exists='replace', index=False)
    log(f"\n[estimativas_pop] OK: {df_estpop.shape[0]} filas, {df_estpop.shape[1]} columnas. Path: {df_estpop_path}")

    # 7. IDHM municipal
    df_idhm_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/idhm_indice_desarrollo_humano_municipal/IRPFmunicipios_final_IDHM.csv')
    df_idhm = pd.read_csv(df_idhm_path, dtype={'mun_code': str})
    # Esta tabla tiene 'year', aplicar filtro
    df_idhm = filter_by_year_range(df_idhm, year_column='year', start_year=START_YEAR, end_year=END_YEAR)
    df_idhm.to_sql('idhm_indice_desarrollo_humano_municipal', engine, if_exists='replace', index=False)
    log(f"\n[idhm_indice_desarrollo_humano_municipal] OK: {df_idhm.shape[0]} filas, {df_idhm.shape[1]} columnas. Path: {df_idhm_path}")

    # 8. Indicadores fecundidad provincias
    df_fert_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/indicadores_fecundidad_municipio_provincias/df_total_interpolado_full_tasa_estandarizada.csv')
    df_fert = pd.read_csv(df_fert_path, dtype=str) # 'periodo' es string, se convertirá en filter_by_year_range
    
    log("\n[indicadores_fecundidad] Provincias en datos:")
    prov_list = df_fert['provincias_name'].unique().tolist()
    log(str(sorted(prov_list)[:10])) # Muestra solo las primeras 10 para no saturar el log
    
    # Normalizar nombres de provincia para el merge
    df_fert['provincias_name_clean'] = df_fert['provincias_name'].str.normalize('NFKD').str.encode('ASCII', errors='ignore').str.decode('ASCII').str.upper()
    df_prov['provincia_name_clean'] = df_prov['provincia_name'].str.normalize('NFKD').str.encode('ASCII', errors='ignore').str.decode('ASCII').str.upper()
    
    df_fert_merged = df_fert.merge(
        df_prov[['CPRO', 'provincia_name_clean']], 
        left_on='provincias_name_clean', 
        right_on='provincia_name_clean', 
        how='left'
    )
    
    n_missing = df_fert_merged['CPRO'].isna().sum()
    if n_missing > 0:
        log(f"\n[indicadores_fecundidad] ADVERTENCIA: {n_missing} filas sin correspondencia de provincia tras normalización.")
        missing_prov = df_fert_merged[df_fert_merged['CPRO'].isna()]['provincias_name'].unique()
        log(f"Provincias sin match: {sorted(missing_prov.tolist())}")
    
    df_fert_merged = df_fert_merged.drop(['provincias_name_clean', 'provincia_name_clean'], axis=1)
    df_fert_merged = df_fert_merged.rename(columns={
        'tasa_estandarizada': 'tasa_fert_prov', 
        'periodo': 'year', # 'periodo' es la columna de año aquí
        'CPRO': 'cpro'      # Código de provincia
    })
    df_fert_merged = filter_by_year_range(df_fert_merged, year_column='year', start_year=START_YEAR, end_year=END_YEAR)
    # Mapear fecundidad a municipios
    # Asegurarse que 'cpro' en df_fert_merged y 'CPRO' en df_eq son compatibles (ambos strings de 2 dígitos)
    df_fert_merged['cpro'] = df_fert_merged['cpro'].astype(str).str.zfill(2)
    df_fecundidad_municipio = pd.merge(df_fert_merged, df_eq[['mun_code', 'NOMBRE', 'CPRO']], left_on='cpro', right_on='CPRO', how='left')
    if df_fecundidad_municipio['mun_code'].isna().any():
        log(f"ADVERTENCIA en fecundidad_municipio: {df_fecundidad_municipio['mun_code'].isna().sum()} filas no pudieron mapear mun_code.")
    df_fecundidad_municipio = df_fecundidad_municipio.drop(columns=['CPRO']) # Eliminar columna redundante
    df_fecundidad_municipio.to_sql('fecundidad_municipio', engine, if_exists='replace', index=False)
    log(f"\n[fecundidad_municipio] OK (mapeada): {df_fecundidad_municipio.shape[0]} filas, {df_fecundidad_municipio.shape[1]} columnas.")
    # Guardar también la original a nivel provincia
    df_fert_merged.to_sql('indicadores_fecundidad_provincia_original', engine, if_exists='replace', index=False)
    log(f"[indicadores_fecundidad_provincia_original] OK: {df_fert_merged.shape[0]} filas, {df_fert_merged.shape[1]} columnas. Path: {df_fert_path}")

    # 9. Interest data (nacional)
    # Estos datos son anuales o ya están preprocesados a una frecuencia que podría no necesitar el filtro START_YEAR, END_YEAR
    # o si lo necesita, la columna 'date' debe ser convertida a 'year'.
    df_fixed_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/interest_data_ETL/imputados/interest_fixed_imputado.csv')
    df_nom_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/interest_data_ETL/imputados/interest_nominal_imputado.csv')
    df_real_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/interest_data_ETL/imputados/interest_real_imputado.csv')

    df_fixed = pd.read_csv(df_fixed_path, sep=';', parse_dates=['date'])
    df_nom = pd.read_csv(df_nom_path, sep=';', parse_dates=['date'])
    df_real = pd.read_csv(df_real_path, sep=';', parse_dates=['date'])
    
    df_int = df_fixed.merge(df_nom, on='date', suffixes=('_fixed', '_nominal')).merge(df_real, on='date')
    df_int = df_int.rename(columns={'interest': 'interest_real', 'interest_fixed': 'interest_fixed', 'interest_nominal': 'interest_nominal'})
    df_int['year'] = df_int['date'].dt.year # Extraer año para posible filtro
    df_int = filter_by_year_range(df_int, year_column='year', start_year=START_YEAR, end_year=END_YEAR)
    df_int.to_sql('interest_data_nacional', engine, if_exists='replace', index=False) # Renombrado para claridad
    log(f"\n[interest_data_nacional] OK: {df_int.shape[0]} filas, {df_int.shape[1]} columnas. Paths: {df_fixed_path}, {df_nom_path}, {df_real_path}")

    # 10. Nivel educativo CCAA
    df_edu_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/nivel_educativo_comunidades/data_final/nivel_educativo_comunidades_completo.csv')
    df_edu = pd.read_csv(df_edu_path, dtype={'ccaa_code': str})
    # Asumiendo que tiene una columna 'year' o 'Año' o 'Periodo'
    # La columna de año en el CSV es 'año'
    df_edu = df_edu.rename(columns={'año': 'year'})
    df_edu['ccaa_code'] = df_edu['ccaa_code'].astype(str).str.zfill(2) # Asegurar formato '01', '02', etc.
    df_edu = filter_by_year_range(df_edu, year_column='year', start_year=START_YEAR, end_year=END_YEAR)
    
    # Mapear nivel educativo a municipios
    df_nivel_educativo_municipio = pd.merge(df_edu, df_eq[['mun_code', 'NOMBRE', 'CODAUTO']], left_on='ccaa_code', right_on='CODAUTO', how='left')
    if df_nivel_educativo_municipio['mun_code'].isna().any():
        log(f"ADVERTENCIA en nivel_educativo_municipio: {df_nivel_educativo_municipio['mun_code'].isna().sum()} filas no pudieron mapear mun_code.")
    df_nivel_educativo_municipio = df_nivel_educativo_municipio.drop(columns=['CODAUTO']) # Eliminar columna redundante
    df_nivel_educativo_municipio.to_sql('nivel_educativo_municipio', engine, if_exists='replace', index=False)
    log(f"\n[nivel_educativo_municipio] OK (mapeada): {df_nivel_educativo_municipio.shape[0]} filas, {df_nivel_educativo_municipio.shape[1]} columnas.")
    # Guardar también la original a nivel CCAA
    df_edu.to_sql('nivel_educativo_ccaa_original', engine, if_exists='replace', index=False)
    log(f"[nivel_educativo_ccaa_original] OK: {df_edu.shape[0]} filas, {df_edu.shape[1]} columnas. Path: {df_edu_path}")

    # 11. PIE (Participación en Ingresos del Estado)
    df_pie_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/PIE/data/raw/finanzas/liquidaciones/preprocess/pie_final_final.csv')
    df_pie = pd.read_csv(df_pie_path, dtype={'codigo_municipio': str})
    df_pie = df_pie.rename(columns={'codigo_municipio': 'mun_code', 'año': 'year'})
    df_pie = filter_by_year_range(df_pie, year_column='year', start_year=START_YEAR, end_year=END_YEAR)
    # Asegurarse de que 'mun_code' no esté también como índice si ya es una columna
    if 'mun_code' in df_pie.columns and df_pie.index.name == 'mun_code':
        df_pie = df_pie.reset_index(drop=True)
    elif df_pie.index.name == 'mun_code': # Si solo está como índice pero no como columna
         df_pie = df_pie.reset_index() # Convertir el índice mun_code en columna

    df_pie.to_sql('pie_liquidaciones_municipales', engine, if_exists='replace', index=False)
    log(f"\n[pie_liquidaciones_municipales] OK: {df_pie.shape[0]} filas, {df_pie.shape[1]} columnas. Path: {df_pie_path}")

    # 12. Tamaño medio hogares CCAA (Placeholder para imputación)
    # Esta tabla requiere un tratamiento especial (imputación para 2014-2020)
    df_hogares_path = os.path.join(os.path.dirname(BASE_DIR), 'ETL/tamaño_medio_hogares_ccaa/data_final/tamaño_medio_hogares_ccaa_completo.csv')
    log(f"\nCargando y procesando [tamaño_medio_hogares_ccaa] desde: {df_hogares_path}")
    if os.path.exists(df_hogares_path):
        df_hogares_raw = pd.read_csv(df_hogares_path) # Dtype se manejará después
        
        # Renombrar columnas para consistencia y asegurar tipos correctos
        df_hogares_raw = df_hogares_raw.rename(columns={
            'comunidad_code': 'ccaa_code', # Nombre de columna en el CSV
            'año': 'year',               # Nombre de columna en el CSV
            'total': 'tamano_medio_hogar' # Nombre de columna en el CSV
        })
        df_hogares_raw['ccaa_code'] = df_hogares_raw['ccaa_code'].astype(str).str.split('.').str[0] # Limpiar '1.0' a '1'
        df_hogares_raw['year'] = pd.to_numeric(df_hogares_raw['year'])
        df_hogares_raw['tamano_medio_hogar'] = pd.to_numeric(df_hogares_raw['tamano_medio_hogar'])

        log(f"Datos crudos de hogares cargados: {df_hogares_raw.shape[0]} filas.")
        log(df_hogares_raw.head().to_string())

        # Años para los que necesitamos datos (2014-2020)
        years_needed = list(range(START_YEAR, END_YEAR + 1))
        
        # Datos existentes que caen en el rango 2014-2020 (probablemente ninguno según el CSV)
        df_hogares_existing_in_range = df_hogares_raw[df_hogares_raw['year'].isin(years_needed)].copy()
        df_hogares_existing_in_range['imputed'] = 0
        
        # Datos que se usarán para la regresión (fuera del rango 2014-2020, ej. 2021-2025)
        # Usaremos todos los datos disponibles en df_hogares_raw para ajustar la regresión,
        # ya que la función impute_household_size se encarga de ello.
        
        # Imputar para los años 2014-2020
        df_hogares_imputados_target_range = impute_household_size(df_hogares_raw.copy(), years_needed)
        
        # Combinar datos imputados para 2014-2020 con los datos originales que ya estaban en ese rango (si los hubiera)
        # y con los datos originales fuera de ese rango (2021 en adelante) que queremos conservar.
        
        # Datos originales que NO están en el rango de imputación (ej. 2021+)
        df_hogares_original_future = df_hogares_raw[df_hogares_raw['year'] > END_YEAR].copy()
        df_hogares_original_future['imputed'] = 0 # No son imputados

        # Concatenar:
        # 1. Datos imputados/originales para 2014-2020 (df_hogares_imputados_target_range ya maneja esto)
        # 2. Datos originales para años > 2020 (df_hogares_original_future)
        df_hogares_final_completo = pd.concat([df_hogares_imputados_target_range, df_hogares_original_future], ignore_index=True)
        df_hogares_final_completo = df_hogares_final_completo.sort_values(by=['ccaa_code', 'year']).reset_index(drop=True)

        if not df_hogares_final_completo.empty:
            df_hogares_final_completo.to_sql('tamaño_medio_hogares_ccaa', engine, if_exists='replace', index=False)
            log(f"[tamaño_medio_hogares_ccaa] OK (con imputación): {df_hogares_final_completo.shape[0]} filas, {df_hogares_final_completo.shape[1]} columnas.")
            log(df_hogares_final_completo[df_hogares_final_completo['year'].isin(years_needed)].head().to_string())
        else:
            log("ADVERTENCIA: No se generaron datos finales para tamaño_medio_hogares_ccaa.")

    else:
        log(f"ADVERTENCIA: No se encontró el archivo {df_hogares_path}. La tabla 'tamaño_medio_hogares_ccaa' no se cargará.")

except Exception as e:
    log(f"\nERROR GENERAL DURANTE LA CARGA ETL: {str(e)}")
    import traceback
    log(traceback.format_exc())

log("\n--- Fin del proceso de carga ETL V2 ---")
print(f"\nCarga completa (o con errores). Revisa el log en {LOG_PATH}")
