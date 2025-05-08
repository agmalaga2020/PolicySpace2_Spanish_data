# TODO - Registro de errores y depuración: Informe de Población Municipal

## Estado actual

- [ ] Error: `No se pudo leer o procesar tabla_equivalencias: The column label 'CMUN' is not unique.. Se mostrarán solo datos de población.`
- [ ] El merge no añade la columna `NOMBRE_MUNICIPIO` a los datos combinados, aunque sí existe en el DataFrame de equivalencias tras el renombrado.
- [ ] El selector muestra municipios, pero al seleccionar uno aparece: `La columna 'NOMBRE_MUNICIPIO' no está presente en los datos combinados. No se puede filtrar por municipio. Verifica el merge.`

## Acciones realizadas

- [X] Verificado el esquema de la tabla `tabla_equivalencias` en SQLite: no hay columnas duplicadas en la definición.
- [X] Comprobado que al leer la tabla con `pd.read_sql_query` y renombrar, la columna `NOMBRE_MUNICIPIO` sí aparece en el DataFrame de equivalencias.
- [X] Realizado el merge sobre `df_pop` y `df_eq` en un script de prueba fuera de Streamlit: la columna `NOMBRE_MUNICIPIO` aparece en el DataFrame resultante.
- [ ] El merge dentro de Streamlit falla y la columna no aparece en los datos combinados.

## Hipótesis

- [X] El error "The column label 'CMUN' is not unique" puede deberse a cómo SQLAlchemy interpreta la tabla al no tener clave primaria definida y múltiples filas con el mismo valor de `CMUN`.
- [ ] El merge puede estar fallando silenciosamente o descartando columnas si hay conflicto de nombres o tipos.

## Próximos pasos sugeridos

- [X] Probar a crear una vista temporal en SQLite con columnas únicas antes de cargarla en pandas.
- [ ] Verificar si hay valores nulos o inconsistentes en `CMUN` o en los códigos de municipio de ambas tablas.
- [ ] Registrar aquí cualquier hallazgo relevante o cambio realizado para depuración futura.

## Resultados de la prueba con vista temporal

- [X] Se creó la vista `vista_equivalencias_unicas` en SQLite con una fila por cada CMUN.
- [X] Al leer la vista desde pandas y hacer el merge, la columna `NOMBRE_MUNICIPIO` aparece correctamente en el DataFrame combinado.
- [X] Esto confirma que el uso de la vista soluciona el problema de unicidad y permite el merge correcto.

## Hallazgos adicionales

- [X] El error "The column label 'CMUN' is not unique" ocurre solo al usar SQLAlchemy/pandas dentro de Streamlit, no en scripts de prueba fuera.
- [X] Cuando ocurre el error, el bloque except se ejecuta y nunca se realiza el merge, por lo que 'NOMBRE_MUNICIPIO' no aparece en los datos combinados.
- [ ] La única solución definitiva es modificar la tabla en la base de datos para que tenga clave primaria o crear una vista temporal con columnas únicas antes de cargarla en pandas.

---
