#!/usr/bin/env python3
"""
Script de Ejemplo - Consultas a la Base de Datos PolicySpace2

Este script demuestra cómo realizar consultas básicas a la base de datos
datawarehouse.db y visualizar los resultados.

Uso:
    python example_query.py
    
Autor: PolicySpace2 España
Fecha: 2025
"""

import sqlite3
import pandas as pd
from pathlib import Path

# Configuración
YEARS_TO_DISPLAY = 5  # Número de años a mostrar en ejemplos de evolución
MAX_ROWS_DISPLAY = 10  # Número máximo de filas a mostrar en ejemplos


def connect_database():
    """
    Conecta a la base de datos PolicySpace2.
    
    Returns:
        sqlite3.Connection: Conexión a la base de datos
    """
    script_dir = Path(__file__).parent
    db_path = script_dir / "data base" / "datawarehouse.db"
    
    if not db_path.exists():
        print(f"❌ Error: No se encontró la base de datos en: {db_path}")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        print(f"✅ Conectado a la base de datos: {db_path.name}\n")
        return conn
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        return None


def list_tables(conn):
    """Lista todas las tablas disponibles en la base de datos."""
    print("="*80)
    print("📊 TABLAS DISPONIBLES EN LA BASE DE DATOS")
    print("="*80 + "\n")
    
    query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    tables = pd.read_sql_query(query, conn)
    
    for i, table in enumerate(tables['name'], 1):
        print(f"   {i}. {table}")
    
    print(f"\n   Total: {len(tables)} tablas\n")
    return tables['name'].tolist()


def example_1_top_municipalities(conn):
    """Ejemplo 1: Top 10 municipios más poblados en 2022."""
    print("="*80)
    print("EJEMPLO 1: Top 10 Municipios Más Poblados (2022)")
    print("="*80 + "\n")
    
    query = """
    SELECT 
        e.NOMBRE as Municipio,
        e.CPRO as Provincia,
        CAST(c."2022" AS INTEGER) as Poblacion2022
    FROM cifras_poblacion_municipio c
    JOIN tabla_equivalencias e ON c.mun_code = e.mun_code
    WHERE c."2022" IS NOT NULL
    ORDER BY CAST(c."2022" AS INTEGER) DESC
    LIMIT 10;
    """
    
    df = pd.read_sql_query(query, conn)
    
    print("🏙️  Municipios con mayor población en 2022:\n")
    print(df.to_string(index=False))
    print("\n")


def example_2_population_trend(conn):
    """Ejemplo 2: Evolución de la población total por año."""
    print("="*80)
    print("EJEMPLO 2: Evolución de la Población Total")
    print("="*80 + "\n")
    
    # Obtener columnas de año disponibles
    query = "PRAGMA table_info(estimativas_pop);"
    columns = pd.read_sql_query(query, conn)
    year_columns = [col for col in columns['name'] if col.isdigit()]
    
    if not year_columns:
        print("⚠️  No se encontraron columnas de año en la tabla\n")
        return
    
    # Calcular población total por año (usando primeros N años como ejemplo)
    print(f"📈 Población total en España (primeros {YEARS_TO_DISPLAY} años disponibles):\n")
    
    for year in year_columns[:YEARS_TO_DISPLAY]:
        query = f'SELECT SUM(CAST("{year}" AS INTEGER)) as total FROM estimativas_pop WHERE "{year}" IS NOT NULL;'
        result = pd.read_sql_query(query, conn)
        total = result['total'].iloc[0]
        print(f"   {year}: {total:>15,} habitantes")
    
    print("\n")


def example_3_idhm_statistics(conn):
    """Ejemplo 3: Estadísticas del Índice de Desarrollo Humano Municipal."""
    print("="*80)
    print("EJEMPLO 3: Estadísticas del IDHM")
    print("="*80 + "\n")
    
    query = """
    SELECT 
        year as Año,
        COUNT(*) as NumMunicipios,
        ROUND(AVG(idhm), 4) as IDHMedio,
        ROUND(MIN(idhm), 4) as IDHMinimo,
        ROUND(MAX(idhm), 4) as IDHMaximo
    FROM idhm_indice_desarrollo_humano_municipal
    WHERE idhm IS NOT NULL
    GROUP BY year
    ORDER BY year DESC
    LIMIT 5;
    """
    
    df = pd.read_sql_query(query, conn)
    
    if df.empty:
        print("⚠️  No se encontraron datos de IDHM\n")
        return
    
    print("🏆 Estadísticas del Índice de Desarrollo Humano Municipal:\n")
    print(df.to_string(index=False))
    print("\n")


