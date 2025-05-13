import subprocess
import sqlite3
import pandas as pd
import os

# --- Configuración ---
start_year_default = 2007
end_year_default = 2022
explorar_script_path = "dashboard/pages/exp/mapa_pie_anual/explorar_pie.py"
generar_script_path = "dashboard/pages/exp/mapa_pie_anual/generar_mapa_pie.py"
db_path = 'data base/datawarehouse.db' # Para obtener los años disponibles dinámicamente

def get_available_years_from_db(db_file):
    """Consulta la base de datos para obtener los años únicos en la tabla PIE."""
    try:
        conn = sqlite3.connect(db_file)
        df_years = pd.read_sql_query("SELECT DISTINCT year FROM PIE ORDER BY year", conn)
        conn.close()
        if not df_years.empty:
            return df_years['year'].tolist()
    except Exception as e:
        print(f"Error al leer años de la base de datos: {e}")
    return None

def run_script(script_path, year):
    """Ejecuta un script Python con un año como argumento."""
    try:
        print(f"\n--- Ejecutando {os.path.basename(script_path)} para el año {year} ---")
        # Usar python3 explícitamente puede ser más robusto en algunos sistemas
        result = subprocess.run(["python3", script_path, str(year)], capture_output=True, text=True, check=True)
        print(f"Salida de {os.path.basename(script_path)} para {year}:\n{result.stdout}")
        if result.stderr:
            print(f"Errores (stderr) de {os.path.basename(script_path)} para {year}:\n{result.stderr}")
        print(f"--- {os.path.basename(script_path)} para el año {year} completado ---")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {os.path.basename(script_path)} para el año {year}:")
        print(f"Código de retorno: {e.returncode}")
        print(f"Salida (stdout):\n{e.stdout}")
        print(f"Error (stderr):\n{e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Error: El intérprete 'python3' o el script '{script_path}' no fue encontrado.")
        return False


if __name__ == "__main__":
    print("Iniciando pregeneración de mapas PIE por año...")
    
    available_years = get_available_years_from_db(db_path)
    
    if available_years:
        print(f"Años detectados en la base de datos para PIE: {available_years}")
        years_to_process = available_years
    else:
        print(f"No se pudieron obtener años de la BD, usando rango por defecto: {start_year_default}-{end_year_default}")
        years_to_process = range(start_year_default, end_year_default + 1)

    for year in years_to_process:
        print(f"\n===== Procesando Año: {year} =====")
        
        # 1. Ejecutar explorar_pie.py para generar el CSV de datos del año
        if not run_script(explorar_script_path, year):
            print(f"Fallo al generar datos CSV para {year}. Saltando generación de mapa para este año.")
            continue # Saltar al siguiente año si falla la extracción de datos

        # 2. Ejecutar generar_mapa_pie.py para generar el HTML del mapa del año
        if not run_script(generar_script_path, year):
            print(f"Fallo al generar mapa HTML para {year}.")
            # Continuar con el siguiente año incluso si este falla, para intentar generar los demás
            
    print("\n===== Pregeneración de todos los mapas completada. =====")
