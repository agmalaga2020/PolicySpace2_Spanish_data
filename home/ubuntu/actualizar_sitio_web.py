import pandas as pd
import sys
import os
from datetime import datetime

# Configuración de directorios
OUTPUT_DIR = "datos_espana"

def crear_estructura_directorios():
    """
    Crea la estructura de directorios necesaria para almacenar los datos
    """
    directorios = [
        OUTPUT_DIR,
        f"{OUTPUT_DIR}/demograficos",
        f"{OUTPUT_DIR}/economicos",
        f"{OUTPUT_DIR}/geograficos",
        f"{OUTPUT_DIR}/educativos"
    ]
    
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)
        print(f"Directorio creado: {directorio}")

def cargar_equivalencias(csv_path):
    """
    Carga el archivo CSV de equivalencias
    
    Args:
        csv_path (str): Ruta al archivo CSV de equivalencias
        
    Returns:
        pd.DataFrame: DataFrame con las equivalencias
    """
    try:
        df = pd.read_csv(csv_path)
        print(f"Archivo de equivalencias cargado: {csv_path}")
        print(f"Total de documentos: {len(df)}")
        return df
    except Exception as e:
        print(f"Error al cargar el archivo de equivalencias: {e}")
        return None

def generar_informe_equivalencias(df, output_path):
    """
    Genera un informe HTML con las equivalencias
    
    Args:
        df (pd.DataFrame): DataFrame con las equivalencias
        output_path (str): Ruta de salida para el informe HTML
    """
    try:
        # Agrupar por fuente española
        fuentes = df['fuente_espanola'].value_counts().reset_index()
        fuentes.columns = ['Fuente', 'Cantidad']
        
        # Crear HTML
        html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Equivalencias de Datos España-Brasil</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333; }
                h1, h2, h3 { color: #2c3e50; }
                .container { max-width: 1200px; margin: 0 auto; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f2f2f2; }
                tr:hover { background-color: #f5f5f5; }
                .summary { background-color: #eef; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                .category { background-color: #e7f4e4; padding: 10px; margin-top: 20px; border-radius: 5px; }
                .btn { display: inline-block; padding: 8px 16px; background-color: #3498db; color: white; 
                       text-decoration: none; border-radius: 4px; margin-right: 10px; margin-bottom: 10px; }
                .btn:hover { background-color: #2980b9; }
                .timestamp { font-size: 0.8em; color: #777; margin-top: 30px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Equivalencias de Datos entre Brasil y España para PolicySpace2</h1>
                
                <div class="summary">
                    <h2>Resumen</h2>
                    <p>Total de documentos: """ + str(len(df)) + """</p>
                    <p>Fuentes de datos españolas utilizadas: """ + str(len(fuentes)) + """</p>
                </div>
                
                <h2>Fuentes de Datos</h2>
                <table>
                    <tr>
                        <th>Fuente</th>
                        <th>Cantidad de Documentos</th>
                    </tr>
        """
        
        for _, row in fuentes.iterrows():
            html += f"""
                    <tr>
                        <td>{row['Fuente']}</td>
                        <td>{row['Cantidad']}</td>
                    </tr>
            """
        
        html += """
                </table>
                
                <h2>Categorías de Datos</h2>
        """
        
        # Categorías de datos
        categorias = {
            "Geográficos y Administrativos": ["ACPs_BR.csv", "ACPs_MUN_CODES.csv", "RM_BR_STATES.csv", "STATES_ID_NUM.csv", 
                                             "names_and_codes_municipalities.csv", "single_aps_2000.csv", "single_aps_2010.csv"],
            "Demográficos - Población": ["estimativas_pop.csv", "pop_men_2000.csv", "pop_men_2010.csv", "pop_women_2000.csv", 
                                        "pop_women_2010.csv", "num_people_age_gender_AP_2000.csv", "num_people_age_gender_AP_2010.csv",
                                        "average_num_members_families_2010.csv", "prop_urban_2000_2010.csv"],
            "Demográficos - Fertilidad": [doc for doc in df['documento'] if doc.startswith("fertility_")],
            "Demográficos - Mortalidad": [doc for doc in df['documento'] if doc.startswith("mortality_")],
            "Demográficos - Matrimonio": ["marriage_age_men.csv", "marriage_age_men_original.csv", 
                                         "marriage_age_women.csv", "marriage_age_women_original.csv"],
            "Económicos - Empresas": ["firms_by_APs2000_t0_full.csv", "firms_by_APs2000_t1_full.csv", 
                                     "firms_by_APs2010_t0_full.csv", "firms_by_APs2010_t1_full.csv"],
            "Económicos - Financiación Municipal": [doc for doc in df['documento'] if len(doc) == 6 and doc.endswith(".csv")],
            "Económicos - Indicadores": ["interest_fixed.csv", "interest_nominal.csv", "interest_real.csv", "idhm_2000_2010.csv"],
            "Educativos": ["qualification_APs_2000.csv", "qualification_APs_2010.csv"]
        }
        
        for categoria, documentos in categorias.items():
            df_categoria = df[df['documento'].isin(documentos)]
            
            html += f"""
                <div class="category">
                    <h3>{categoria}</h3>
                    <p>Documentos: {len(df_categoria)}</p>
                    <table>
                        <tr>
                            <th>Documento Original (Brasil)</th>
                            <th>Equivalente Español</th>
                            <th>Fuente Española</th>
                            <th>URL/API</th>
                        </tr>
            """
            
            for _, row in df_categoria.iterrows():
                html += f"""
                        <tr>
                            <td>{row['documento']}</td>
                            <td>{row['equivalente_espanol']}</td>
                            <td>{row['fuente_espanola']}</td>
                            <td><a href="{row['url_api']}" target="_blank">Enlace</a></td>
                        </tr>
                """
            
            html += """
                    </table>
                </div>
            """
        
        html += f"""
                <h2>Descargar Datos</h2>
                <p>Puede descargar los siguientes archivos:</p>
                <a href="downloads/equivalencias_datos_espana.csv" class="btn">CSV de Equivalencias</a>
                <a href="downloads/ine_api_actualizado.py" class="btn">Código Python para API INE</a>
                <a href="downloads/scripts_policyspace2_espana.zip" class="btn">Scripts Completos</a>
                
                <div class="timestamp">
                    <p>Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Informe HTML generado: {output_path}")
        return True
    except Exception as e:
        print(f"Error al generar el informe HTML: {e}")
        return False

def main():
    """
    Función principal
    """
    print("Iniciando actualización del sitio web con información completa...")
    
    # Crear estructura de directorios
    crear_estructura_directorios()
    
    # Cargar equivalencias
    equivalencias_csv = "equivalencias_datos_espana.csv"
    df_equivalencias = cargar_equivalencias(equivalencias_csv)
    
    if df_equivalencias is None:
        print("No se pudo cargar el archivo de equivalencias. Abortando.")
        return
    
    # Generar informe HTML
    html_output = "policyspace2-web/public/index.html"
    if generar_informe_equivalencias(df_equivalencias, html_output):
        print(f"Sitio web actualizado correctamente: {html_output}")
    else:
        print("Error al actualizar el sitio web.")
    
    # Copiar archivos necesarios
    os.makedirs("policyspace2-web/public/downloads", exist_ok=True)
    os.system(f"cp {equivalencias_csv} policyspace2-web/public/downloads/")
    os.system("cp ine_api_actualizado.py policyspace2-web/public/downloads/")
    
    print("Proceso completado.")

if __name__ == "__main__":
    main()