def example_4_companies_by_activity(conn):
    """Ejemplo 4: Municipios con más empresas."""
    print("="*80)
    print("EJEMPLO 4: Municipios con Más Empresas (Año más reciente)")
    print("="*80 + "\n")
    
    query = """
    SELECT 
        municipio_name as Municipio,
        year as Año,
        CAST(total_empresas AS INTEGER) as TotalEmpresas
    FROM empresas_municipio_actividad_principal
    WHERE total_empresas IS NOT NULL
        AND year = (SELECT MAX(year) FROM empresas_municipio_actividad_principal)
    ORDER BY total_empresas DESC
    LIMIT 10;
    """
    
    df = pd.read_sql_query(query, conn)
    
    if df.empty:
        print("⚠️  No se encontraron datos de empresas\n")
        return
    
    print("🏢 Municipios con mayor número de empresas:\n")
    print(df.to_string(index=False))
    print("\n")


def example_5_mortality_rates(conn):
    """Ejemplo 5: Datos de mortalidad por comunidad autónoma y sexo."""
    print("="*80)
    print("EJEMPLO 5: Muertes por CC.AA. y Sexo (Año más reciente)")
    print("="*80 + "\n")
    
    query = """
    SELECT 
        ccaa_name as ComunidadAutonoma,
        sex as Sexo,
        year as Año,
        SUM(total_muertes) as TotalMuertes
    FROM df_mortalidad_ccaa_sexo
    WHERE year = (SELECT MAX(year) FROM df_mortalidad_ccaa_sexo)
    GROUP BY ccaa_name, sex
    ORDER BY TotalMuertes DESC
    LIMIT 20;
    """
    
    df = pd.read_sql_query(query, conn)
    
    if df.empty:
        print("⚠️  No se encontraron datos de mortalidad\n")
        return
    
    print("⚰️  Total de muertes por comunidad autónoma y sexo:\n")
    print(df.to_string(index=False))
    print("\n")


def custom_query_example(conn):
    """Muestra cómo realizar una consulta personalizada."""
    print("="*80)
    print("EJEMPLO PERSONALIZADO: Crear Tu Propia Consulta")
    print("="*80 + "\n")
    
    example_code = '''
# Ejemplo de código para realizar consultas personalizadas:

import sqlite3
import pandas as pd

# Conectar a la base de datos
conn = sqlite3.connect('data base/datawarehouse.db')

# Tu consulta SQL personalizada (con JOIN para obtener nombres)
query = """
SELECT 
    e.NOMBRE as municipio,
    e.CPRO as provincia,
    c."2020" as poblacion_2020,
    c."2022" as poblacion_2022,
    CAST(c."2022" AS REAL) - CAST(c."2020" AS REAL) as cambio_absoluto,
    ROUND(
        (CAST(c."2022" AS REAL) - CAST(c."2020" AS REAL)) / 
        CAST(c."2020" AS REAL) * 100, 
        2
    ) as cambio_porcentual
FROM cifras_poblacion_municipio c
JOIN tabla_equivalencias e ON c.mun_code = e.mun_code
WHERE c."2020" IS NOT NULL AND c."2022" IS NOT NULL
    AND CAST(c."2020" AS INTEGER) > 100000
ORDER BY cambio_porcentual DESC
LIMIT 10;
"""

# Ejecutar consulta
df = pd.read_sql_query(query, conn)

# Mostrar resultados
print(df)

# Guardar a CSV
df.to_csv('mi_analisis.csv', index=False)

# Cerrar conexión
conn.close()
    '''
    
    print(example_code)
    print("\n")


def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("\n" + "="*80)
    print("🇪🇸 PolicySpace2 España - Ejemplos de Consultas")
    print("="*80 + "\n")
    
    print("Este script demuestra cómo consultar la base de datos PolicySpace2.\n")
    
    # Conectar a la base de datos
    conn = connect_database()
    if not conn:
        return 1
    
    try:
        # Listar todas las tablas
        list_tables(conn)
        
        # Ejecutar ejemplos
        example_1_top_municipalities(conn)
        example_2_population_trend(conn)
        example_3_idhm_statistics(conn)
        example_4_companies_by_activity(conn)
        example_5_mortality_rates(conn)
        
        # Mostrar ejemplo de consulta personalizada
        custom_query_example(conn)
        
        print("="*80)
        print("✅ Ejemplos completados exitosamente")
        print("="*80 + "\n")
        
        print("💡 Consejos:")
        print("   - Modifica estos ejemplos para tus propios análisis")
        print("   - Usa pandas para manipular y visualizar los datos")
        print("   - Consulta la documentación SQL de SQLite para más opciones")
        print("   - Exporta resultados a CSV, Excel o JSON según necesites\n")
        
    finally:
        conn.close()
        print("🔌 Conexión cerrada\n")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
