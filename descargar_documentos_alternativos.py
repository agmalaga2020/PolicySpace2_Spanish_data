#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para descargar datos de financiación municipal desde el Ministerio de Hacienda
y otros documentos alternativos necesarios para adaptar PolicySpace2 al contexto español.
"""

import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
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

def descargar_datos_financiacion_municipal():
    """
    Descarga datos de financiación municipal desde el Ministerio de Hacienda.
    """
    output_dir = crear_directorio_salida()
    
    print("Descargando datos de financiación municipal...")
    try:
        # URL de la página con los enlaces a los datos
        url_base = "https://www.hacienda.gob.es/es-ES/CDI/Paginas/SistemasFinanciacionDeuda/InformacionEELLs/DatosFinanciacionEL.aspx"
        response = requests.get(url_base)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar enlaces a archivos Excel o PDF
            enlaces = []
            for a in soup.find_all('a'):
                href = a.get('href', '')
                if '.xls' in href.lower() or '.xlsx' in href.lower() or '.pdf' in href.lower():
                    enlaces.append(href)
            
            # Descargar los archivos encontrados
            for i, enlace in enumerate(enlaces):
                if not enlace.startswith('http'):
                    # Convertir a URL absoluta si es relativa
                    if enlace.startswith('/'):
                        enlace = 'https://www.hacienda.gob.es' + enlace
                    else:
                        enlace = 'https://www.hacienda.gob.es/es-ES/CDI/Paginas/SistemasFinanciacionDeuda/InformacionEELLs/' + enlace
                
                try:
                    print(f"Descargando {enlace}...")
                    file_response = requests.get(enlace)
                    
                    if file_response.status_code == 200:
                        # Extraer nombre del archivo de la URL
                        filename = enlace.split('/')[-1]
                        output_file = os.path.join(output_dir, filename)
                        
                        # Guardar el archivo
                        with open(output_file, 'wb') as f:
                            f.write(file_response.content)
                        
                        print(f"Archivo guardado en {output_file}")
                    else:
                        print(f"Error al descargar {enlace}: {file_response.status_code}")
                except Exception as e:
                    print(f"Error al procesar {enlace}: {e}")
            
            # Si no se encontraron enlaces, crear un archivo CSV de ejemplo
            if not enlaces:
                print("No se encontraron enlaces directos. Creando archivo de ejemplo...")
                
                # Crear un DataFrame de ejemplo con datos de financiación municipal
                data = {
                    'cod_mun': ['01001', '02001', '03001', '04001', '05001'],
                    'municipio': ['Vitoria', 'Albacete', 'Alicante', 'Almería', 'Ávila'],
                    'financiacion_2023': [1000000, 800000, 1200000, 750000, 500000],
                    'financiacion_2024': [1050000, 840000, 1260000, 787500, 525000],
                    'financiacion_2025': [1102500, 882000, 1323000, 826875, 551250]
                }
                
                df = pd.DataFrame(data)
                output_file = os.path.join(output_dir, "financiacion_municipios_espana.csv")
                df.to_csv(output_file, index=False)
                
                print(f"Archivo de ejemplo creado en {output_file}")
        else:
            print(f"Error al acceder a la página: {response.status_code}")
    except Exception as e:
        print(f"Error al descargar datos de financiación municipal: {e}")

def descargar_datos_fertilidad_mortalidad():
    """
    Descarga datos de fertilidad y mortalidad desde el INE.
    """
    output_dir = crear_directorio_salida()
    
    print("Descargando datos de fertilidad y mortalidad...")
    try:
        # URLs de ejemplo para datos de fertilidad y mortalidad
        urls = {
            'fertilidad': 'https://www.ine.es/jaxi/files/tpx/es/csv_bd/12201.csv',
            'mortalidad_hombres': 'https://www.ine.es/jaxi/files/tpx/es/csv_bd/13453.csv',
            'mortalidad_mujeres': 'https://www.ine.es/jaxi/files/tpx/es/csv_bd/13454.csv'
        }
        
        for tipo, url in urls.items():
            try:
                print(f"Descargando datos de {tipo}...")
                response = requests.get(url)
                
                if response.status_code == 200:
                    # Guardar el archivo
                    output_file = os.path.join(output_dir, f"{tipo}_ccaa_espana.csv")
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"Datos de {tipo} guardados en {output_file}")
                else:
                    print(f"Error al descargar datos de {tipo}: {response.status_code}")
                    
                    # Crear un DataFrame de ejemplo
                    if tipo == 'fertilidad':
                        data = {
                            'age': list(range(15, 50)),
                            '2000': [0.01, 0.02, 0.03, 0.05, 0.08, 0.10, 0.12, 0.14, 0.15, 0.14, 0.12, 0.10, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01, 0.005] * 2,
                            '2010': [0.005, 0.01, 0.02, 0.04, 0.07, 0.09, 0.11, 0.13, 0.14, 0.13, 0.11, 0.09, 0.07, 0.05, 0.03, 0.02, 0.01, 0.005, 0.002] * 2,
                            '2020': [0.002, 0.005, 0.01, 0.03, 0.06, 0.08, 0.10, 0.12, 0.13, 0.12, 0.10, 0.08, 0.06, 0.04, 0.02, 0.01, 0.005, 0.002, 0.001] * 2
                        }
                    else:
                        data = {
                            'age': list(range(0, 100)),
                            '2000': [0.05, 0.01, 0.005] + [0.001, 0.002, 0.003, 0.004, 0.005] * 10 + [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10] * 5,
                            '2010': [0.04, 0.008, 0.004] + [0.001, 0.002, 0.003, 0.004, 0.005] * 10 + [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10] * 5,
                            '2020': [0.03, 0.006, 0.003] + [0.001, 0.002, 0.003, 0.004, 0.005] * 10 + [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10] * 5
                        }
                    
                    df = pd.DataFrame(data)
                    output_file = os.path.join(output_dir, f"{tipo}_ccaa_espana.csv")
                    df.to_csv(output_file, index=False)
                    
                    print(f"Archivo de ejemplo para {tipo} creado en {output_file}")
            except Exception as e:
                print(f"Error al procesar datos de {tipo}: {e}")
    except Exception as e:
        print(f"Error al descargar datos de fertilidad y mortalidad: {e}")

def descargar_datos_matrimonio():
    """
    Descarga datos de matrimonio por edad desde el INE.
    """
    output_dir = crear_directorio_salida()
    
    print("Descargando datos de matrimonio por edad...")
    try:
        # URL de ejemplo para datos de matrimonio
        url = 'https://www.ine.es/jaxi/files/tpx/es/csv_bd/30304.csv'
        
        response = requests.get(url)
        
        if response.status_code == 200:
            # Guardar el archivo
            output_file = os.path.join(output_dir, "matrimonio_edad_espana.csv")
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            print(f"Datos de matrimonio guardados en {output_file}")
        else:
            print(f"Error al descargar datos de matrimonio: {response.status_code}")
            
            # Crear un DataFrame de ejemplo
            data = {
                'low': [15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
                'high': [19, 24, 29, 34, 39, 44, 49, 54, 59, 64],
                'percentage_men': [0.01, 0.05, 0.20, 0.30, 0.20, 0.10, 0.05, 0.04, 0.03, 0.02],
                'percentage_women': [0.03, 0.15, 0.30, 0.25, 0.15, 0.05, 0.03, 0.02, 0.01, 0.01]
            }
            
            df = pd.DataFrame(data)
            
            # Guardar archivos separados para hombres y mujeres
            men_df = df[['low', 'high', 'percentage_men']].rename(columns={'percentage_men': 'percentage'})
            women_df = df[['low', 'high', 'percentage_women']].rename(columns={'percentage_women': 'percentage'})
            
            men_output = os.path.join(output_dir, "marriage_age_men_espana.csv")
            women_output = os.path.join(output_dir, "marriage_age_women_espana.csv")
            
            men_df.to_csv(men_output, index=False)
            women_df.to_csv(women_output, index=False)
            
            print(f"Archivos de ejemplo para matrimonio creados en {men_output} y {women_output}")
    except Exception as e:
        print(f"Error al descargar datos de matrimonio: {e}")

def descargar_datos_educacion():
    """
    Descarga datos de nivel educativo por municipio desde el INE.
    """
    output_dir = crear_directorio_salida()
    
    print("Descargando datos de educación por municipio...")
    try:
        # URL de ejemplo para datos de educación
        url = 'https://www.ine.es/jaxi/files/tpx/es/csv_bd/50321.csv'
        
        response = requests.get(url)
        
        if response.status_code == 200:
            # Guardar el archivo
            output_file = os.path.join(output_dir, "educacion_municipios_espana.csv")
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            print(f"Datos de educación guardados en {output_file}")
        else:
            print(f"Error al descargar datos de educación: {response.status_code}")
            
            # Crear un DataFrame de ejemplo
            municipios = ['01001', '02001', '03001', '04001', '05001']
            data = {
                'code': municipios,
                '1': [0.10, 0.15, 0.12, 0.18, 0.20],  # Sin estudios
                '2': [0.25, 0.30, 0.28, 0.32, 0.35],  # Primaria
                '3': [0.35, 0.30, 0.32, 0.28, 0.25],  # Secundaria
                '4': [0.20, 0.15, 0.18, 0.12, 0.10],  # Bachillerato
                '5': [0.10, 0.10, 0.10, 0.10, 0.10]   # Universidad
            }
            
            df = pd.DataFrame(data)
            output_file = os.path.join(output_dir, "educacion_municipios_espana.csv")
            df.to_csv(output_file, index=False)
            
            print(f"Archivo de ejemplo para educación creado en {output_file}")
    except Exception as e:
        print(f"Error al descargar datos de educación: {e}")

def main():
    """
    Función principal que ejecuta todo el proceso de descarga de documentos alternativos.
    """
    print("Iniciando proceso de descarga de documentos alternativos para PolicySpace2...")
    
    # Crear directorio de salida
    output_dir = crear_directorio_salida()
    
    # Descargar datos de financiación municipal
    descargar_datos_financiacion_municipal()
    
    # Descargar datos de fertilidad y mortalidad
    descargar_datos_fertilidad_mortalidad()
    
    # Descargar datos de matrimonio
    descargar_datos_matrimonio()
    
    # Descargar datos de educación
    descargar_datos_educacion()
    
    print("\nProceso completado. Todos los documentos alternativos han sido descargados o creados en el directorio:", output_dir)

if __name__ == "__main__":
    main()
