import pandas as pd
import glob
from sqlalchemy import create_engine

# Crear motor de base de datos (SQLite como ejemplo)
engine = create_engine('sqlite:///datawarehouse.db')

# 1. Dimensiones a partir de equivalencias
df_eq = pd.read_csv('ETL/tabla_equivalencias/data/df_equivalencias_municipio_CORRECTO.csv', dtype=str)

# DimComunidad
dim_comunidad = (
    df_eq[['CODAUTO']]
      .drop_duplicates()
      .rename(columns={'CODAUTO': 'ccaa_code'})
)
dim_comunidad.to_sql('dim_comunidad', engine, if_exists='replace', index=False)

# DimProvincia
dim_provincia = (
    df_eq[['CODAUTO', 'CPRO']]
      .drop_duplicates()
      .rename(columns={'CODAUTO': 'ccaa_code', 'CPRO': 'cpro'})
)
dim_provincia.to_sql('dim_provincia', engine, if_exists='replace', index=False)

# DimMunicipio
dim_municipio = (
    df_eq[['CODAUTO', 'CPRO', 'CMUN', 'mun_code', 'NOMBRE']]
      .drop_duplicates()
      .rename(columns={
          'CODAUTO': 'ccaa_code',
          'CPRO': 'cpro',
          'CMUN': 'cmun',
          'mun_code': 'mun_code',
          'NOMBRE': 'municipio_name'
      })
)
dim_municipio.to_sql('dim_municipio', engine, if_exists='replace', index=False)

# 2. DimFecha (años 2003–2025)
years = list(range(2003, 2026))
dim_fecha = pd.DataFrame({
    'year': years,
    'date_key': pd.to_datetime([f"{y}-01-01" for y in years])
})
dim_fecha.to_sql('dim_fecha', engine, if_exists='replace', index=False)

# 3. Hechos
# 3.1 Fertilidad provincias
df_fert_prov = pd.read_csv(
    'ETL/indicadores_fecundidad_municipio_provincias/df_total_interpolado_full_tasa_estandarizada.csv',
    dtype={'CPRO': str}
)
df_fert_prov = df_fert_prov.rename(
    columns={'CPRO': 'cpro', 'periodo': 'year', 'tasa_estandarizada': 'tasa_fert_prov'})
df_fert_prov[['cpro', 'year', 'tasa_fert_prov']].to_sql(
    'fact_fertilidad_provincia', engine, if_exists='replace', index=False)

# 3.2 Fertilidad comunidades
df_fert_com = pd.read_csv(
    'ETL/indicadores_fecundidad_municipio_provincias/df_total_interpolado_full.csv',
    dtype={'CODAUTO': str}
)
df_fert_com = df_fert_com.rename(
    columns={'CODAUTO': 'ccaa_code', 'periodo': 'year', 'total_interpolado': 'tasa_fert_com'})
df_fert_com[['ccaa_code', 'year', 'tasa_fert_com']].to_sql(
    'fact_fertilidad_comunidad', engine, if_exists='replace', index=False)

# 3.3 PIE (Participación Impositiva Equilibrada)
df_pie = pd.read_csv(
    'ETL/PIE/data/raw/finanzas/liquidaciones/preprocess/pie_final_final.csv',
    dtype={'codigo_provincia': str, 'codigo_municipio': str}
)
df_pie = df_pie.rename(
    columns={
        'codigo_provincia': 'cpro',
        'codigo_municipio': 'mun_code',
        'año': 'year'
    }
)
df_pie.to_sql('fact_pie', engine, if_exists='replace', index=False)

# 3.4 Mortalidad CCAA por sexo
df_mort = pd.read_csv(
    'ETL/df_mortalidad_ccaa_sexo/df_mortalidad_final.csv',
    dtype={'ccaa_code': str}
)
df_mort = df_mort.rename(
    columns={'ccaa_code': 'ccaa_code', 'Sexo': 'sex', 'Periodo': 'year', 'Total': 'total_muertes'}
)
df_mort[['ccaa_code', 'sex', 'year', 'total_muertes']].to_sql(
    'fact_mortalidad_ccaa', engine, if_exists='replace', index=False)

