# PolicySpace2_Spanish_data 🇪🇸

¡Bienvenido! Este proyecto adapta el modelo PolicySpace2 al contexto español, integrando datos oficiales y procesos ETL avanzados para simular y analizar políticas públicas, dinámicas demográficas y socioeconómicas a nivel municipal y regional.

---

## 📚 ¿Qué es este proyecto?

Es una adaptación exhaustiva de PolicySpace2 (modelo brasileño de simulación basada en agentes) para España. Aquí se han reconstruido todos los datasets clave (población, mortalidad, fecundidad, empresas, educación, urbanismo, hogares, finanzas municipales, etc.) usando fuentes oficiales como el INE, Banco de España, Eurostat y ministerios.

---

## 🗂️ Estructura y Procesos ETL

Cada subcarpeta de `ETL/` contiene un flujo de trabajo reproducible (notebooks y scripts) para transformar datos brutos en datasets limpios y comparables con el modelo original. Ejemplos destacados:

- **Población por municipio**: Extracción, limpieza, detección/corrección de outliers, interpolación y pivoteo para obtener series completas (ver `estimativas_pop/` y `cifras_poblacion_municipio/`).
- **Mortalidad**: Procesamiento de tasas por edad, sexo y comunidad, imputación de valores faltantes y generación de archivos listos para simulación (`df_mortalidad_ccaa_sexo/`).
- **Distribución urbana**: Modelo proxy para estimar la proporción urbana/rural por municipio, combinando densidad, población y validación con datos reales (`distribucion_urbana/`).
- **Empresas**: Limpieza avanzada, cruce con población, imputación de NaN y generación de series históricas de empresas por municipio (`empresas_municipio_actividad_principal/`).
- **Fecundidad**: Interpolación por edad, estandarización internacional y exportación por comunidad y provincia (`indicadores_fecundidad_municipio_provincias/`).
- **Tasas de interés**: Descarga, imputación y validación de series del BCE y Banco de España, tanto nominales como reales (`interest_data_ETL/`).
- **Nivel educativo**: Homogeneización y codificación de niveles educativos por comunidad y año (`nivel_educativo_comunidades/`).
- **Tamaño medio de hogares**: Extracción y limpieza de series por comunidad autónoma (`tamaño_medio_hogares_ccaa/`).
- **Finanzas municipales (PIE)**: Descarga, selección, procesamiento y unificación de liquidaciones municipales para análisis fiscal (`PIE/`).

Cada notebook incluye un informe detallado del proceso, decisiones de limpieza, justificación de imputaciones y visualizaciones.

---

## 🔗 Fuentes de Datos

- **INE**: Población, mortalidad, fecundidad, hogares, empresas, educación, urbanismo.
- **Banco de España / BCE**: Tasas de interés.
- **Eurostat**: Inflación (HICP).
- **Ministerio de Hacienda**: Finanzas municipales.
- **Portales autonómicos**: Educación, indicadores locales.

---

## 📊 Ejemplo de Procesos y Resultados

- **Población**: +8.000 municipios, 30 años, 0% NaN tras limpieza.
- **Mortalidad**: 38 archivos finales (hombres/mujeres x comunidad), 0% NaN, tasas adaptadas a formato PolicySpace2.
- **Empresas**: Imputación dual (0 para municipios sin actividad, media para casos residuales), sin NaN.
- **Fecundidad**: Interpolación por edad, estandarización a nacimientos por mujer, exportación por comunidad/provincia.
- **Urbanismo**: Modelo de reglas calibrado y validado contra datos reales del INE.
- **Educación y hogares**: Series anuales limpias y listas para simulación.

---

## 🚦 Estado del Proyecto

- Todos los procesos ETL son reproducibles y documentados.
- Los datasets finales están listos para simulaciones, análisis y visualizaciones.
- Se han documentado limitaciones (resolución espacial, diferencias de definición internacional, etc.) y se proponen mejoras futuras.

---

## 📁 ¿Qué encontrarás en cada carpeta?

