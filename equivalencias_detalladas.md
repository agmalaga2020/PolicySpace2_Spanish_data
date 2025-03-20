# Equivalencias de Datos entre Brasil y España para PolicySpace2

## 1. Datos Geográficos y Administrativos

| Documento Original (Brasil) | Equivalente Español | Fuente Española | URL/API |
|----------------------------|---------------------|-----------------|---------|
| ACPs_BR.csv | Secciones Censales | INE - API JSON | https://www.ine.es/dyngs/DAB/index.htm?cid=1099 |
| ACPs_MUN_CODES.csv | Relación Secciones-Municipios | INE - API JSON | https://www.ine.es/dyngs/DAB/index.htm?cid=1099 |
| RM_BR_STATES.csv | Relación Municipios-Provincias | INE - Códigos Territoriales | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177031&menu=ultiDatos&idp=1254734710990 |
| STATES_ID_NUM.csv | Códigos Numéricos Territoriales | INE - Códigos Territoriales | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177031&menu=ultiDatos&idp=1254734710990 |
| names_and_codes_municipalities.csv | Relación de Municipios y Códigos | INE - Códigos Territoriales | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177031&menu=ultiDatos&idp=1254734710990 |
| single_aps_2000.csv y single_aps_2010.csv | Listado de Códigos Municipales | INE - Códigos Territoriales | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177031&menu=ultiDatos&idp=1254734710990 |

## 2. Datos Demográficos

### 2.1 Población

| Documento Original (Brasil) | Equivalente Español | Fuente Española | URL/API |
|----------------------------|---------------------|-----------------|---------|
| estimativas_pop.csv | Cifras de Población por Municipio | INE - API JSON | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177011&menu=resultados&idp=1254734710990 |
| pop_men_2000.csv y pop_men_2010.csv | Población Masculina por Edad y Municipio | INE - API JSON | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177012&menu=resultados&idp=1254734710990 |
| pop_women_2000.csv y pop_women_2010.csv | Población Femenina por Edad y Municipio | INE - API JSON | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177012&menu=resultados&idp=1254734710990 |
| num_people_age_gender_AP_2000.csv y num_people_age_gender_AP_2010.csv | Población por Sección Censal, Género y Edad | INE - Censos de Población | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177012&menu=resultados&idp=1254734710990 |
| average_num_members_families_2010.csv | Tamaño Medio de los Hogares | INE - Censos de Población | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176952&menu=resultados&idp=1254735572981 |
| prop_urban_2000_2010.csv | Distribución de Población Urbana/Rural | INE - Censos de Población | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176951&menu=resultados&idp=1254735572981 |

### 2.2 Fertilidad

| Documento Original (Brasil) | Equivalente Español | Fuente Española | URL/API |
|----------------------------|---------------------|-----------------|---------|
| fertility_[ESTADO].csv (27 archivos) | Indicadores de Fecundidad por CCAA | INE - Indicadores Demográficos Básicos | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177003&menu=resultados&idp=1254735573002 |

### 2.3 Mortalidad

| Documento Original (Brasil) | Equivalente Español | Fuente Española | URL/API |
|----------------------------|---------------------|-----------------|---------|
| mortality_men_[ESTADO].csv (27 archivos) | Tablas de Mortalidad Masculina por CCAA | INE - Tablas de Mortalidad | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177004&menu=resultados&idp=1254735573002 |
| mortality_women_[ESTADO].csv (27 archivos) | Tablas de Mortalidad Femenina por CCAA | INE - Tablas de Mortalidad | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177004&menu=resultados&idp=1254735573002 |

### 2.4 Matrimonio

| Documento Original (Brasil) | Equivalente Español | Fuente Española | URL/API |
|----------------------------|---------------------|-----------------|---------|
| marriage_age_men.csv y marriage_age_men_original.csv | Matrimonios por Edad del Esposo | INE - Estadística de Matrimonios | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176999&menu=resultados&idp=1254735573002 |
| marriage_age_women.csv y marriage_age_women_original.csv | Matrimonios por Edad de la Esposa | INE - Estadística de Matrimonios | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176999&menu=resultados&idp=1254735573002 |

## 3. Datos Económicos

### 3.1 Empresas

| Documento Original (Brasil) | Equivalente Español | Fuente Española | URL/API |
|----------------------------|---------------------|-----------------|---------|
| firms_by_APs2000_t0_full.csv, firms_by_APs2000_t1_full.csv, firms_by_APs2010_t0_full.csv, firms_by_APs2010_t1_full.csv | Empresas por Municipio y Actividad Principal | INE - DIRCE | https://www.ine.es/jaxiT3/Tabla.htm?t=4721 |

### 3.2 Financiación Municipal

| Documento Original (Brasil) | Equivalente Español | Fuente Española | URL/API |
|----------------------------|---------------------|-----------------|---------|
| [ESTADO].csv (27 archivos) | Datos de Financiación Municipal | Ministerio de Hacienda - Oficina Virtual | https://www.hacienda.gob.es/es-ES/Areas%20Tematicas/Administracion%20Electronica/OVEELL/Paginas/OVEntidadesLocales.aspx |

### 3.3 Indicadores Económicos

| Documento Original (Brasil) | Equivalente Español | Fuente Española | URL/API |
|----------------------------|---------------------|-----------------|---------|
| interest_fixed.csv, interest_nominal.csv, interest_real.csv | Tipos de Interés | Banco de España | https://www.bde.es/webbde/es/estadis/infoest/tipos/tipos.html |
| idhm_2000_2010.csv | Indicadores de Desarrollo Humano Municipal | DataBank - Banco Mundial | https://databank.worldbank.org/source/world-development-indicators |

## 4. Datos Educativos

| Documento Original (Brasil) | Equivalente Español | Fuente Española | URL/API |
|----------------------------|---------------------|-----------------|---------|
| qualification_APs_2000.csv y qualification_APs_2010.csv | Nivel Educativo por Municipio | INE - Censos de Población | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176918&menu=resultados&idp=1254735976595 |

## Códigos de Acceso a la API JSON del INE

Para acceder a los datos del INE mediante su API JSON, se utiliza la siguiente estructura de URL:

```
https://servicios.ine.es/wstempus/js/{idioma}/{función}/{input}[?parámetros]
```

Donde:
- **{idioma}**: ES (español) o EN (inglés)
- **{función}**: Función implementada en el sistema (DATOS_TABLA, DATOS_SERIE, etc.)
- **{input}**: Identificadores de los elementos de entrada
- **[?parámetros]**: Parámetros opcionales

### Ejemplos de Códigos para Datos Demográficos

- Población por municipios: `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/t1/es`
- Nacimientos por municipio: `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/t2/es`
- Defunciones por municipio: `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/t3/es`

## Códigos de Acceso a Datos del Ministerio de Hacienda

Para los datos de financiación municipal, se pueden descargar desde la Oficina Virtual para la Coordinación Financiera con las Entidades Locales:

```
https://serviciostelematicosext.hacienda.gob.es/SGFAL/CONPREL
```

Es necesario navegar por las diferentes secciones para acceder a los datos específicos por municipio y año.
