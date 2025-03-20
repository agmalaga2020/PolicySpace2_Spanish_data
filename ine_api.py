#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para conectar con la API JSON del INE (Instituto Nacional de Estadística) de España
y obtener datos equivalentes a los utilizados en PolicySpace2.
"""

import requests
import pandas as pd
import json
import os
from datetime import datetime

class INE_API:
    """
    Clase para interactuar con la API JSON del INE (Instituto Nacional de Estadística) de España.
    """
    
    def __init__(self):
        """
        Inicializa la clase con la URL base de la API del INE.
        """
        self.base_url = "https://servicios.ine.es/wstempus/js"
        self.output_dir = "datos_espana"
        
        # Crear directorio de salida si no existe
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def get_series(self, series_id):
        """
        Obtiene los datos de una serie específica del INE.
        
        Args:
            series_id (str): Identificador de la serie.
            
        Returns:
            dict: Datos de la serie en formato JSON.
        """
        url = f"{self.base_url}/ES/SERIES/{series_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener la serie {series_id}: {response.status_code}")
            return None
    
    def get_table(self, table_id):
        """
        Obtiene los datos de una tabla específica del INE.
        
        Args:
            table_id (str): Identificador de la tabla.
            
        Returns:
            dict: Datos de la tabla en formato JSON.
        """
        url = f"{self.base_url}/ES/DATOS_TABLA/{table_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener la tabla {table_id}: {response.status_code}")
            return None
    
    def search_operations(self, query):
        """
        Busca operaciones estadísticas que coincidan con la consulta.
        
        Args:
            query (str): Texto a buscar.
            
        Returns:
            dict: Resultados de la búsqueda en formato JSON.
        """
        url = f"{self.base_url}/ES/OPERACIONES_ESTADISTICAS"
        params = {"q": query}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al buscar operaciones: {response.status_code}")
            return None
    
    def get_municipalities(self):
        """
        Obtiene la lista de municipios y sus códigos.
        Equivalente a ACPs_MUN_CODES.csv y names_and_codes_municipalities.csv
        
        Returns:
            pandas.DataFrame: DataFrame con los municipios y sus códigos.
        """
        # La tabla 35 contiene los municipios
        table_id = "35"
        data = self.get_table(table_id)
        
        if data:
            # Procesar los datos para crear un DataFrame
            municipalities = []
            
            for item in data:
                try:
                    mun_code = item.get('COD', '')
                    mun_name = item.get('Nombre', '')
                    province_code = mun_code[:2] if len(mun_code) >= 5 else ''
                    
                    municipalities.append({
                        'cod_mun': mun_code,
                        'cod_name': mun_name,
                        'state_code': province_code
                    })
                except Exception as e:
                    print(f"Error al procesar municipio: {e}")
            
            df = pd.DataFrame(municipalities)
            
            # Guardar en CSV
            output_file = os.path.join(self.output_dir, "municipios_codigos_espana.csv")
            df.to_csv(output_file, index=False)
            
            print(f"Datos de municipios guardados en {output_file}")
            return df
        
        return None
    
    def get_population_data(self, year=2021):
        """
        Obtiene datos de población por municipio, sexo y edad.
        Equivalente a pop_men_XXXX.csv, pop_women_XXXX.csv y num_people_age_gender_AP_XXXX.csv
        
        Args:
            year (int): Año para el que se quieren los datos.
            
        Returns:
            pandas.DataFrame: DataFrame con los datos de población.
        """
        # Buscar la tabla adecuada para población por municipios
        # Esto es una aproximación, habría que ajustar el ID de tabla según la disponibilidad
        table_id = "50563"  # Este ID es un ejemplo, habría que verificar el correcto
        
        data = self.get_table(table_id)
        
        if data:
            # Procesar los datos para crear un DataFrame
            population_data = []
            
            for item in data:
                try:
                    mun_code = item.get('Municipio', {}).get('COD', '')
                    gender = item.get('Sexo', {}).get('Nombre', '')
                    age = item.get('Edad', {}).get('Nombre', '')
                    value = item.get('Valor', 0)
                    
                    population_data.append({
                        'cod_mun': mun_code,
                        'gender': 'M' if gender == 'Hombres' else 'F',
                        'age': age,
                        'num_people': value
                    })
                except Exception as e:
                    print(f"Error al procesar dato de población: {e}")
            
            df = pd.DataFrame(population_data)
            
            # Guardar en CSV
            output_file = os.path.join(self.output_dir, f"poblacion_municipio_sexo_edad_{year}.csv")
            df.to_csv(output_file, index=False)
            
            # También crear archivos separados por género
            men_df = df[df['gender'] == 'M'].pivot(index='cod_mun', columns='age', values='num_people')
            women_df = df[df['gender'] == 'F'].pivot(index='cod_mun', columns='age', values='num_people')
            
            men_output = os.path.join(self.output_dir, f"poblacion_hombres_{year}.csv")
            women_output = os.path.join(self.output_dir, f"poblacion_mujeres_{year}.csv")
            
            men_df.to_csv(men_output)
            women_df.to_csv(women_output)
            
            print(f"Datos de población guardados en {output_file}")
            print(f"Datos de población masculina guardados en {men_output}")
            print(f"Datos de población femenina guardados en {women_output}")
            
            return df
        
        return None
    
    def get_urban_proportion(self):
        """
        Obtiene la proporción de población urbana por municipio.
        Equivalente a prop_urban_2000_2010.csv
        
        Returns:
            pandas.DataFrame: DataFrame con la proporción urbana.
        """
        # Buscar la tabla adecuada para población urbana/rural
        # Esto es una aproximación, habría que ajustar el ID de tabla según la disponibilidad
        table_id = "50531"  # Este ID es un ejemplo, habría que verificar el correcto
        
        data = self.get_table(table_id)
        
        if data:
            # Procesar los datos para crear un DataFrame
            urban_data = []
            
            for item in data:
                try:
                    mun_code = item.get('Municipio', {}).get('COD', '')
                    year = item.get('Periodo', {}).get('Nombre', '')
                    urban_value = item.get('Valor', 0)
                    
                    urban_data.append({
                        'cod_mun': mun_code,
                        'year': year,
                        'urban_proportion': urban_value
                    })
                except Exception as e:
                    print(f"Error al procesar dato de proporción urbana: {e}")
            
            df = pd.DataFrame(urban_data)
            
            # Pivotar para tener años como columnas
            pivot_df = df.pivot(index='cod_mun', columns='year', values='urban_proportion')
            
            # Guardar en CSV
            output_file = os.path.join(self.output_dir, "proporcion_urbana_municipios.csv")
            pivot_df.to_csv(output_file)
            
            print(f"Datos de proporción urbana guardados en {output_file}")
            return pivot_df
        
        return None
    
    def get_firms_by_municipality(self):
        """
        Obtiene el número de empresas por municipio.
        Equivalente a firms_by_APs*.csv
        
        Returns:
            pandas.DataFrame: DataFrame con el número de empresas.
        """
        # Buscar la tabla adecuada para empresas por municipio
        # Esto es una aproximación, habría que ajustar el ID de tabla según la disponibilidad
        table_id = "50891"  # Este ID es un ejemplo, habría que verificar el correcto
        
        data = self.get_table(table_id)
        
        if data:
            # Procesar los datos para crear un DataFrame
            firms_data = []
            
            for item in data:
                try:
                    mun_code = item.get('Municipio', {}).get('COD', '')
                    year = item.get('Periodo', {}).get('Nombre', '')
                    num_firms = item.get('Valor', 0)
                    
                    firms_data.append({
                        'cod_mun': mun_code,
                        'year': year,
                        'num_firms': num_firms
                    })
                except Exception as e:
                    print(f"Error al procesar dato de empresas: {e}")
            
            df = pd.DataFrame(firms_data)
            
            # Guardar en CSV
            output_file = os.path.join(self.output_dir, "empresas_por_municipio.csv")
            df.to_csv(output_file, index=False)
            
            print(f"Datos de empresas guardados en {output_file}")
            return df
        
        return None

# Ejemplo de uso
if __name__ == "__main__":
    ine = INE_API()
    
    print("Obteniendo datos de municipios...")
    municipalities = ine.get_municipalities()
    
    print("\nObteniendo datos de población...")
    population = ine.get_population_data(2021)
    
    print("\nObteniendo datos de proporción urbana...")
    urban = ine.get_urban_proportion()
    
    print("\nObteniendo datos de empresas...")
    firms = ine.get_firms_by_municipality()
    
    print("\nProceso completado.")
