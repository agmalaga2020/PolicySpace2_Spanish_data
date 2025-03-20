# Categorización de Documentos para Adaptación al Contexto Español

## 1. Datos Geográficos y Administrativos
- **ACPs_BR.csv**: Códigos de áreas de ponderación (ID;ACPs;state_code)
- **ACPs_MUN_CODES.csv**: Relación entre áreas de ponderación y códigos municipales (ACPs;cod_mun)
- **RM_BR_STATES.csv**: Relación de municipios por estados (codmun)
- **STATES_ID_NUM.csv**: Códigos numéricos de estados y municipios (nummun;codmun)
- **names_and_codes_municipalities.csv**: Nombres y códigos de municipios (cod_name;cod_mun;state)
- **single_aps_2000.csv** y **single_aps_2010.csv**: Listados de códigos de municipios (mun_code)

## 2. Datos Demográficos
### 2.1 Población
- **estimativas_pop.csv**: Estimaciones de población por municipio y año (mun_code;2001;2002;...;2019)
- **pop_men_2000.csv** y **pop_men_2010.csv**: Población masculina por edad y municipio
- **pop_women_2000.csv** y **pop_women_2010.csv**: Población femenina por edad y municipio
- **num_people_age_gender_AP_2000.csv** y **num_people_age_gender_AP_2010.csv**: Población por área, género, edad y municipio
- **average_num_members_families_2010.csv**: Tamaño medio de familias por área (AREAP;avg_num_people)
- **prop_urban_2000_2010.csv**: Proporción de población urbana por municipio (cod_mun;2000;2010)

### 2.2 Fertilidad
- **fertility_[ESTADO].csv** (27 archivos, uno por estado brasileño): Tasas de fertilidad por edad y año

### 2.3 Mortalidad
- **mortality_men_[ESTADO].csv** (27 archivos): Tasas de mortalidad masculina por edad y año
- **mortality_women_[ESTADO].csv** (27 archivos): Tasas de mortalidad femenina por edad y año

### 2.4 Matrimonio
- **marriage_age_men.csv** y **marriage_age_men_original.csv**: Distribución de edad de matrimonio para hombres
- **marriage_age_women.csv** y **marriage_age_women_original.csv**: Distribución de edad de matrimonio para mujeres

## 3. Datos Económicos
### 3.1 Empresas
- **firms_by_APs2000_t0_full.csv**, **firms_by_APs2000_t1_full.csv**, **firms_by_APs2010_t0_full.csv**, **firms_by_APs2010_t1_full.csv**: Número de empresas por área de ponderación

### 3.2 Financiación Municipal
- **[ESTADO].csv** (27 archivos, uno por estado brasileño): Datos de financiación municipal (ano;fpm;cod;uf)

### 3.3 Indicadores Económicos
- **interest_fixed.csv**, **interest_nominal.csv**, **interest_real.csv**: Tasas de interés (date;interest;mortgage)
- **idhm_2000_2010.csv**: Índice de desarrollo humano municipal (year;cod_mun;idhm)

## 4. Datos Educativos
- **qualification_APs_2000.csv** y **qualification_APs_2010.csv**: Nivel educativo por área de ponderación

## Resumen de Fuentes Necesarias para España

1. **Instituto Nacional de Estadística (INE)**:
   - Datos demográficos (población por municipio, sexo y edad)
   - Datos de fertilidad y mortalidad
   - Datos de matrimonio
   - Datos de nivel educativo
   - Códigos y nomenclatura de municipios y provincias

2. **Ministerio de Hacienda**:
   - Datos de financiación municipal
   - Participación en los tributos del Estado

3. **Banco de España / DataBank**:
   - Tasas de interés
   - Indicadores económicos

4. **Ministerio de Industria, Comercio y Turismo**:
   - Datos de empresas por municipio

5. **Programa de las Naciones Unidas para el Desarrollo (PNUD)**:
   - Índice de desarrollo humano por municipio/provincia
