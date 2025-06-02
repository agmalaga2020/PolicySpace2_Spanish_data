import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TABLE_PATH = os.path.join("post_analysis", "post_analysis_spain_2_POLICIES", "policy_mun_tables", "table_municipal_regional_house_values.csv")

def analyze_house_values():
    if not os.path.exists(TABLE_PATH):
        logging.error(f"Archivo no encontrado: {TABLE_PATH}")
        return

    try:
        # Leer el CSV, especificando el delimitador y el separador decimal
        df = pd.read_csv(TABLE_PATH, sep=';', decimal=',')
        logging.info(f"Archivo CSV cargado. Columnas: {df.columns.tolist()}")

        # Asegurarse de que 'month' es datetime y 'metric_value' es numérico
        df['month'] = pd.to_datetime(df['month'])
        if 'metric_value' not in df.columns:
            logging.error("La columna 'metric_value' no se encuentra en el CSV.")
            return
            
        # df['metric_value'] ya debería ser numérico debido a decimal=','
        # pero verificamos por si acaso hay algún problema de carga.
        if not pd.api.types.is_numeric_dtype(df['metric_value']):
             logging.warning("La columna 'metric_value' no es numérica. Intentando convertir...")
             df['metric_value'] = pd.to_numeric(df['metric_value'], errors='coerce')


        # Agrupar por escenario de política y municipio
        # Obtener el último valor (valor final) y el valor promedio
        
        summary_list = []

        for group_name, group_df in df.groupby(['policy_scenario', 'municipality_name', 'municipality_id']):
            policy_scenario, mun_name, mun_id = group_name
            
            # Ordenar por fecha para asegurar que el último valor es correcto
            group_df_sorted = group_df.sort_values(by='month')
            
            final_value = group_df_sorted['metric_value'].iloc[-1] if not group_df_sorted.empty else None
            mean_value = group_df_sorted['metric_value'].mean() if not group_df_sorted.empty else None
            
            summary_list.append({
                "Escenario de Política": policy_scenario,
                "ID Municipio": mun_id,
                "Municipio": mun_name,
                "Valor Final Vivienda Regional": final_value,
                "Promedio Valor Vivienda Regional": mean_value
            })
        
        summary_df = pd.DataFrame(summary_list)

        # Ordenar para facilitar la comparación
        summary_df_sorted = summary_df.sort_values(by=['Municipio', 'Escenario de Política'])

        logging.info("\nResumen de Valores Regionales de Vivienda por Política y Municipio:")
        print(summary_df_sorted.to_string())

        # Guardar la tabla resumen
        output_summary_table_path = os.path.join(os.path.dirname(TABLE_PATH), "summary_regional_house_values_by_policy.csv")
        summary_df_sorted.to_csv(output_summary_table_path, index=False, sep=';', decimal=',')
        logging.info(f"\nTabla resumen guardada en: {output_summary_table_path}")
        
        logging.info("\nRECORDATORIO IMPORTANTE: Todas las ejecuciones analizadas tenían POLICY_COEFFICIENT = 0.")
        logging.info("Las diferencias observadas probablemente se deban a la variabilidad inherente de la simulación y no a un efecto real de las políticas.")

    except Exception as e:
        logging.error(f"Ocurrió un error durante el análisis: {e}", exc_info=True)

if __name__ == "__main__":
    analyze_house_values()