- **ETL/**: Notebooks y scripts de procesamiento, informes y datasets intermedios/finales.
- **datos_espana/**: Datasets finales y equivalencias.
- **Documentación**: guías de uso, fuentes, reportes de estado y equivalencias.

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- 500 MB de espacio libre en disco
- Conexión a Internet (para descargar datos actualizados)

### Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/agmalaga2020/PolicySpace2_Spanish_data.git
   cd PolicySpace2_Spanish_data
   ```

2. **Crear entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verificar la instalación:**
   ```bash
   python check_database_health.py
   ```

### Uso del Dashboard Interactivo

El proyecto incluye un dashboard Streamlit para explorar los datos de forma interactiva:

1. **Instalar dependencias del dashboard:**
   ```bash
   cd dashboard
   pip install -r requirements.txt
   ```

2. **Ejecutar el dashboard:**
   ```bash
   streamlit run app.py
   ```

3. **Abrir en el navegador:**
   El dashboard se abrirá automáticamente en `http://localhost:8501`

### Uso de Scripts ETL

Para reproducir o actualizar los procesos de limpieza y transformación de datos:

1. **Navegar a la carpeta ETL específica:**
   ```bash
   cd ETL/estimativas_pop  # Ejemplo: datos de población
   ```

2. **Abrir el notebook Jupyter:**
   ```bash
   jupyter notebook
   ```

3. **Ejecutar el notebook completo o celdas individuales** para reproducir el proceso ETL

---

## 🧑‍💻 ¿Cómo usarlo?

### Opción 1: Dashboard Interactivo (Recomendado para exploración)
- Ejecuta `streamlit run dashboard/app.py`
- Explora datos, crea visualizaciones y exporta resultados
- Genera informes personalizados

### Opción 2: Scripts Python
- Usa los scripts principales para obtener datos actualizados:
  ```bash
  python adaptar_policyspace2_espana.py
  ```
- Consulta `guia_uso.md` para opciones avanzadas

### Opción 3: Notebooks Jupyter (Para desarrollo)
1. Revisa los notebooks de ETL para entender y reproducir cada flujo de datos
2. Usa los datasets finales para alimentar modelos de simulación, análisis estadístico o visualizaciones
3. Consulta los informes incluidos en cada notebook para entender las decisiones de limpieza y modelado

### Opción 4: Acceso Directo a la Base de Datos
```python
import sqlite3
import pandas as pd

# Conectar a la base de datos
conn = sqlite3.connect('data base/datawarehouse.db')

# Consultar datos
df = pd.read_sql_query("SELECT * FROM tabla_poblacion LIMIT 100", conn)
print(df.head())

conn.close()
```

---

## ✨ Ejemplo de impacto

> Este proyecto permite simular, con datos reales y actualizados, el efecto de políticas públicas en España: desde vivienda y natalidad hasta educación, empleo y urbanismo. Es una base robusta para investigación, docencia y análisis de políticas.

**Ejemplo de uso:**  
Supón que quieres analizar cómo afectaría una subida de los tipos de interés del BCE al acceso a la vivienda y la natalidad en municipios rurales frente a urbanos.  
1. Usando los datasets de tasas de interés (`interest_data_ETL/`), población (`estimativas_pop/`), fecundidad (`indicadores_fecundidad_municipio_provincias/`) y urbanismo (`distribucion_urbana/`), puedes alimentar un modelo PolicySpace2 adaptado.
2. Simulas diferentes escenarios de política monetaria y observas el impacto en la formación de hogares, nacimientos y migración interna.
3. Visualizas los resultados para identificar municipios más vulnerables o resilientes, y orientar políticas de vivienda o incentivos a la natalidad.
   
---

## 🛠️ Herramientas Útiles

### Verificar Salud de la Base de Datos
```bash
python check_database_health.py
```
Este script verifica la integridad de los datos y proporciona estadísticas sobre las tablas.

### Generar Mapas Pregenerados
```bash
python pregenerar_mapas_pie.py
```
Genera visualizaciones geoespaciales para análisis rápido.

### Adaptar Datos de PolicySpace2
```bash
python adaptar_policyspace2_espana.py --help
```
Ver todas las opciones para obtener y actualizar datos.

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor, lee [CONTRIBUTING.md](CONTRIBUTING.md) para conocer los detalles sobre:
- Cómo reportar bugs
- Cómo proponer nuevas funcionalidades
- Guías de estilo de código
- Proceso de pull requests

---

## 📄 Documentación Adicional

- **[guia_uso.md](guia_uso.md)**: Guía detallada de uso de scripts y APIs
- **[fuentes_datos_espanolas.md](fuentes_datos_espanolas.md)**: Documentación de fuentes de datos
- **[equivalencias_detalladas.md](equivalencias_detalladas.md)**: Mapeo entre datos brasileños y españoles
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Guía para contribuidores
- **[dashboard/TODO.md](dashboard/TODO.md)**: Estado del desarrollo del dashboard

---

## 📊 Estadísticas del Proyecto

- **Municipios cubiertos**: 8.131
- **Provincias**: 50
- **Comunidades Autónomas**: 17 + 2 ciudades autónomas
- **Años de datos**: 2013-2022 (según la fuente)
- **Tablas en la base de datos**: 30+
- **Tamaño de la base de datos**: ~25 MB

---

## 📬 Contacto

¿Dudas o sugerencias? 
- Abre un [issue](https://github.com/agmalaga2020/PolicySpace2_Spanish_data/issues)
- Consulta la [documentación](guia_uso.md)
- Revisa los [issues existentes](https://github.com/agmalaga2020/PolicySpace2_Spanish_data/issues)

---

## 📝 Licencia

Ver el archivo [LICENSE](LICENSE) para más detalles.

---

¡Explora, aprende y contribuye a la simulación de políticas públicas en España! 🇪🇸🚀
