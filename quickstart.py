#!/usr/bin/env python3
"""
Script de Inicio Rápido - PolicySpace2 España

Este script interactivo guía al usuario a través de las primeras acciones
que puede realizar con el proyecto PolicySpace2 España.

Uso:
    python quickstart.py
    
El script verificará:
- Instalación de dependencias
- Estado de la base de datos
- Disponibilidad del dashboard
- Ejemplos de consultas

Autor: PolicySpace2 España
Fecha: 2025
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Imprime un encabezado formateado."""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)


def print_section(text):
    """Imprime un título de sección."""
    print(f"\n{'─'*80}")
    print(f"  {text}")
    print(f"{'─'*80}")


def check_python_version():
    """Verifica la versión de Python."""
    print_section("🐍 Verificando versión de Python")
    
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ❌ Se requiere Python 3.8 o superior")
        return False
    else:
        print("   ✅ Versión de Python compatible")
        return True


def check_dependencies():
    """Verifica si las dependencias están instaladas."""
    print_section("📦 Verificando dependencias")
    
    required_packages = [
        'pandas',
        'sqlalchemy',
        'streamlit',
        'plotly'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (no instalado)")
            missing.append(package)
    
    if missing:
        print(f"\n   ⚠️  Faltan {len(missing)} paquetes")
        print("\n   Para instalarlos, ejecuta:")
        print(f"   pip install {' '.join(missing)}")
        return False
    else:
        print("\n   ✅ Todas las dependencias están instaladas")
        return True


def check_database():
    """Verifica el estado de la base de datos."""
    print_section("💾 Verificando base de datos")
    
    script_dir = Path(__file__).parent
    db_path = script_dir / "data base" / "datawarehouse.db"
    
    if not db_path.exists():
        print(f"   ❌ No se encontró la base de datos en: {db_path}")
        return False
    else:
        size_mb = db_path.stat().st_size / (1024 * 1024)
        print(f"   ✅ Base de datos encontrada")
        print(f"   📊 Tamaño: {size_mb:.2f} MB")
        return True


def run_health_check():
    """Ejecuta el verificador de salud de la base de datos."""
    print_section("🏥 Ejecutando verificación de salud")
    
    print("\n   Ejecutando check_database_health.py...\n")
    
    try:
        result = subprocess.run(
            [sys.executable, "check_database_health.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Mostrar solo las últimas líneas del resultado
        lines = result.stdout.split('\n')
        for line in lines[-15:]:
            if line.strip():
                print(f"   {line}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"   ❌ Error al ejecutar health check: {e}")
        return False


def show_menu():
    """Muestra el menú principal de opciones."""
    print_section("📋 ¿Qué deseas hacer?")
    
    print("""
   1. 🌐 Iniciar dashboard interactivo (Streamlit)
   2. 🔍 Ver ejemplos de consultas SQL
   3. 📊 Ejecutar validación de datos
   4. 📚 Ver documentación del proyecto
   5. 🛠️  Ver herramientas disponibles
   6. 🚪 Salir
    """)
    
    return input("   Selecciona una opción (1-6): ").strip()


def start_dashboard():
    """Inicia el dashboard de Streamlit."""
    print_section("🌐 Iniciando Dashboard Streamlit")
    
    dashboard_path = Path(__file__).parent / "dashboard" / "app.py"
    
    if not dashboard_path.exists():
        print(f"   ❌ No se encontró el archivo del dashboard: {dashboard_path}")
        return
    
    print("\n   El dashboard se abrirá en tu navegador...")
    print("   Presiona Ctrl+C para detenerlo\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(dashboard_path)
        ])
    except KeyboardInterrupt:
        print("\n\n   ✅ Dashboard detenido")
    except Exception as e:
        print(f"   ❌ Error al iniciar dashboard: {e}")


def show_sql_examples():
    """Muestra ejemplos de consultas SQL."""
    print_section("🔍 Ejemplos de Consultas SQL")
    
    examples = """
   Ejemplo 1: Ver tablas disponibles
   ---------------------------------
   SELECT name FROM sqlite_master WHERE type='table';

   Ejemplo 2: Contar municipios
   ----------------------------
   SELECT COUNT(*) as total_municipios 
   FROM cifras_poblacion_municipio;

   Ejemplo 3: Top 10 municipios más poblados (2022)
   ------------------------------------------------
   SELECT municipio_name, "2022" as poblacion_2022
   FROM cifras_poblacion_municipio
   ORDER BY "2022" DESC
   LIMIT 10;

   Ejemplo 4: Evolución poblacional de una provincia
   ------------------------------------------------
   SELECT year, SUM(population) as total_poblacion
   FROM estimativas_pop
   WHERE cpro = '28'  -- Madrid
   GROUP BY year
   ORDER BY year;

   Ejemplo 5: Consulta de IDHM por año
   -----------------------------------
   SELECT mun_code, year, idhm
   FROM idhm_indice_desarrollo_humano_municipal
   WHERE year >= 2015
   ORDER BY idhm DESC
   LIMIT 20;
   
   Para ejecutar estas consultas:
   ------------------------------
   import sqlite3
   import pandas as pd
   
   conn = sqlite3.connect('data base/datawarehouse.db')
   df = pd.read_sql_query("TU_CONSULTA_AQUI", conn)
   print(df)
   conn.close()
    """
    
    print(examples)
    input("\n   Presiona Enter para continuar...")


def run_validation():
    """Ejecuta el script de validación de datos."""
    print_section("📊 Validación de Datos")
    
    print("\n   ¿Qué deseas validar?")
    print("   1. Una tabla específica")
    print("   2. Todas las tablas (puede tardar)")
    
    choice = input("\n   Selecciona una opción (1-2): ").strip()
    
    try:
        if choice == "1":
            table = input("   Nombre de la tabla: ").strip()
            subprocess.run([
                sys.executable, "validate_data.py",
                "--table", table, "--verbose"
            ])
        elif choice == "2":
            print("\n   Validando todas las tablas...\n")
            subprocess.run([
                sys.executable, "validate_data.py", "--verbose"
            ])
        else:
            print("   ❌ Opción no válida")
    except Exception as e:
        print(f"   ❌ Error al ejecutar validación: {e}")


def show_documentation():
    """Muestra enlaces a la documentación."""
    print_section("📚 Documentación del Proyecto")
    
    docs = """
   📖 Archivos de Documentación Disponibles:
   
   • README.md
     Descripción general del proyecto, instalación y uso
     
   • CONTRIBUTING.md
     Guía para contribuir al proyecto
     
   • guia_uso.md
     Guía detallada de uso de scripts y APIs
     
   • fuentes_datos_espanolas.md
     Documentación de fuentes de datos
     
   • equivalencias_detalladas.md
     Mapeo entre datos brasileños y españoles
     
   • dashboard/TODO.md
     Estado del desarrollo del dashboard
   
   📂 Notebooks ETL:
   
   Los notebooks en la carpeta ETL/ documentan cada proceso de 
   limpieza y transformación de datos:
   
   • ETL/estimativas_pop/
   • ETL/df_mortalidad_ccaa_sexo/
   • ETL/empresas_municipio_actividad_principal/
   • ETL/indicadores_fecundidad_municipio_provincias/
   • Y más...
   
   Para leer la documentación, usa:
   • less README.md
   • cat guia_uso.md
   • jupyter notebook (para los notebooks ETL)
    """
    
    print(docs)
    input("\n   Presiona Enter para continuar...")


def show_tools():
    """Muestra las herramientas disponibles."""
    print_section("🛠️  Herramientas Disponibles")
    
    tools = """
   🔧 Scripts Principales:
   
   1. check_database_health.py
      Verifica la integridad y salud de la base de datos
      Uso: python check_database_health.py
   
   2. validate_data.py
      Valida la calidad de los datos en las tablas
      Uso: python validate_data.py [--table NOMBRE] [--verbose]
   
   3. adaptar_policyspace2_espana.py
      Obtiene y actualiza datos desde las APIs
      Uso: python adaptar_policyspace2_espana.py [opciones]
   
   4. pregenerar_mapas_pie.py
      Genera visualizaciones geoespaciales
      Uso: python pregenerar_mapas_pie.py
   
   5. dashboard/app.py
      Dashboard interactivo Streamlit
      Uso: streamlit run dashboard/app.py
   
   📡 Módulos de API:
   
   • ine_api.py - Conecta con la API del INE
   • databank_api.py - Conecta con DataBank del Banco Mundial
   • descargar_documentos_alternativos.py - Descarga datos adicionales
   
   Para más información sobre cada herramienta, consulta guia_uso.md
    """
    
    print(tools)
    input("\n   Presiona Enter para continuar...")


def main():
    """Función principal del script de inicio rápido."""
    print_header("🇪🇸 PolicySpace2 España - Inicio Rápido")
    
    print("""
    Bienvenido al proyecto PolicySpace2 España!
    
    Este script te guiará a través de los primeros pasos
    para trabajar con el proyecto.
    """)
    
    # Verificaciones iniciales
    if not check_python_version():
        print("\n   ⚠️  Por favor, actualiza Python antes de continuar")
        return 1
    
    deps_ok = check_dependencies()
    
    if check_database():
        if deps_ok:
            run_health_check()
    
    if not deps_ok:
        print("\n   ⚠️  Instala las dependencias antes de usar todas las funciones")
        print("   Puedes continuar para ver la documentación")
    
    # Menú interactivo
    while True:
        choice = show_menu()
        
        if choice == "1":
            if not deps_ok:
                print("\n   ❌ Necesitas instalar dependencias primero")
                continue
            start_dashboard()
        elif choice == "2":
            show_sql_examples()
        elif choice == "3":
            if not deps_ok:
                print("\n   ❌ Necesitas instalar dependencias primero")
                continue
            run_validation()
        elif choice == "4":
            show_documentation()
        elif choice == "5":
            show_tools()
        elif choice == "6":
            print("\n   👋 ¡Hasta pronto!")
            break
        else:
            print("\n   ❌ Opción no válida. Por favor, selecciona 1-6")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n   👋 Proceso interrumpido por el usuario")
        sys.exit(0)
