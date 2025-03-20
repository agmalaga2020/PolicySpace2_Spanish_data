# Guía de Uso: Adaptación de PolicySpace2 al Contexto Español

## Introducción

Este documento proporciona instrucciones para utilizar los scripts desarrollados para adaptar el proyecto PolicySpace2 al contexto español. Se han creado varios módulos Python que permiten obtener datos españoles equivalentes a los utilizados en el proyecto original brasileño.

## Requisitos Previos

- Python 3.6 o superior
- Bibliotecas requeridas: pandas, requests, beautifulsoup4
- Conexión a Internet para acceder a las APIs

## Estructura de Archivos

- `adaptar_policyspace2_espana.py`: Script principal que integra todos los módulos
- `ine_api.py`: Módulo para conectar con la API JSON del INE (Instituto Nacional de Estadística)
- `databank_api.py`: Módulo para conectar con la API de DataBank del Banco Mundial
- `descargar_documentos_alternativos.py`: Módulo para descargar datos no disponibles mediante APIs
- `fuentes_datos_espanolas.md`: Documento con las equivalencias entre datos brasileños y españoles
- `equivalencias_archivos.csv`: CSV con las equivalencias detalladas entre archivos originales y españoles

## Instalación

1. Descargue todos los archivos Python en un mismo directorio
2. Instale las dependencias necesarias:

```bash
pip install pandas requests beautifulsoup4
```

## Uso del Script Principal

El script principal `adaptar_policyspace2_espana.py` proporciona varias opciones para obtener los datos españoles:

### Obtener Todos los Datos

Para obtener todos los datos españoles equivalentes a los utilizados en PolicySpace2:

```bash
python adaptar_policyspace2_espana.py
```

Esto ejecutará todos los módulos y guardará los resultados en el directorio `datos_espana`.

### Opciones Adicionales

El script acepta varios argumentos de línea de comandos:

- `--output DIRECTORIO`: Especifica el directorio de salida (por defecto: datos_espana)
- `--ine-only`: Obtiene solo datos del INE
- `--databank-only`: Obtiene solo datos de DataBank
- `--alt-only`: Descarga solo documentos alternativos
- `--csv-only`: Genera solo el CSV de equivalencias

Ejemplos:

```bash
# Obtener solo datos del INE
python adaptar_policyspace2_espana.py --ine-only

# Especificar un directorio de salida diferente
python adaptar_policyspace2_espana.py --output datos_policyspace_espana

# Generar solo el CSV de equivalencias
python adaptar_policyspace2_espana.py --csv-only
```

## Descripción de los Módulos

### INE API (ine_api.py)

Este módulo proporciona una clase para interactuar con la API JSON del INE (Instituto Nacional de Estadística) de España. Incluye métodos para obtener:

- Datos de municipios y sus códigos
- Datos de población por municipio, sexo y edad
- Proporción de población urbana por municipio
- Número de empresas por municipio

### DataBank API (databank_api.py)

Este módulo proporciona una clase para interactuar con la API de DataBank del Banco Mundial. Incluye métodos para obtener:

- Datos del PIB para España
- Datos del PIB per cápita
- Datos de desempleo
- Datos del Índice de Desarrollo Humano
- Datos de tasas de interés

### Documentos Alternativos (descargar_documentos_alternativos.py)

Este módulo proporciona funciones para descargar datos que no están disponibles a través de las APIs:

- Datos de financiación municipal desde el Ministerio de Hacienda
- Datos de fertilidad y mortalidad
- Datos de matrimonio por edad
- Datos de nivel educativo por municipio

## Resultados

Todos los datos obtenidos se guardan en el directorio especificado (por defecto: `datos_espana`). Además, se genera un CSV (`equivalencias_archivos.csv`) que mapea cada archivo original de PolicySpace2 con su equivalente español, incluyendo la fuente de datos y una descripción.

## Solución de Problemas

- Si recibe errores de conexión, verifique su conexión a Internet y que las URLs de las APIs estén actualizadas
- Si faltan archivos de salida, verifique que tiene permisos de escritura en el directorio de salida
- Si recibe errores de importación, asegúrese de que todos los archivos Python están en el mismo directorio

## Contacto

Para cualquier consulta o problema, por favor contacte al desarrollador del proyecto.
