import subprocess

def run_script(path):
    print(f"Ejecutando: {path}")
    result = subprocess.run(["python", path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

if __name__ == "__main__":
    # 1. Descargar archivos originales
    run_script("./PIE/scrap_liquidaciones.py")
    # 2. Seleccionar, convertir y renombrar archivos homogéneos
    run_script("./PIE/select_liquidaciones_regimen_general.py")
    # 3. (Opcional) Verificar cobertura anual
    run_script("./PIE/count_liquidaciones_by_year.py")
    # 4. Procesar y unificar datos finales
    run_script("./PIE/procesar_liquidacion_pie_final.py")
