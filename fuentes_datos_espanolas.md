# Fuentes de Datos Españolas para PolicySpace2

## Fuentes Principales Identificadas

### Instituto Nacional de Estadística (INE)
- **Sitio web**: https://www.ine.es/
- **API JSON**: https://www.ine.es/dyngs/DAB/index.htm?cid=1099
- **Descripción**: El INE proporciona datos demográficos, económicos y sociales oficiales de España. Su API JSON permite acceder a toda la información disponible en INEbase.
- **Datos disponibles**: Población por municipios, datos demográficos, censos, estadísticas económicas, etc.

### Bibliotecas y Paquetes para Acceso a Datos
- **Python**: 
  - `ineware`: Biblioteca Python para acceder a la API JSON-stat del INE
  - Repositorio de ejemplo: https://github.com/dani537/extractor_ine
- **R**:
  - `INEapir`: Paquete R oficial del INE para acceder a su API
  - `INEbaseR`: Paquete R para obtener y analizar datos abiertos del INE

### Banco Mundial (DataBank)
- **API**: Disponible a través del módulo de datos
- **Descripción**: Proporciona indicadores económicos y de desarrollo para España y otros países.

## Equivalencias de Datos Brasil-España

### Datos Geográficos y Administrativos
- **ACPs_BR.csv** → Datos de Comunidades Autónomas y Provincias de España (INE)
- **ACPs_MUN_CODES.csv** → Códigos de municipios españoles (INE)
- **RM_BR_STATES.csv** → Relación de municipios por provincias (INE)
- **STATES_ID_NUM.csv** → Códigos numéricos de provincias y municipios (INE)
- **names_and_codes_municipalities.csv** → Relación de municipios y sus códigos (INE)

### Datos Demográficos
- **average_num_members_families_2010.csv** → Tamaño medio de los hogares por municipio (INE)
- **estimativas_pop.csv** → Cifras de población por municipios (INE)
- **pop_men_2000.csv/pop_men_2010.csv** → Población masculina por edad y municipio (INE)
- **pop_women_2000.csv/pop_women_2010.csv** → Población femenina por edad y municipio (INE)
- **num_people_age_gender_AP_2000.csv/num_people_age_gender_AP_2010.csv** → Población por sexo, edad y municipio (INE)
- **fertility_*.csv** → Indicadores de fecundidad por comunidades autónomas (INE)
- **mortality_*.csv** → Indicadores de mortalidad por comunidades autónomas (INE)
- **marriage_age_*.csv** → Edad media al matrimonio por sexo (INE)

### Datos Económicos
- **idhm_2000_2010.csv** → Indicadores de desarrollo humano municipal (DataBank)
- **interest_*.csv** → Tipos de interés (Banco de España)
- **firms_by_APs*.csv** → Empresas por municipio (INE)

### Datos Urbanos
- **prop_urban_2000_2010.csv** → Proporción de población urbana por municipio (INE)
- **qualification_APs_*.csv** → Nivel de formación por municipio (INE)

## URLs Específicas para Datos Clave
- Códigos de municipios: https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177031&menu=ultiDatos&idp=1254734710990
- Cifras de población: https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177011&menu=resultados&idp=1254734710990
- Datos demográficos: https://www.ine.es/dynt3/inebase/index.htm?padre=1894&capsel=1895
