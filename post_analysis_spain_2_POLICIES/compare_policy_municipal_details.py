import pandas as pd
import matplotlib.pyplot as plt
import os
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Escenarios de políticas (igual que en generate_policy_comparison_plots.py)
SCENARIOS = {
    "All_Policies_C0": {
        "path": "output/run__2025-05-30T16_54_46.264128",
        "label": "Pol:All (C0)", # Etiqueta más corta para leyendas
    },
    "No_Policies_C0": {
        "path": "output/run__2025-05-30T17_37_24.169144",
        "label": "Pol:None (C0)",
    },
    "Buy_Policy_C0": {
        "path": "output/run__2025-05-30T17_50_16.386729",
        "label": "Pol:Buy (C0)",
    },
    "Wage_Policy_C0": {
        "path": "output/run__2025-05-30T18_18_46.032642",
        "label": "Pol:Wage (C0)",
    }
}

# Directorios de salida
BASE_OUTPUT_DIR = "post_analysis/post_analysis_spain_2_POLICIES"
POLICY_MUN_PLOTS_DIR = os.path.join(BASE_OUTPUT_DIR, "policy_mun_plots")
POLICY_MUN_TABLES_DIR = os.path.join(BASE_OUTPUT_DIR, "policy_mun_tables")

# Columnas de temp_regional.csv
REGIONAL_COL_NAMES = [
    'month', 'mun_id', 'commuting', 'pop', 'gdp_region', 
    'regional_gini', 'regional_house_values', 'regional_unemployment', 
    'qli_index', 'gdp_percapita', 'treasure', 'equally', 'locally', 'pie', 
    'licenses'
]

# Archivo de equivalencias para nombres de municipios
MUN_NAMES_CSV_PATH = os.path.join('ETL', 'tabla_equivalencias', 'data', 'df_equivalencias_municipio_CORRECTO.csv')

def get_municipality_name_map():
    """Carga el mapeo de mun_id a nombre de municipio."""
    try:
        df_nombres = pd.read_csv(MUN_NAMES_CSV_PATH, dtype={'CPRO': str, 'CMUN': str})
        df_nombres['CMUN_FULL'] = df_nombres['CPRO'].str.zfill(2) + df_nombres['CMUN'].str.zfill(3)
        return pd.Series(df_nombres.NOMBRE.values, index=df_nombres.CMUN_FULL).to_dict()
    except Exception as e:
        logging.error(f"No se pudo cargar el mapeo de nombres de municipios: {e}")
        return {}

MUN_NAME_MAP = get_municipality_name_map()

def load_regional_data_for_scenario(scenario_path):
    """Carga temp_regional.csv para un escenario."""
    file_path = os.path.join(scenario_path, "avg", "temp_regional.csv")
    if not os.path.exists(file_path):
        logging.warning(f"Archivo no encontrado: {file_path}")
        return None
    try:
        df = pd.read_csv(file_path, sep=";", header=None, names=REGIONAL_COL_NAMES, decimal='.')
        if 'month' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['month']):
            df['month'] = pd.to_datetime(df['month'])
        df['mun_id'] = df['mun_id'].astype(str).str.zfill(5) # Asegurar formato de 5 dígitos
        return df
    except Exception as e:
        logging.error(f"Error cargando {file_path}: {e}")
        return None

def main():
    os.makedirs(POLICY_MUN_PLOTS_DIR, exist_ok=True)
    os.makedirs(POLICY_MUN_TABLES_DIR, exist_ok=True)

    logging.info("ADVERTENCIA IMPORTANTE: Los archivos conf.json de las ejecuciones analizadas indican POLICY_COEFFICIENT = 0.")
    logging.info("Esto significa que las políticas listadas probablemente no tuvieron un impacto económico real.")
    logging.info("Las diferencias observadas podrían deberse a la variabilidad de la simulación y no a las políticas.")

    # Cargar todos los datos regionales primero
    all_regional_data = {}
    municipalities_to_process = set()

    for scenario_key, details in SCENARIOS.items():
        logging.info(f"Cargando datos para escenario: {details['label']} desde {details['path']}")
        df_regional = load_regional_data_for_scenario(details["path"])
        all_regional_data[scenario_key] = df_regional
        if df_regional is not None:
            municipalities_to_process.update(df_regional['mun_id'].unique())
    
    if not municipalities_to_process:
        logging.error("No se encontraron municipios en los datos. Terminando.")
        return

    logging.info(f"Municipios encontrados en los datos: {sorted(list(municipalities_to_process))}")

    metrics_to_compare = [
        'regional_gini', 'regional_unemployment', 'qli_index', 
        'regional_house_values', 'pop', 'licenses', 'gdp_percapita', 'commuting'
    ]

    for metric in metrics_to_compare:
        plt.figure(figsize=(15, 8))
        combined_data_for_metric = []

        for scenario_key, details in SCENARIOS.items():
            df_scenario_regional = all_regional_data[scenario_key]
            if df_scenario_regional is None:
                continue

            for mun_id in sorted(list(municipalities_to_process)):
                df_mun = df_scenario_regional[df_scenario_regional['mun_id'] == mun_id]
                if not df_mun.empty and metric in df_mun.columns:
                    mun_name = MUN_NAME_MAP.get(mun_id, mun_id)
                    label = f"{mun_name} - {details['label']}"
                    plt.plot(df_mun['month'], df_mun[metric], label=label, alpha=0.8)
                    
                    # Para la tabla CSV
                    df_table_part = df_mun[['month', metric]].copy()
                    df_table_part['municipality_id'] = mun_id
                    df_table_part['municipality_name'] = mun_name
                    df_table_part['policy_scenario'] = details['label']
                    df_table_part.rename(columns={metric: 'metric_value'}, inplace=True)
                    df_table_part['metric_name'] = metric
                    combined_data_for_metric.append(df_table_part)

        plt.xlabel("Fecha")
        plt.ylabel(metric.replace('_', ' ').title())
        plt.title(f"Comparación Municipal de {metric.replace('_', ' ').title()} por Escenario de Política")
        
        # Ajustar leyenda para que no sea demasiado grande
        handles, labels = plt.gca().get_legend_handles_labels()
        if len(labels) > 10: # Si hay muchas líneas, colocar la leyenda fuera
            plt.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')
            plt.tight_layout(rect=[0, 0, 0.85, 1]) # Ajustar para dar espacio a la leyenda
        else:
            plt.legend(loc='best', fontsize='small')
            plt.tight_layout()

        plt.grid(True, linestyle='--', alpha=0.7)
        plot_filename = f"comparison_municipal_{metric}.png"
        plt.savefig(os.path.join(POLICY_MUN_PLOTS_DIR, plot_filename))
        plt.close()
        logging.info(f"Gráfico comparativo municipal guardado: {plot_filename}")

        # Guardar tabla combinada para la métrica actual
        if combined_data_for_metric:
            df_combined_metric_table = pd.concat(combined_data_for_metric, ignore_index=True)
            table_filename = f"table_municipal_{metric}.csv"
            df_combined_metric_table.to_csv(os.path.join(POLICY_MUN_TABLES_DIR, table_filename), index=False, sep=';', decimal=',')
            logging.info(f"Tabla comparativa municipal guardada: {table_filename}")

    logging.info("Proceso de comparación municipal detallada completado.")
    logging.info(f"Los gráficos se han guardado en: {POLICY_MUN_PLOTS_DIR}")
    logging.info(f"Las tablas se han guardado en: {POLICY_MUN_TABLES_DIR}")

if __name__ == "__main__":
    main()