# 3.5 Tamaño medio de hogares CCAA (años multiples)
frames = []
for year in [2021, 2022, 2023, 2024, 2025]:
    path = f"ETL/tamaño_medio_hogares_ccaa/data_final/tamaño_medio_hogares_ccaa_{year}.csv"
    df = pd.read_csv(path, dtype={'comunidad_code': str})
    df = df.rename(columns={'comunidad_code': 'ccaa_code', 'total': 'avg_num_people'})
    df['year'] = year
    frames.append(df[['ccaa_code', 'year', 'avg_num_people']])
pd.concat(frames, ignore_index=True).to_sql(
    'fact_hogares_ccaa', engine, if_exists='replace', index=False
)

# 3.6 Población municipio total
df_pob = pd.read_csv(
    'ETL/cifras_poblacion_municipio/cifras_poblacion_municipio.csv',
    dtype={'mun_code': str}
)
years_cols = [c for c in df_pob.columns if c.isdigit()]
df_pob_long = df_pob.melt(
    id_vars=['mun_code'], value_vars=years_cols,
    var_name='year', value_name='poblacion_total'
)
df_pob_long.to_sql('fact_poblacion_municipio', engine, if_exists='replace', index=False)

# 3.7 Empresas por municipio
df_emp = pd.read_csv(
    'ETL/empresas_municipio_actividad_principal/preprocesados/empresas_municipio_actividad_principal.csv',
    dtype={'municipio_code': str}
)
df_emp = df_emp.rename(
    columns={'municipio_code': 'mun_code', 'Periodo': 'year', 'Total': 'total_empresas'}
)
df_emp[['mun_code', 'year', 'total_empresas']].to_sql(
    'fact_empresas_municipio', engine, if_exists='replace', index=False
)

# 3.8 IDHM municipal
df_idhm = pd.read_csv(
    'ETL/idhm_indice_desarrollo_humano_municipal/idhm_2013_2022.csv',
    dtype={'cod_mun': str}
)
df_idhm = df_idhm.rename(columns={'cod_mun': 'mun_code'})
df_idhm.to_sql('fact_idhm', engine, if_exists='replace', index=False)

# 3.9 Tipos de interés
df_fixed = pd.read_csv(
    'ETL/interest_data_ETL/imputados/interest_fixed_imputado.csv',
    parse_dates=['date']
)
df_nom = pd.read_csv(
    'ETL/interest_data_ETL/imputados/interest_nominal_imputado.csv',
    parse_dates=['date']
)
df_real = pd.read_csv(
    'ETL/interest_data_ETL/imputados/interest_real_imputado.csv',
    parse_dates=['date']
)
df_int = df_fixed.merge(df_nom, on='date').merge(df_real, on='date')
df_int = df_int.rename(
    columns={
        'interest_x': 'interest_fixed',
        'interest_y': 'interest_nominal',
        'interest': 'interest_real'
    }
)
df_int['date_key'] = df_int['date']
df_int[['date_key', 'interest_fixed', 'interest_nominal', 'interest_real', 'mortgage']].to_sql(
    'fact_interest', engine, if_exists='replace', index=False
)

# 3.10 Distribución urbana
df_urb = pd.read_csv(
    'ETL/distribucion_urbana/data_final/distribucion_urbana_municipios_2003_to_2022.csv',
    dtype={'municipio_code': str}
)
df_urb = df_urb.rename(columns={'municipio_code': 'mun_code'})
years_cols = [c for c in df_urb.columns if c.isdigit()]
df_urb_long = df_urb.melt(
    id_vars=['mun_code'], value_vars=years_cols,
    var_name='year', value_name='proporcion_urbana'
)
df_urb_long.to_sql('fact_urban_distribucion', engine, if_exists='replace', index=False)

# 3.11 Nivel educativo CCAA
df_edu_frames = []
for year in [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]:
    path = f"ETL/nivel_educativo_comunidades/data_final/nivel_educativo_comunidades_{year}.csv"
    df = pd.read_csv(path, dtype={'ccaa_code': str})
    id_vars = ['ccaa_code']
    value_vars = [col for col in df.columns if col.replace('.', '').isdigit()]
    df_long = df.melt(
        id_vars=id_vars, value_vars=value_vars,
        var_name='education_level', value_name='count'
    )
    df_long['year'] = year
    df_edu_frames.append(df_long)
pd.concat(df_edu_frames, ignore_index=True).to_sql(
    'fact_educacion_ccaa', engine, if_exists='replace', index=False
)

print("Carga de datos completa.")
