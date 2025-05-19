# Lista de Tareas para la Creación de la Nueva Base de Datos

## 1. Consideraciones Iniciales de Datos:
- [] **Número de Municipios:** Aproximadamente 2168 municipios comunes debido a limitaciones en los datos de liquidaciones de hacienda (PIE) que solo cubren municipios con más de 5000 habitantes.
- [] **Descarte de Municipios:** Algunos municipios fueron descartados durante los procesos ETL por falta de datos o incoherencias.
- [] **Rango de Fechas Común:** La mayoría de las tablas cubren el rango de 2014 a 2020.

## 2. Tratamiento de Datos Específicos:
- [] **Tamaño Medio de los Hogares:**
    - [] Simular el rango de fechas de 2014 a 2020 utilizando algoritmos de regresión u otros métodos de imputación.
- [] **Datos No Municipales (Indicadores de Fecundidad, Nivel Educativo, Mortalidad):**
    - [] Mapear estos valores a nivel municipal utilizando la `tabla_equivalencias`.
- [] **Datos Nacionales (Tablas `interest_data`):**
    - [] Utilizar únicamente los rangos de fechas, ya que los datos son a nivel nacional.

## 3. Creación de la Nueva Base de Datos (`database 2`):
- [] **Objetivo:** Crear una nueva base de datos donde todas las tablas estén correctamente conectadas y los datos tratados según las consideraciones anteriores.
- [] **Referencia:** Utilizar la estructura y contenido de la carpeta `data base` actual como guía.

## 4. Generación de Esquema Relacional:
- [] **Formato:** Similar al esquema `data base/esquema_db_record.png`.
- [] **Contenido:** Representar la estructura relacional de la nueva base de datos creada en `database 2`.

## 5. Pasos Detallados (Plan Propuesto):
- [] **Paso 1: Copiar y Reestructurar Archivos Existentes:**
    - [] Analizar la carpeta `data base` actual.
    - [] Copiar los scripts ETL relevantes (ej. `etl_load_data.py`) y archivos de datos a `database 2`.
    - [] Modificar los scripts para reflejar las nuevas lógicas de tratamiento de datos.
- [] **Paso 2: Implementar Lógica de Imputación para Tamaño Medio de Hogares:**
    - [] Desarrollar o adaptar scripts para realizar la regresión/imputación de datos faltantes.
- [] **Paso 3: Implementar Mapeo de Datos No Municipales:**
    - [] Modificar los scripts ETL para incorporar el mapeo usando `tabla_equivalencias`.
- [] **Paso 4: Integrar `interest_data`:**
    - [] Asegurar que los scripts ETL manejen correctamente estas tablas, considerando solo las fechas.
- [] **Paso 5: Ejecutar ETL y Cargar Datos:**
    - [] Correr los scripts ETL modificados para poblar la nueva base de datos (probablemente un nuevo archivo SQLite en `database 2`).
- [] **Paso 6: Generar el Nuevo Esquema Relacional:**
    - [] Utilizar herramientas o scripts para visualizar y guardar el esquema de la nueva base de datos.
