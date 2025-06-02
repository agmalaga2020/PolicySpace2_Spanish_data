import pandas as pd
import matplotlib.pyplot as plt
import os
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define los escenarios de políticas y sus directorios de datos
# Incluye tanto las simulaciones anteriores (Coef=0) como la nueva simulación (Coef=0.8)
SCENARIOS = {
    "All_Policies_C0": { # Coeficiente 0 según conf.json
        "path": "output/run__2025-05-30T16_54_46.264128",
        "label": "Policies: Buy, Rent, Wage (Coef=0)",
        "policies_in_params": "['buy', 'rent', 'wage']" # Según conf.json
    },
    "No_Policies_C0": { # Coeficiente 0 según conf.json
        "path": "output/run__2025-05-30T17_37_24.169144",
        "label": "Policies: None (Coef=0)",
        "policies_in_params": "[]" # Según conf.json
    },
    "Buy_Policy_C0": { # Coeficiente 0 según conf.json
        "path": "output/run__2025-05-30T17_50_16.386729",
        "label": "Policy: Buy (Coef=0)",
        "policies_in_params": "['buy']" # Según conf.json
    },
    "Wage_Policy_C0": { # Coeficiente 0 según conf.json
        "path": "output/run__2025-05-30T18_18_46.032642",
        "label": "Policy: Wage (Coef=0)",
        "policies_in_params": "['wage']" # Según conf.json
    },
    "Wage_Policy_C08": { # Nueva simulación con coeficiente 0.8
        "path": "output/run__2025-05-30T19_28_13.368579",
        "label": "Policy: Wage (Coef=0.8)",
        "policies_in_params": "['wage']" # Esperado según configuración
    }
}

# Directorios de salida para los resultados de esta comparación
BASE_OUTPUT_DIR = "post_analysis/post_analysis_spain_2_POLICIES"
PLOTS_OUTPUT_DIR = os.path.join(BASE_OUTPUT_DIR, "plots")
TABLES_OUTPUT_DIR = os.path.join(BASE_OUTPUT_DIR, "tables")

# Columnas de temp_stats.csv
STATS_COL_NAMES = [
    'month', 'price_index', 'gdp_index', 'gdp_growth', 'unemployment', 
    'average_workers', 'families_median_wealth', 'families_wealth', 
    'families_commuting', 'families_savings', 'families_helped', 
    'amount_subsidised', 'firms_wealth', 'firms_profit', 'gini_index', 
    'average_utility', 'pct_zero_consumption', 'rent_default', 'inflation', 
    'average_qli', 'house_vacancy', 'house_price', 'house_rent', 
    'affordable', 'p_delinquent', 'equally', 'locally', 'pie', 'bank'
]

# Columnas de temp_regional.csv
REGIONAL_COL_NAMES = [
    'month', 'mun_id', 'commuting', 'pop', 'gdp_region', 
    'regional_gini', 'regional_house_values', 'regional_unemployment', 
    'qli_index', 'gdp_percapita', 'treasure', 'equally', 'locally', 'pie', 
    'licenses'
]

def load_data(scenario_path, file_name, col_names):
    """Carga datos de un archivo CSV de un escenario específico."""
    file_path = os.path.join(scenario_path, "avg", file_name)
    if not os.path.exists(file_path):
        logging.warning(f"Archivo no encontrado: {file_path}")
        return None
    try:
        df = pd.read_csv(file_path, sep=";", header=None, names=col_names, decimal='.')
        # Convertir 'month' a datetime si no lo es ya
        if 'month' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['month']):
            try:
                df['month'] = pd.to_datetime(df['month'])
            except Exception as e:
                logging.warning(f"No se pudo convertir 'month' a datetime en {file_path}: {e}")
        return df
    except Exception as e:
        logging.error(f"Error cargando {file_path}: {e}")
        return None

def plot_comparison(metric_name, data_frames, labels, output_dir, y_label=None, title_suffix=""):
    """Genera un gráfico de líneas comparando una métrica entre escenarios."""
    plt.figure(figsize=(12, 7))
    for df, label in zip(data_frames, labels):
        if df is not None and metric_name in df.columns and 'month' in df.columns:
            plt.plot(df['month'], df[metric_name], label=label)
        elif df is not None:
            logging.warning(f"Métrica '{metric_name}' o 'month' no encontrada en el DataFrame para la etiqueta '{label}'.")

    plt.xlabel("Fecha")
    plt.ylabel(y_label if y_label else metric_name.replace('_', ' ').title())
    plt.title(f"Comparación de {metric_name.replace('_', ' ').title()}{title_suffix} entre Escenarios de Políticas")
    plt.legend(loc='best')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plot_filename = f"comparison_{metric_name}{title_suffix.replace(' ', '_')}.png"
    plt.savefig(os.path.join(output_dir, plot_filename))
    plt.close()
    logging.info(f"Gráfico comparativo guardado: {plot_filename}")

