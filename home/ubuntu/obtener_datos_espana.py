#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal para obtener datos españoles equivalentes a los utilizados en PolicySpace2.
Este script utiliza los módulos ine_api.py y databank_api.py para conectar con las APIs
y obtener los datos necesarios.
"""

import os
import pandas as pd
from ine_api import INE_API
from databank_api import DataBankAPI
import requests
import zipfile
import io

def crear_directorio_salida():
    """
    Crea el directorio de salida para los datos.
    
    Returns:
        str: Ruta del directorio de salida.
    """
    output_dir = "datos_espana"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def descargar_datos_adicionales():
    """
    Descarga datos adicionales que no están disponibles a través de las APIs.
    """
    output_dir = crear_directorio_salida()
    
    # Datos de matrimonio por edad
    print("Descargando datos de matrimonio por edad...")
    try:
        # URL de ejemplo, habría que ajustar a la URL correcta
        url = "https://www.ine.es/jaxi/files/tpx/es/csv_bd/50771.csv"
        response = requests.get(url)
        
        if response.status_code == 200:
            # Procesar los datos
            content = response.content.decode('utf-8')
            
            # Guardar el archivo
            output_file = os.path.join(output_dir, "matrimonio_edad_espana.csv")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Datos de matrimonio guardados en {output_file}")
        else:
            print(f"Error al descargar datos de matrimonio: {response.status_code}")
    except Exception as e:
        print(f"Error al descargar datos de matrimonio: {e}")
    
    # Datos de calificación/educación por municipio
    print("\nDescargando datos de educación por municipio...")
    try:
        # URL de ejemplo, habría que ajustar a la URL correcta
        url = "https://www.ine.es/jaxi/files/tpx/es/csv_bd/50321.csv"
        response = requests.get(url)
        
        if response.status_code == 200:
            # Procesar los datos
            content = response.content.decode('utf-8')
            
            # Guardar el archivo
            output_file = os.path.join(output_dir, "educacion_municipios_espana.csv")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Datos de educación guardados en {output_file}")
        else:
            print(f"Error al descargar datos de educación: {response.status_code}")
    except Exception as e:
        print(f"Error al descargar datos de educación: {e}")

def generar_csv_equivalencias():
    """
    Genera un CSV con las equivalencias entre los archivos originales de PolicySpace2
    y los nuevos archivos con datos españoles.
    
    Returns:
        pandas.DataFrame: DataFrame con las equivalencias.
    """
    output_dir = crear_directorio_salida()
    
    # Crear lista de equivalencias
    equivalencias = [
        {"archivo_original": "ACPs_BR.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Códigos de comunidades autónomas y provincias"},
        {"archivo_original": "ACPs_MUN_CODES.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Códigos de municipios"},
        {"archivo_original": "RM_BR_STATES.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Relación de municipios por provincias"},
        {"archivo_original": "STATES_ID_NUM.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Códigos numéricos de provincias y municipios"},
        {"archivo_original": "average_num_members_families_2010.csv", "archivo_espana": "tamano_hogares_municipio.csv", "fuente": "INE API", "descripcion": "Tamaño medio de los hogares por municipio"},
        {"archivo_original": "estimativas_pop.csv", "archivo_espana": "poblacion_municipio_sexo_edad_2021.csv", "fuente": "INE API", "descripcion": "Cifras de población por municipios"},
        {"archivo_original": "firms_by_APs2000_t0_full.csv", "archivo_espana": "empresas_por_municipio.csv", "fuente": "INE API", "descripcion": "Empresas por municipio"},
        {"archivo_original": "firms_by_APs2000_t1_full.csv", "archivo_espana": "empresas_por_municipio.csv", "fuente": "INE API", "descripcion": "Empresas por municipio"},
        {"archivo_original": "firms_by_APs2010_t0_full.csv", "archivo_espana": "empresas_por_municipio.csv", "fuente": "INE API", "descripcion": "Empresas por municipio"},
        {"archivo_original": "firms_by_APs2010_t1_full.csv", "archivo_espana": "empresas_por_municipio.csv", "fuente": "INE API", "descripcion": "Empresas por municipio"},
        {"archivo_original": "idhm_2000_2010.csv", "archivo_espana": "indicador_desarrollo_espana.csv", "fuente": "DataBank API", "descripcion": "Indicadores de desarrollo humano"},
        {"archivo_original": "interest_fixed.csv", "archivo_espana": "tasas_interes_espana.csv", "fuente": "DataBank API", "descripcion": "Tipos de interés"},
        {"archivo_original": "interest_nominal.csv", "archivo_espana": "tasas_interes_espana.csv", "fuente": "DataBank API", "descripcion": "Tipos de interés nominales"},
        {"archivo_original": "interest_real.csv", "archivo_espana": "tasas_interes_espana.csv", "fuente": "DataBank API", "descripcion": "Tipos de interés reales"},
        {"archivo_original": "marriage_age_men.csv", "archivo_espana": "matrimonio_edad_espana.csv", "fuente": "INE Web", "descripcion": "Edad media al matrimonio por sexo"},
        {"archivo_original": "marriage_age_men_original.csv", "archivo_espana": "matrimonio_edad_espana.csv", "fuente": "INE Web", "descripcion": "Edad media al matrimonio por sexo"},
        {"archivo_original": "marriage_age_women.csv", "archivo_espana": "matrimonio_edad_espana.csv", "fuente": "INE Web", "descripcion": "Edad media al matrimonio por sexo"},
        {"archivo_original": "marriage_age_women_original.csv", "archivo_espana": "matrimonio_edad_espana.csv", "fuente": "INE Web", "descripcion": "Edad media al matrimonio por sexo"},
        {"archivo_original": "names_and_codes_municipalities.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Relación de municipios y sus códigos"},
        {"archivo_original": "num_people_age_gender_AP_2000.csv", "archivo_espana": "poblacion_municipio_sexo_edad_2021.csv", "fuente": "INE API", "descripcion": "Población por sexo, edad y municipio"},
        {"archivo_original": "num_people_age_gender_AP_2010.csv", "archivo_espana": "poblacion_municipio_sexo_edad_2021.csv", "fuente": "INE API", "descripcion": "Población por sexo, edad y municipio"},
        {"archivo_original": "pop_men_2000.csv", "archivo_espana": "poblacion_hombres_2021.csv", "fuente": "INE API", "descripcion": "Población masculina por edad y municipio"},
        {"archivo_original": "pop_men_2010.csv", "archivo_espana": "poblacion_hombres_2021.csv", "fuente": "INE API", "descripcion": "Población masculina por edad y municipio"},
        {"archivo_original": "pop_women_2000.csv", "archivo_espana": "poblacion_mujeres_2021.csv", "fuente": "INE API", "descripcion": "Población femenina por edad y municipio"},
        {"archivo_original": "pop_women_2010.csv", "archivo_espana": "poblacion_mujeres_2021.csv", "fuente": "INE API", "descripcion": "Población femenina por edad y municipio"},
        {"archivo_original": "prop_urban_2000_2010.csv", "archivo_espana": "proporcion_urbana_municipios.csv", "fuente": "INE API", "descripcion": "Proporción de población urbana por municipio"},
        {"archivo_original": "qualification_APs_2000.csv", "archivo_espana": "educacion_municipios_espana.csv", "fuente": "INE Web", "descripcion": "Nivel de formación por municipio"},
        {"archivo_original": "qualification_APs_2010.csv", "archivo_espana": "educacion_municipios_espana.csv", "fuente": "INE Web", "descripcion": "Nivel de formación por municipio"},
        {"archivo_original": "single_aps_2000.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Códigos de municipios"},
        {"archivo_original": "single_aps_2010.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Códigos de municipios"}
    ]
    
    # Añadir equivalencias para los archivos de fertilidad y mortalidad
    for estado in ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]:
        equivalencias.append({
            "archivo_original": f"fertility_{estado}.csv",
            "archivo_espana": "fertilidad_ccaa_espana.csv",
            "fuente": "INE API",
            "descripcion": "Indicadores de fecundidad por comunidades autónomas"
        })
        equivalencias.append({
            "archivo_original": f"mortality_men_{estado}.csv",
            "archivo_espana": "mortalidad_hombres_ccaa_espana.csv",
            "fuente": "INE API",
            "descripcion": "Indicadores de mortalidad masculina por comunidades autónomas"
        })
        equivalencias.append({
            "archivo_original": f"mortality_women_{estado}.csv",
            "archivo_espana": "mortalidad_mujeres_ccaa_espana.csv",
            "fuente": "INE API",
            "descripcion": "Indicadores de mortalidad femenina por comunidades autónomas"
        })
    
    # Añadir equivalencias para los archivos de FPM (Fondo de Participación de los Municipios)
    for estado in ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]:
        equivalencias.append({
            "archivo_original": f"{estado}.csv",
            "archivo_espana": "financiacion_municipios_espana.csv",
            "fuente": "Ministerio de Hacienda",
            "descripcion": "Datos de financiación municipal"
        })
    
    # Crear DataFrame
    df = pd.DataFrame(equivalencias)
    
    # Guardar en CSV
    output_file = os.path.join(output_dir, "equivalencias_archivos.csv")
    df.to_csv(output_file, index=False)
    
    print(f"CSV de equivalencias guardado en {output_file}")
    return df

def main():
    """
    Función principal que ejecuta todo el proceso de obtención de datos.
    """
    print("Iniciando proceso de obtención de datos españoles para PolicySpace2...")
    
    # Crear directorio de salida
    output_dir = crear_directorio_salida()
    
    # Obtener datos del INE
    print("\n=== Obteniendo datos del INE ===")
    ine = INE_API()
    
    print("\nObteniendo datos de municipios...")
    municipalities = ine.get_municipalities()
    
    print("\nObteniendo datos de población...")
    population = ine.get_population_data(2021)
    
    print("\nObteniendo datos de proporción urbana...")
    urban = ine.get_urban_proportion()
    
    print("\nObteniendo datos de empresas...")
    firms = ine.get_firms_by_municipality()
    
    # Obtener datos de DataBank
    print("\n=== Obteniendo datos de DataBank ===")
    databank = DataBankAPI()
    
    print("\nObteniendo datos del PIB...")
    gdp = databank.get_gdp_data()
    
    print("\nObteniendo datos del PIB per cápita...")
    gdp_per_capita = databank.get_gdp_per_capita_data()
    
    print("\nObteniendo datos de desarrollo humano...")
    hdi = databank.get_hdi_data()
    
    print("\nObteniendo datos de tasas de interés...")
    interest = databank.get_interest_rates()
    
    # Descargar datos adicionales
    print("\n=== Descargando datos adicionales ===")
    descargar_datos_adicionales()
    
    # Generar CSV de equivalencias
    print("\n=== Generando CSV de equivalencias ===")
    equivalencias = generar_csv_equivalencias()
    
    print("\nProceso completado. Todos los datos han sido guardados en el directorio:", output_dir)
    print("Se ha generado un CSV con las equivalencias entre los archivos originales y los nuevos archivos.")

if __name__ == "__main__":
    main()
