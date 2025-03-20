#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para conectar con la API de DataBank del Banco Mundial
y obtener indicadores económicos para España.
"""

import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient
import pandas as pd
import os
from datetime import datetime

class DataBankAPI:
    """
    Clase para interactuar con la API de DataBank del Banco Mundial.
    """
    
    def __init__(self):
        """
        Inicializa la clase con el cliente de API.
        """
        self.client = ApiClient()
        self.output_dir = "datos_espana"
        
        # Crear directorio de salida si no existe
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def get_indicator_data(self, indicator, country="ESP"):
        """
        Obtiene datos de un indicador específico para España.
        
        Args:
            indicator (str): Código del indicador.
            country (str): Código ISO del país (ESP para España).
            
        Returns:
            dict: Datos del indicador.
        """
        try:
            data = self.client.call_api('DataBank/indicator_data', query={'indicator': indicator, 'country': country})
            return data
        except Exception as e:
            print(f"Error al obtener datos del indicador {indicator}: {e}")
            return None
    
    def get_indicator_detail(self, indicator):
        """
        Obtiene detalles de un indicador específico.
        
        Args:
            indicator (str): Código del indicador.
            
        Returns:
            dict: Detalles del indicador.
        """
        try:
            data = self.client.call_api('DataBank/indicator_detail', query={'indicatorCode': indicator})
            return data
        except Exception as e:
            print(f"Error al obtener detalles del indicador {indicator}: {e}")
            return None
    
    def search_indicators(self, query, page=1, page_size=10):
        """
        Busca indicadores que coincidan con la consulta.
        
        Args:
            query (str): Texto a buscar.
            page (int): Número de página.
            page_size (int): Tamaño de página.
            
        Returns:
            dict: Resultados de la búsqueda.
        """
        try:
            data = self.client.call_api('DataBank/indicator_list', query={'q': query, 'page': page, 'pageSize': page_size})
            return data
        except Exception as e:
            print(f"Error al buscar indicadores con la consulta {query}: {e}")
            return None
    
    def get_gdp_data(self):
        """
        Obtiene datos del PIB para España.
        
        Returns:
            pandas.DataFrame: DataFrame con los datos del PIB.
        """
        indicator = "NY.GDP.MKTP.CD"  # PIB en USD
        data = self.get_indicator_data(indicator)
        
        if data:
            # Convertir a DataFrame
            years = []
            values = []
            
            for year, value in data.get('data', {}).items():
                if value is not None:
                    years.append(year)
                    values.append(value)
            
            df = pd.DataFrame({
                'year': years,
                'gdp_usd': values
            })
            
            # Guardar en CSV
            output_file = os.path.join(self.output_dir, "pib_espana.csv")
            df.to_csv(output_file, index=False)
            
            print(f"Datos del PIB guardados en {output_file}")
            return df
        
        return None
    
    def get_gdp_per_capita_data(self):
        """
        Obtiene datos del PIB per cápita para España.
        
        Returns:
            pandas.DataFrame: DataFrame con los datos del PIB per cápita.
        """
        indicator = "NY.GDP.PCAP.CD"  # PIB per cápita en USD
        data = self.get_indicator_data(indicator)
        
        if data:
            # Convertir a DataFrame
            years = []
            values = []
            
            for year, value in data.get('data', {}).items():
                if value is not None:
                    years.append(year)
                    values.append(value)
            
            df = pd.DataFrame({
                'year': years,
                'gdp_per_capita_usd': values
            })
            
            # Guardar en CSV
            output_file = os.path.join(self.output_dir, "pib_per_capita_espana.csv")
            df.to_csv(output_file, index=False)
            
            print(f"Datos del PIB per cápita guardados en {output_file}")
            return df
        
        return None
    
    def get_unemployment_data(self):
        """
        Obtiene datos de desempleo para España.
        
        Returns:
            pandas.DataFrame: DataFrame con los datos de desempleo.
        """
        indicator = "SL.UEM.TOTL.ZS"  # Tasa de desempleo
        data = self.get_indicator_data(indicator)
        
        if data:
            # Convertir a DataFrame
            years = []
            values = []
            
            for year, value in data.get('data', {}).items():
                if value is not None:
                    years.append(year)
                    values.append(value)
            
            df = pd.DataFrame({
                'year': years,
                'unemployment_rate': values
            })
            
            # Guardar en CSV
            output_file = os.path.join(self.output_dir, "desempleo_espana.csv")
            df.to_csv(output_file, index=False)
            
            print(f"Datos de desempleo guardados en {output_file}")
            return df
        
        return None
    
    def get_hdi_data(self):
        """
        Obtiene datos del Índice de Desarrollo Humano para España.
        Equivalente a idhm_2000_2010.csv
        
        Returns:
            pandas.DataFrame: DataFrame con los datos del IDH.
        """
        # El Banco Mundial no tiene directamente el IDH, pero podemos usar indicadores relacionados
        # o buscar una fuente alternativa para este dato específico
        
        # Para este ejemplo, usaremos el PIB per cápita como aproximación
        indicator = "NY.GDP.PCAP.CD"  # PIB per cápita en USD
        data = self.get_indicator_data(indicator)
        
        if data:
            # Convertir a DataFrame
            years = []
            values = []
            
            for year, value in data.get('data', {}).items():
                if value is not None and int(year) >= 2000:  # Filtrar años desde 2000
                    years.append(year)
                    values.append(value)
            
            df = pd.DataFrame({
                'year': years,
                'gdp_per_capita_usd': values
            })
            
            # Guardar en CSV
            output_file = os.path.join(self.output_dir, "indicador_desarrollo_espana.csv")
            df.to_csv(output_file, index=False)
            
            print(f"Datos de desarrollo guardados en {output_file}")
            return df
        
        return None
    
    def get_interest_rates(self):
        """
        Obtiene datos de tasas de interés para España.
        Equivalente a interest_*.csv
        
        Returns:
            pandas.DataFrame: DataFrame con los datos de tasas de interés.
        """
        # Buscar indicadores relacionados con tasas de interés
        search_results = self.search_indicators("interest rate spain")
        
        if search_results and 'items' in search_results:
            # Mostrar los indicadores encontrados
            print("Indicadores de tasas de interés encontrados:")
            for item in search_results.get('items', []):
                print(f"- {item.get('indicatorCode')}: {item.get('indicatorName')}")
            
            # Usar el primer indicador encontrado como ejemplo
            if search_results.get('items'):
                indicator = search_results.get('items')[0].get('indicatorCode')
                data = self.get_indicator_data(indicator)
                
                if data:
                    # Convertir a DataFrame
                    years = []
                    values = []
                    
                    for year, value in data.get('data', {}).items():
                        if value is not None:
                            years.append(year)
                            values.append(value)
                    
                    df = pd.DataFrame({
                        'year': years,
                        'interest_rate': values
                    })
                    
                    # Guardar en CSV
                    output_file = os.path.join(self.output_dir, "tasas_interes_espana.csv")
                    df.to_csv(output_file, index=False)
                    
                    print(f"Datos de tasas de interés guardados en {output_file}")
                    return df
        
        print("No se encontraron indicadores de tasas de interés adecuados.")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    databank = DataBankAPI()
    
    print("Obteniendo datos del PIB...")
    gdp = databank.get_gdp_data()
    
    print("\nObteniendo datos del PIB per cápita...")
    gdp_per_capita = databank.get_gdp_per_capita_data()
    
    print("\nObteniendo datos de desempleo...")
    unemployment = databank.get_unemployment_data()
    
    print("\nObteniendo datos de desarrollo humano...")
    hdi = databank.get_hdi_data()
    
    print("\nObteniendo datos de tasas de interés...")
    interest = databank.get_interest_rates()
    
    print("\nProceso completado.")