def generate_summary_table(metric_name, data_frames, labels, output_dir, title_suffix=""):
    """Genera una tabla CSV resumiendo una métrica (valor final y promedio)."""
    summary_data = []
    for df, label in zip(data_frames, labels):
        if df is not None and metric_name in df.columns:
            final_value = df[metric_name].iloc[-1] if not df.empty else None
            mean_value = df[metric_name].mean() if not df.empty else None
            summary_data.append({"Escenario": label, "Valor Final": final_value, "Valor Promedio": mean_value})
        elif df is not None:
            logging.warning(f"Métrica '{metric_name}' no encontrada en el DataFrame para la etiqueta '{label}' al generar tabla.")
            summary_data.append({"Escenario": label, "Valor Final": "N/A", "Valor Promedio": "N/A"})


    if summary_data:
        df_summary = pd.DataFrame(summary_data)
        table_filename = f"summary_table_{metric_name}{title_suffix.replace(' ', '_')}.csv"
        df_summary.to_csv(os.path.join(output_dir, table_filename), index=False, sep=';', decimal=',')
        logging.info(f"Tabla resumen guardada: {table_filename}")
    else:
        logging.warning(f"No se generó tabla para {metric_name} debido a falta de datos.")


def main():
    os.makedirs(PLOTS_OUTPUT_DIR, exist_ok=True)
    os.makedirs(TABLES_OUTPUT_DIR, exist_ok=True)

    logging.info("ADVERTENCIA IMPORTANTE: Los archivos conf.json de las ejecuciones analizadas indican POLICY_COEFFICIENT = 0.")
    logging.info("Esto significa que las políticas listadas probablemente no tuvieron un impacto económico real.")
    logging.info("Las diferencias observadas podrían deberse a la variabilidad de la simulación y no a las políticas.")

    all_stats_dfs = {}
    all_regional_dfs = {}
    scenario_labels = []

    for scenario_name, details in SCENARIOS.items():
        logging.info(f"Procesando escenario: {details['label']} desde {details['path']}")
        
        # Verificar parámetros de la ejecución actual
        conf_file_path = os.path.join(details['path'], "conf.json")
        try:
            with open(conf_file_path, 'r') as f:
                conf_data = json.load(f)
            actual_policies = conf_data.get("PARAMS", {}).get("POLICIES", "No especificado")
            actual_coeff = conf_data.get("PARAMS", {}).get("POLICY_COEFFICIENT", "No especificado")
            logging.info(f"  Parámetros en conf.json -> POLICIES: {actual_policies}, POLICY_COEFFICIENT: {actual_coeff}")
            if str(actual_coeff) != "0": # Comparar como string por si acaso
                 logging.warning(f"  ¡ATENCIÓN! POLICY_COEFFICIENT en {conf_file_path} NO es 0, es {actual_coeff}. Esto contradice la revisión inicial.")
        except Exception as e:
            logging.error(f"  No se pudo leer o parsear {conf_file_path}: {e}")


        stats_df = load_data(details["path"], "temp_stats.csv", STATS_COL_NAMES)
        regional_df = load_data(details["path"], "temp_regional.csv", REGIONAL_COL_NAMES)
        
        all_stats_dfs[scenario_name] = stats_df
        all_regional_dfs[scenario_name] = regional_df
        scenario_labels.append(details["label"])

    # Métricas globales a comparar de temp_stats.csv
    global_metrics_to_plot = [
        "unemployment", "gini_index", "average_qli", "house_price", 
        "house_rent", "families_median_wealth", "amount_subsidised"
    ]
    for metric in global_metrics_to_plot:
        dfs_to_plot = [all_stats_dfs[name] for name in SCENARIOS.keys()]
        plot_comparison(metric, dfs_to_plot, scenario_labels, PLOTS_OUTPUT_DIR)
        generate_summary_table(metric, dfs_to_plot, scenario_labels, TABLES_OUTPUT_DIR)

    # Métricas regionales a comparar (promedio sobre todos los municipios)
    # Se podrían agregar más o hacer por municipio si fuera necesario
    regional_metrics_to_plot = [
        "regional_gini", "regional_unemployment", "qli_index", 
        "regional_house_values", "pop", "licenses"
    ]
    for metric in regional_metrics_to_plot:
        dfs_to_plot_regional_avg = []
        for scenario_name in SCENARIOS.keys():
            df_regional = all_regional_dfs[scenario_name]
            if df_regional is not None and metric in df_regional.columns:
                # Agrupar por mes y calcular la media de la métrica para ese mes
                # Asegurarse de que 'month' es datetime
                if not pd.api.types.is_datetime64_any_dtype(df_regional['month']):
                     df_regional['month'] = pd.to_datetime(df_regional['month'])
                
                # Convertir la métrica a numérico antes de promediar, si no lo es
                if not pd.api.types.is_numeric_dtype(df_regional[metric]):
                    df_regional[metric] = pd.to_numeric(df_regional[metric], errors='coerce')

                df_avg = df_regional.groupby('month')[metric].mean().reset_index()
                dfs_to_plot_regional_avg.append(df_avg)
            else:
                dfs_to_plot_regional_avg.append(None) # Mantener el orden si faltan datos
        
        plot_comparison(metric, dfs_to_plot_regional_avg, scenario_labels, PLOTS_OUTPUT_DIR, title_suffix=" (Promedio Regional)")
        generate_summary_table(metric, dfs_to_plot_regional_avg, scenario_labels, TABLES_OUTPUT_DIR, title_suffix=" (Promedio Regional)")

    logging.info("Proceso de comparación de políticas completado.")
    logging.info(f"Los gráficos comparativos se han guardado en: {PLOTS_OUTPUT_DIR}")
    logging.info(f"Las tablas resumen se han guardado en: {TABLES_OUTPUT_DIR}")

if __name__ == "__main__":
    main()
