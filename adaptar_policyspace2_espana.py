#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal para adaptar PolicySpace2 al contexto español.
Este script integra todos los módulos desarrollados para obtener datos españoles
equivalentes a los utilizados en el proyecto original.
"""

import os
import pandas as pd
import argparse
import sys
from datetime import datetime

# Importar los módulos desarrollados
try:
    from ine_api import INE_API
    from databank_api import DataBankAPI
    import descargar_documentos_alternativos
except ImportError:
    print("Error: No se pudieron importar los módulos necesarios.")
    print("Asegúrate de que los archivos ine_api.py, databank_api.py y descargar_documentos_alternativos.py están en el mismo directorio.")
    sys.exit(1)

def crear_directorio_salida(output_dir="datos_espana"):
    """
    Crea el directorio de salida para los datos.
    
    Args:
        output_dir (str): Nombre del directorio de salida.
        
    Returns:
        str: Ruta del directorio de salida.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def generar_csv_final(output_dir="datos_espana"):
    """
    Genera un CSV final con las equivalencias entre los archivos originales
    de PolicySpace2 y los nuevos archivos con datos españoles.
    
    Args:
        output_dir (str): Directorio donde se guardarán los resultados.
        
    Returns:
        pandas.DataFrame: DataFrame con las equivalencias.
    """
    # Crear lista de equivalencias
    equivalencias = [
        {"archivo_original": "ACPs_BR.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Códigos de comunidades autónomas y provincias", "variables": "ID;ACPs;state_code"},
        {"archivo_original": "ACPs_MUN_CODES.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Códigos de municipios", "variables": "ACPs;cod_mun"},
        {"archivo_original": "RM_BR_STATES.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Relación de municipios por provincias", "variables": "codmun"},
        {"archivo_original": "STATES_ID_NUM.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Códigos numéricos de provincias y municipios", "variables": "nummun;codmun"},
        {"archivo_original": "average_num_members_families_2010.csv", "archivo_espana": "tamano_hogares_municipio.csv", "fuente": "INE API", "descripcion": "Tamaño medio de los hogares por municipio", "variables": "AREAP;avg_num_people"},
        {"archivo_original": "estimativas_pop.csv", "archivo_espana": "poblacion_municipio_sexo_edad_2021.csv", "fuente": "INE API", "descripcion": "Cifras de población por municipios", "variables": "mun_code;2001;2002;2003;2004;2005;2006;2008;2009;2011;2012;2013;2014;2015;2016;2017;2018;2019"},
        {"archivo_original": "firms_by_APs2000_t0_full.csv", "archivo_espana": "empresas_por_municipio.csv", "fuente": "INE API", "descripcion": "Empresas por municipio", "variables": "AP;num_firms"},
        {"archivo_original": "firms_by_APs2000_t1_full.csv", "archivo_espana": "empresas_por_municipio.csv", "fuente": "INE API", "descripcion": "Empresas por municipio", "variables": "AP;num_firms"},
        {"archivo_original": "firms_by_APs2010_t0_full.csv", "archivo_espana": "empresas_por_municipio.csv", "fuente": "INE API", "descripcion": "Empresas por municipio", "variables": "AP;num_firms"},
        {"archivo_original": "firms_by_APs2010_t1_full.csv", "archivo_espana": "empresas_por_municipio.csv", "fuente": "INE API", "descripcion": "Empresas por municipio", "variables": "AP;num_firms"},
        {"archivo_original": "idhm_2000_2010.csv", "archivo_espana": "indicador_desarrollo_espana.csv", "fuente": "DataBank API", "descripcion": "Indicadores de desarrollo humano", "variables": "year;cod_mun;idhm"},
        {"archivo_original": "interest_fixed.csv", "archivo_espana": "tasas_interes_espana.csv", "fuente": "DataBank API", "descripcion": "Tipos de interés", "variables": "date;interest;mortgage"},
        {"archivo_original": "interest_nominal.csv", "archivo_espana": "tasas_interes_espana.csv", "fuente": "DataBank API", "descripcion": "Tipos de interés nominales", "variables": "date;interest;mortgage"},
        {"archivo_original": "interest_real.csv", "archivo_espana": "tasas_interes_espana.csv", "fuente": "DataBank API", "descripcion": "Tipos de interés reales", "variables": "date;interest;mortgage"},
        {"archivo_original": "marriage_age_men.csv", "archivo_espana": "marriage_age_men_espana.csv", "fuente": "INE Web", "descripcion": "Edad media al matrimonio por sexo", "variables": "low;high;percentage"},
        {"archivo_original": "marriage_age_men_original.csv", "archivo_espana": "marriage_age_men_espana.csv", "fuente": "INE Web", "descripcion": "Edad media al matrimonio por sexo", "variables": "low;high;percentage"},
        {"archivo_original": "marriage_age_women.csv", "archivo_espana": "marriage_age_women_espana.csv", "fuente": "INE Web", "descripcion": "Edad media al matrimonio por sexo", "variables": "low;high;percentage"},
        {"archivo_original": "marriage_age_women_original.csv", "archivo_espana": "marriage_age_women_espana.csv", "fuente": "INE Web", "descripcion": "Edad media al matrimonio por sexo", "variables": "low;high;percentage"},
        {"archivo_original": "names_and_codes_municipalities.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Relación de municipios y sus códigos", "variables": "cod_name;cod_mun;state"},
        {"archivo_original": "num_people_age_gender_AP_2000.csv", "archivo_espana": "poblacion_municipio_sexo_edad_2021.csv", "fuente": "INE API", "descripcion": "Población por sexo, edad y municipio", "variables": "AREAP;gender;age;num_people;mun"},
        {"archivo_original": "num_people_age_gender_AP_2010.csv", "archivo_espana": "poblacion_municipio_sexo_edad_2021.csv", "fuente": "INE API", "descripcion": "Población por sexo, edad y municipio", "variables": "AREAP;gender;age;num_people;mun"},
        {"archivo_original": "pop_men_2000.csv", "archivo_espana": "poblacion_hombres_2021.csv", "fuente": "INE API", "descripcion": "Población masculina por edad y municipio", "variables": "cod_mun;0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;24;25;26;27;28;29;30;31;32;33;34;35;36;37;38;39;40;41;42;43;44;45;46;47;48;49;50;51;52;53;54;55;56;57;58;59;60;61;62;63;64;65;66;67;68;69;70;71;72;73;74;75;76;77;78;79;80;81;82;83;84;85;86;87;88;89;90;91;92;93;94;95;96;97;98;99;100"},
        {"archivo_original": "pop_men_2010.csv", "archivo_espana": "poblacion_hombres_2021.csv", "fuente": "INE API", "descripcion": "Población masculina por edad y municipio", "variables": "cod_mun;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;24;25;26;27;28;29;30;31;32;33;34;35;36;37;38;39;40;41;42;43;44;45;46;47;48;49;50;51;52;53;54;55;56;57;58;59;60;61;62;63;64;65;66;67;68;69;70;71;72;73;74;75;76;77;78;79;80;81;82;83;84;85;86;87;88;89;90;91;92;93;94;95;96;97;98;99;100;0"},
        {"archivo_original": "pop_women_2000.csv", "archivo_espana": "poblacion_mujeres_2021.csv", "fuente": "INE API", "descripcion": "Población femenina por edad y municipio", "variables": "cod_mun;0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;24;25;26;27;28;29;30;31;32;33;34;35;36;37;38;39;40;41;42;43;44;45;46;47;48;49;50;51;52;53;54;55;56;57;58;59;60;61;62;63;64;65;66;67;68;69;70;71;72;73;74;75;76;77;78;79;80;81;82;83;84;85;86;87;88;89;90;91;92;93;94;95;96;97;98;99;100"},
        {"archivo_original": "pop_women_2010.csv", "archivo_espana": "poblacion_mujeres_2021.csv", "fuente": "INE API", "descripcion": "Población femenina por edad y municipio", "variables": "cod_mun;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;24;25;26;27;28;29;30;31;32;33;34;35;36;37;38;39;40;41;42;43;44;45;46;47;48;49;50;51;52;53;54;55;56;57;58;59;60;61;62;63;64;65;66;67;68;69;70;71;72;73;74;75;76;77;78;79;80;81;82;83;84;85;86;87;88;89;90;91;92;93;94;95;96;97;98;99;100;0"},
        {"archivo_original": "prop_urban_2000_2010.csv", "archivo_espana": "proporcion_urbana_municipios.csv", "fuente": "INE API", "descripcion": "Proporción de población urbana por municipio", "variables": "cod_mun;2000;2010"},
        {"archivo_original": "qualification_APs_2000.csv", "archivo_espana": "educacion_municipios_espana.csv", "fuente": "INE Web", "descripcion": "Nivel de formación por municipio", "variables": "code;1;2;4;6;8;10;11;12;13;14;15;9"},
        {"archivo_original": "qualification_APs_2010.csv", "archivo_espana": "educacion_municipios_espana.csv", "fuente": "INE Web", "descripcion": "Nivel de formación por municipio", "variables": "code;1;2;3;4;5"},
        {"archivo_original": "single_aps_2000.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Códigos de municipios", "variables": "mun_code"},
        {"archivo_original": "single_aps_2010.csv", "archivo_espana": "municipios_codigos_espana.csv", "fuente": "INE API", "descripcion": "Códigos de municipios", "variables": "mun_code"}
    ]
    
    # Añadir equivalencias para los archivos de fertilidad y mortalidad
    for estado in ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]:
        equivalencias.append({
            "archivo_original": f"fertility_{estado}.csv",
            "archivo_espana": "fertilidad_ccaa_espana.csv",
            "fuente": "INE API",
            "descripcion": "Indicadores de fecundidad por comunidades autónomas",
            "variables": "age;2000;2001;2002;2003;2004;2005;2006;2007;2008;2009;2010;2011;2012;2013;2014;2015;2016;2017;2018;2019;2020;2021;2022;2023;2024;2025;2026;2027;2028;2029;2030"
        })
        equivalencias.append({
            "archivo_original": f"mortality_men_{estado}.csv",
            "archivo_espana": "mortalidad_hombres_ccaa_espana.csv",
            "fuente": "INE API",
            "descripcion": "Indicadores de mortalidad masculina por comunidades autónomas",
            "variables": "age;2000;2001;2002;2003;2004;2005;2006;2007;2008;2009;2010;2011;2012;2013;2014;2015;2016;2017;2018;2019;2020;2021;2022;2023;2024;2025;2026;2027;2028;2029;2030"
        })
        equivalencias.append({
            "archivo_original": f"mortality_women_{estado}.csv",
            "archivo_espana": "mortalidad_mujeres_ccaa_espana.csv",
            "fuente": "INE API",
            "descripcion": "Indicadores de mortalidad femenina por comunidades autónomas",
            "variables": "age;2000;2001;2002;2003;2004;2005;2006;2007;2008;2009;2010;2011;2012;2013;2014;2015;2016;2017;2018;2019;2020;2021;2022;2023;2024;2025;2026;2027;2028;2029;2030"
        })
    
    # Añadir equivalencias para los archivos de FPM (Fondo de Participación de los Municipios)
    for estado in ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]:
        equivalencias.append({
            "archivo_original": f"{estado}.csv",
            "archivo_espana": "financiacion_municipios_espana.csv",
            "fuente": "Ministerio de Hacienda",
            "descripcion": "Datos de financiación municipal",
            "variables": "Unnamed: 0;Unnamed: 0.1;ano;fpm;cod;uf"
        })
    
    # Crear DataFrame
    df = pd.DataFrame(equivalencias)
    
    # Guardar en CSV
    output_file = os.path.join(output_dir, "equivalencias_archivos.csv")
    df.to_csv(output_file, index=False)
    
    print(f"CSV de equivalencias guardado en {output_file}")
    return df

