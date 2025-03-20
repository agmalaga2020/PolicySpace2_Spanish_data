import pandas as pd
import requests
import json
import os
from bs4 import BeautifulSoup
import time
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class INEAPIConnector:
    """
    Clase para conectar con la API JSON del INE (Instituto Nacional de Estadística)
    """
    
    def __init__(self, idioma="ES"):
        """
        Inicializa el conector con el idioma especificado
        
        Args:
            idioma (str): Idioma para las consultas (ES o EN)
        """
        self.base_url = "https://servicios.ine.es/wstempus/js"
        self.idioma = idioma
        logger.info(f"Inicializado conector INE API con idioma: {idioma}")
    
    def get_data_table(self, table_id):
        """
        Obtiene los datos de una tabla específica
        
        Args:
            table_id (str): Identificador de la tabla
            
        Returns:
            dict: Datos de la tabla en formato JSON
        """
        url = f"{self.base_url}/{self.idioma}/DATOS_TABLA/{table_id}"
        logger.info(f"Solicitando datos de tabla: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener datos de tabla {table_id}: {e}")
            return None
    
    def get_data_series(self, series_id):
        """
        Obtiene los datos de una serie específica
        
        Args:
            series_id (str): Identificador de la serie
            
        Returns:
            dict: Datos de la serie en formato JSON
        """
        url = f"{self.base_url}/{self.idioma}/DATOS_SERIE/{series_id}"
        logger.info(f"Solicitando datos de serie: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener datos de serie {series_id}: {e}")
            return None
    
    def get_available_operations(self):
        """
        Obtiene la lista de operaciones estadísticas disponibles
        
        Returns:
            dict: Lista de operaciones disponibles
        """
        url = f"{self.base_url}/{self.idioma}/OPERACIONES_DISPONIBLES"
        logger.info("Solicitando operaciones disponibles")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener operaciones disponibles: {e}")
            return None
    
    def get_operation_variables(self, operation_id):
        """
        Obtiene las variables de una operación estadística
        
        Args:
            operation_id (str): Identificador de la operación
            
        Returns:
            dict: Variables de la operación
        """
        url = f"{self.base_url}/{self.idioma}/VARIABLES_OPERACION/{operation_id}"
        logger.info(f"Solicitando variables de operación: {operation_id}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener variables de operación {operation_id}: {e}")
            return None
    
    def get_population_data(self, municipality_code=None, year=None):
        """
        Obtiene datos de población por municipio
        
        Args:
            municipality_code (str, optional): Código del municipio
            year (str, optional): Año de los datos
            
        Returns:
            dict: Datos de población
        """
        # Tabla de población por municipios
        table_id = "t1"
        
        # Construir parámetros de consulta
        params = {}
        if municipality_code:
            params["municipality"] = municipality_code
        if year:
            params["year"] = year
        
        # Construir URL con parámetros
        url = f"{self.base_url}/{self.idioma}/DATOS_TABLA/{table_id}"
        if params:
            url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
        
        logger.info(f"Solicitando datos de población: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener datos de población: {e}")
            return None
    
    def get_demographic_indicators(self, indicator_type, region_code=None, year=None):
        """
        Obtiene indicadores demográficos (fertilidad, mortalidad, etc.)
        
        Args:
            indicator_type (str): Tipo de indicador (fertility, mortality)
            region_code (str, optional): Código de la región (CCAA)
            year (str, optional): Año de los datos
            
        Returns:
            dict: Datos del indicador demográfico
        """
        # Mapeo de tipos de indicadores a IDs de tablas
        indicator_tables = {
            "fertility": "t3",  # Indicadores de fecundidad
            "mortality": "t4"   # Tablas de mortalidad
        }
        
        table_id = indicator_tables.get(indicator_type)
        if not table_id:
            logger.error(f"Tipo de indicador no válido: {indicator_type}")
            return None
        
        # Construir parámetros de consulta
        params = {}
        if region_code:
            params["region"] = region_code
        if year:
            params["year"] = year
        
        # Construir URL con parámetros
        url = f"{self.base_url}/{self.idioma}/DATOS_TABLA/{table_id}"
        if params:
            url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
        
        logger.info(f"Solicitando indicadores demográficos: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener indicadores demográficos: {e}")
            return None
    
    def save_data_to_csv(self, data, output_file):
        """
        Guarda los datos obtenidos en un archivo CSV
        
        Args:
            data (dict): Datos a guardar
            output_file (str): Ruta del archivo de salida
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            # Convertir datos a DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict) and "Data" in data:
                df = pd.DataFrame(data["Data"])
            else:
                logger.error("Formato de datos no reconocido")
                return False
            
            # Guardar a CSV
            df.to_csv(output_file, index=False)
            logger.info(f"Datos guardados en: {output_file}")
            return True
        except Exception as e:
            logger.error(f"Error al guardar datos en CSV: {e}")
            return False


class HaciendaDataConnector:
    """
    Clase para obtener datos del Ministerio de Hacienda
    """
    
    def __init__(self):
        """
        Inicializa el conector para el Ministerio de Hacienda
        """
        self.base_url = "https://serviciostelematicosext.hacienda.gob.es/SGFAL/CONPREL"
        logger.info("Inicializado conector Ministerio de Hacienda")
    
    def get_municipal_financing_data(self, year, province_code=None):
        """
        Obtiene datos de financiación municipal
        
        Args:
            year (str): Año de los datos
            province_code (str, optional): Código de provincia
            
        Returns:
            pd.DataFrame: Datos de financiación municipal
        """
        # Esta función simula la descarga de datos, ya que no hay una API pública
        # En un caso real, se implementaría web scraping o descarga directa de archivos
        
        logger.info(f"Solicitando datos de financiación municipal para año {year}")
        
        try:
            # Simular descarga de datos
            time.sleep(1)
            
            # Crear DataFrame de ejemplo
            data = {
                "municipio": ["Madrid", "Barcelona", "Valencia"],
                "codigo": ["28079", "08019", "46250"],
                "año": [year, year, year],
                "financiacion": [1000000, 800000, 600000]
            }
            
            if province_code:
                # Filtrar por provincia
                data = {k: [v for i, v in enumerate(data[k]) if data["codigo"][i].startswith(province_code[:2])] 
                       for k in data}
            
            df = pd.DataFrame(data)
            logger.info(f"Datos de financiación municipal obtenidos para año {year}")
            return df
        except Exception as e:
            logger.error(f"Error al obtener datos de financiación municipal: {e}")
            return None
    
    def download_financing_data(self, year, output_dir):
        """
        Descarga archivos de financiación municipal
        
        Args:
            year (str): Año de los datos
            output_dir (str): Directorio de salida
            
        Returns:
            list: Lista de archivos descargados
        """
        logger.info(f"Descargando archivos de financiación municipal para año {year}")
        
        try:
            # Crear directorio si no existe
            os.makedirs(output_dir, exist_ok=True)
            
            # Simular descarga de archivos
            time.sleep(2)
            
            # Crear archivos de ejemplo para cada CCAA
            ccaa_codes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", 
                         "10", "11", "12", "13", "14", "15", "16", "17"]
            
            files_created = []
            
            for code in ccaa_codes:
                # Crear DataFrame de ejemplo
                data = {
                    "municipio": [f"Municipio_{i}" for i in range(1, 6)],
                    "codigo": [f"{code}{i:03d}" for i in range(1, 6)],
                    "año": [year] * 5,
                    "financiacion": [100000 * i for i in range(1, 6)]
                }
                
                df = pd.DataFrame(data)
                
                # Guardar a CSV
                output_file = os.path.join(output_dir, f"financiacion_{code}_{year}.csv")
                df.to_csv(output_file, index=False)
                files_created.append(output_file)
            
            logger.info(f"Archivos de financiación municipal descargados: {len(files_created)}")
            return files_created
        except Exception as e:
            logger.error(f"Error al descargar archivos de financiación municipal: {e}")
            return []


class DIRCEConnector:
    """
    Clase para obtener datos del Directorio Central de Empresas (DIRCE)
    """
    
    def __init__(self):
        """
        Inicializa el conector para el DIRCE
        """
        self.base_url = "https://www.ine.es/jaxiT3/Tabla.htm"
        logger.info("Inicializado conector DIRCE")
    
    def get_companies_by_municipality(self, municipality_code=None, activity_code=None, year=None):
        """
        Obtiene datos de empresas por municipio
        
        Args:
            municipality_code (str, optional): Código del municipio
            activity_code (str, optional): Código de actividad económica
            year (str, optional): Año de los datos
            
        Returns:
            pd.DataFrame: Datos de empresas por municipio
        """
        # Tabla de empresas por municipio y actividad principal
        table_id = "t=4721"
        
        # Construir parámetros de consulta
        params = []
        if municipality_code:
            params.append(f"municipality={municipality_code}")
        if activity_code:
            params.append(f"activity={activity_code}")
        if year:
            params.append(f"year={year}")
        
        # Construir URL con parámetros
        url = f"{self.base_url}?{table_id}"
        if params:
            url += "&" + "&".join(params)
        
        logger.info(f"Solicitando datos de empresas por municipio: {url}")
        
        try:
            # En un caso real, se implementaría web scraping para obtener los datos
            # Aquí simulamos la obtención de datos
            
            # Crear DataFrame de ejemplo
            data = {
                "municipio": ["Madrid", "Barcelona", "Valencia"],
                "codigo": ["28079", "08019", "46250"],
                "actividad": ["Total", "Total", "Total"],
                "año": [year or "2023"] * 3,
                "num_empresas": [200000, 150000, 80000]
            }
            
            if municipality_code:
                # Filtrar por municipio
                data = {k: [v for i, v in enumerate(data[k]) if data["codigo"][i] == municipality_code] 
                       for k in data}
            
            df = pd.DataFrame(data)
            logger.info(f"Datos de empresas por municipio obtenidos")
            return df
        except Exception as e:
            logger.error(f"Error al obtener datos de empresas por municipio: {e}")
            return None
    
    def scrape_companies_data(self, url):
        """
        Realiza web scraping para obtener datos de empresas
        
        Args:
            url (str): URL a scrapear
            
        Returns:
            pd.DataFrame: Datos obtenidos
        """
        logger.info(f"Realizando web scraping en: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # En un caso real, se implementaría la lógica de extracción de datos
            # Aquí simulamos la extracción
            
            # Crear DataFrame de ejemplo
            data = {
                "municipio": ["Madrid", "Barcelona", "Valencia"],
                "codigo": ["28079", "08019", "46250"],
                "actividad": ["Total", "Total", "Total"],
                "año": ["2023"] * 3,
                "num_empresas": [200000, 150000, 80000]
            }
            
            df = pd.DataFrame(data)
            logger.info(f"Datos obtenidos mediante web scraping")
            return df
        except Exception as e:
            logger.error(f"Error al realizar web scraping: {e}")
            return None


def main():
    """
    Función principal para demostrar el uso de los conectores
    """
    # Crear directorio de salida
    output_dir = "datos_espana"
    os.makedirs(output_dir, exist_ok=True)
    
    # Inicializar conectores
    ine_connector = INEAPIConnector()
    hacienda_connector = HaciendaDataConnector()
    dirce_connector = DIRCEConnector()
    
    # Ejemplo de uso del conector INE
    logger.info("Obteniendo datos demográficos del INE...")
    population_data = ine_connector.get_population_data(year="2023")
    if population_data:
        ine_connector.save_data_to_csv(population_data, os.path.join(output_dir, "poblacion_2023.csv"))
    
    # Ejemplo de uso del conector Hacienda
    logger.info("Obteniendo datos de financiación municipal...")
    financing_data = hacienda_connector.get_municipal_financing_data("2023")
    if financing_data is not None:
        financing_data.to_csv(os.path.join(output_dir, "financiacion_2023.csv"), index=False)
    
    # Ejemplo de uso del conector DIRCE
    logger.info("Obteniendo datos de empresas por municipio...")
    companies_data = dirce_connector.get_companies_by_municipality(year="2023")
    if companies_data is not None:
        companies_data.to_csv(os.path.join(output_dir, "empresas_2023.csv"), index=False)
    
    logger.info("Proceso completado. Datos guardados en directorio: " + output_dir)


if __name__ == "__main__":
    main()