def obtener_todos_datos(output_dir="datos_espana"):
    """
    Ejecuta todos los módulos para obtener los datos españoles.
    
    Args:
        output_dir (str): Directorio donde se guardarán los resultados.
    """
    print(f"Iniciando proceso de obtención de datos españoles para PolicySpace2 en {output_dir}...")
    
    # Crear directorio de salida
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
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
    
    # Descargar documentos alternativos
    print("\n=== Descargando documentos alternativos ===")
    descargar_documentos_alternativos.descargar_datos_financiacion_municipal()
    descargar_documentos_alternativos.descargar_datos_fertilidad_mortalidad()
    descargar_documentos_alternativos.descargar_datos_matrimonio()
    descargar_documentos_alternativos.descargar_datos_educacion()
    
    # Generar CSV de equivalencias
    print("\n=== Generando CSV de equivalencias ===")
    equivalencias = generar_csv_final(output_dir)
    
    print("\nProceso completado. Todos los datos han sido guardados en el directorio:", output_dir)
    print("Se ha generado un CSV con las equivalencias entre los archivos originales y los nuevos archivos.")

def main():
    """
    Función principal que ejecuta el script.
    """
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Adaptar PolicySpace2 al contexto español')
    parser.add_argument('--output', type=str, default='datos_espana',
                        help='Directorio de salida para los datos (por defecto: datos_espana)')
    parser.add_argument('--ine-only', action='store_true',
                        help='Obtener solo datos del INE')
    parser.add_argument('--databank-only', action='store_true',
                        help='Obtener solo datos de DataBank')
    parser.add_argument('--alt-only', action='store_true',
                        help='Descargar solo documentos alternativos')
    parser.add_argument('--csv-only', action='store_true',
                        help='Generar solo el CSV de equivalencias')
    
    args = parser.parse_args()
    
    # Crear directorio de salida
    output_dir = crear_directorio_salida(args.output)
    
    # Ejecutar según los argumentos
    if args.ine_only:
        print("Obteniendo solo datos del INE...")
        ine = INE_API()
        ine.get_municipalities()
        ine.get_population_data(2021)
        ine.get_urban_proportion()
        ine.get_firms_by_municipality()
    elif args.databank_only:
        print("Obteniendo solo datos de DataBank...")
        databank = DataBankAPI()
        databank.get_gdp_data()
        databank.get_gdp_per_capita_data()
        databank.get_hdi_data()
        databank.get_interest_rates()
    elif args.alt_only:
        print("Descargando solo documentos alternativos...")
        descargar_documentos_alternativos.descargar_datos_financiacion_municipal()
        descargar_documentos_alternativos.descargar_datos_fertilidad_mortalidad()
        descargar_documentos_alternativos.descargar_datos_matrimonio()
        descargar_documentos_alternativos.descargar_datos_educacion()
    elif args.csv_only:
        print("Generando solo el CSV de equivalencias...")
        generar_csv_final(output_dir)
    else:
        # Ejecutar todo el proceso
        obtener_todos_datos(output_dir)
    
    print("\nProceso completado.")

if __name__ == "__main__":
    main()
