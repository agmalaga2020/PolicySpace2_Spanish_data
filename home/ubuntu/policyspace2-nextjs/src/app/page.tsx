import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <div>
      <header className="bg-blue-600 text-white py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold">PolicySpace2</h1>
              <p className="text-xl">Adaptación al Contexto Español</p>
            </div>
            <div className="mt-4 md:mt-0">
              <Link href="/downloads/scripts_policyspace2_espana.zip" className="bg-white text-blue-600 px-4 py-2 rounded hover:bg-gray-100">
                Descargar Scripts
              </Link>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">Introducción</h2>
          <p className="mb-4">Este proyecto proporciona herramientas para adaptar PolicySpace2 al contexto español, permitiendo obtener datos españoles equivalentes a los utilizados en el proyecto original brasileño. Se han desarrollado varios módulos Python que conectan con APIs oficiales y descargan datos alternativos cuando es necesario.</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
            <div className="bg-white p-6 rounded shadow">
              <h3 className="text-xl font-semibold mb-2">Objetivo</h3>
              <p>Adaptar el proyecto PolicySpace2 al mercado español, recopilando datos equivalentes a los utilizados en el contexto brasileño original.</p>
            </div>
            <div className="bg-white p-6 rounded shadow">
              <h3 className="text-xl font-semibold mb-2">Metodología</h3>
              <p>Identificación de fuentes de datos españolas, creación de conexiones API y desarrollo de scripts para automatizar la obtención de datos.</p>
            </div>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">Fuentes de Datos</h2>
          <p className="mb-4">Se han identificado las siguientes fuentes oficiales para obtener datos españoles equivalentes a los utilizados en PolicySpace2:</p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded shadow h-full">
              <h3 className="text-xl font-semibold mb-2">INE</h3>
              <h4 className="text-gray-600 mb-2">Instituto Nacional de Estadística</h4>
              <p className="mb-4">Proporciona datos demográficos, económicos y sociales oficiales de España a través de su API JSON.</p>
              <a href="https://www.ine.es/dyngs/DAB/index.htm?cid=1099" className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">Acceder a la API</a>
            </div>
            <div className="bg-white p-6 rounded shadow h-full">
              <h3 className="text-xl font-semibold mb-2">DataBank</h3>
              <h4 className="text-gray-600 mb-2">Banco Mundial</h4>
              <p className="mb-4">Proporciona indicadores económicos y de desarrollo para España y otros países.</p>
              <a href="https://datos.bancomundial.org/" className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">Acceder a DataBank</a>
            </div>
            <div className="bg-white p-6 rounded shadow h-full">
              <h3 className="text-xl font-semibold mb-2">Ministerio de Hacienda</h3>
              <h4 className="text-gray-600 mb-2">Gobierno de España</h4>
              <p className="mb-4">Proporciona datos de financiación municipal y otros indicadores fiscales.</p>
              <a href="https://www.hacienda.gob.es/es-ES/CDI/Paginas/SistemasFinanciacionDeuda/InformacionEELLs/DatosFinanciacionEL.aspx" className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">Acceder a los datos</a>
            </div>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">Equivalencias de Datos</h2>
          <p className="mb-4">A continuación se muestra una tabla con las equivalencias entre los archivos originales de PolicySpace2 y sus contrapartes españolas:</p>
          
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white">
              <thead className="bg-blue-100">
                <tr>
                  <th className="py-2 px-4 border-b text-left">Archivo Original</th>
                  <th className="py-2 px-4 border-b text-left">Archivo Español</th>
                  <th className="py-2 px-4 border-b text-left">Fuente</th>
                  <th className="py-2 px-4 border-b text-left">Descripción</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="py-2 px-4 border-b">ACPs_BR.csv</td>
                  <td className="py-2 px-4 border-b">municipios_codigos_espana.csv</td>
                  <td className="py-2 px-4 border-b">INE API</td>
                  <td className="py-2 px-4 border-b">Códigos de comunidades autónomas y provincias</td>
                </tr>
                <tr>
                  <td className="py-2 px-4 border-b">ACPs_MUN_CODES.csv</td>
                  <td className="py-2 px-4 border-b">municipios_codigos_espana.csv</td>
                  <td className="py-2 px-4 border-b">INE API</td>
                  <td className="py-2 px-4 border-b">Códigos de municipios</td>
                </tr>
                <tr>
                  <td className="py-2 px-4 border-b">RM_BR_STATES.csv</td>
                  <td className="py-2 px-4 border-b">municipios_codigos_espana.csv</td>
                  <td className="py-2 px-4 border-b">INE API</td>
                  <td className="py-2 px-4 border-b">Relación de municipios por provincias</td>
                </tr>
                <tr>
                  <td className="py-2 px-4 border-b">estimativas_pop.csv</td>
                  <td className="py-2 px-4 border-b">poblacion_municipio_sexo_edad_2021.csv</td>
                  <td className="py-2 px-4 border-b">INE API</td>
                  <td className="py-2 px-4 border-b">Cifras de población por municipios</td>
                </tr>
                <tr>
                  <td className="py-2 px-4 border-b">firms_by_APs*.csv</td>
                  <td className="py-2 px-4 border-b">empresas_por_municipio.csv</td>
                  <td className="py-2 px-4 border-b">INE API</td>
                  <td className="py-2 px-4 border-b">Empresas por municipio</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <p className="mt-4">
            <Link href="/downloads/equivalencias_archivos.csv" className="text-blue-600 hover:underline">
              Descargar lista completa de equivalencias
            </Link>
          </p>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">Scripts Desarrollados</h2>
          <p className="mb-4">Se han desarrollado los siguientes scripts Python para automatizar la obtención de datos españoles:</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded shadow">
              <h3 className="text-xl font-semibold mb-2">adaptar_policyspace2_espana.py</h3>
              <p className="mb-4">Script principal que integra todos los módulos con una interfaz de línea de comandos.</p>
              <pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto">
                <code>python adaptar_policyspace2_espana.py</code>
              </pre>
            </div>
            <div className="bg-white p-6 rounded shadow">
              <h3 className="text-xl font-semibold mb-2">ine_api.py</h3>
              <p className="mb-4">Módulo para conectar con la API JSON del INE (Instituto Nacional de Estadística).</p>
              <pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto">
                <code>{`from ine_api import INE_API
ine = INE_API()
municipios = ine.get_municipalities()`}</code>
              </pre>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
            <div className="bg-white p-6 rounded shadow">
              <h3 className="text-xl font-semibold mb-2">databank_api.py</h3>
              <p className="mb-4">Módulo para conectar con la API de DataBank del Banco Mundial.</p>
              <pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto">
                <code>{`from databank_api import DataBankAPI
databank = DataBankAPI()
gdp = databank.get_gdp_data()`}</code>
              </pre>
            </div>
            <div className="bg-white p-6 rounded shadow">
              <h3 className="text-xl font-semibold mb-2">descargar_documentos_alternativos.py</h3>
              <p className="mb-4">Módulo para descargar datos no disponibles mediante APIs.</p>
              <pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto">
                <code>{`import descargar_documentos_alternativos
descargar_documentos_alternativos.main()`}</code>
              </pre>
            </div>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">Descargas</h2>
          <p className="mb-4">Descargue los scripts y documentación necesarios para adaptar PolicySpace2 al contexto español:</p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded shadow text-center">
              <h3 className="text-xl font-semibold mb-2">Scripts Python</h3>
              <p className="mb-4">Todos los scripts Python desarrollados para el proyecto.</p>
              <Link href="/downloads/scripts_policyspace2_espana.zip" className="bg-blue-600 text-white px-4 py-2 rounded inline-block hover:bg-blue-700">
                Descargar Scripts
              </Link>
            </div>
            <div className="bg-white p-6 rounded shadow text-center">
              <h3 className="text-xl font-semibold mb-2">Documentación</h3>
              <p className="mb-4">Guía de uso y documentación del proyecto.</p>
              <Link href="/guia_uso.md" className="bg-blue-600 text-white px-4 py-2 rounded inline-block hover:bg-blue-700">
                Descargar Guía
              </Link>
            </div>
            <div className="bg-white p-6 rounded shadow text-center">
              <h3 className="text-xl font-semibold mb-2">Fuentes de Datos</h3>
              <p className="mb-4">Documento con las equivalencias entre datos brasileños y españoles.</p>
              <Link href="/fuentes_datos_espanolas.md" className="bg-blue-600 text-white px-4 py-2 rounded inline-block hover:bg-blue-700">
                Descargar Documento
              </Link>
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold mb-4">Guía de Uso</h2>
          <div className="bg-white p-6 rounded shadow">
            <h3 className="text-xl font-semibold mb-2">Requisitos Previos</h3>
            <ul className="list-disc pl-6 mb-4">
              <li>Python 3.6 o superior</li>
              <li>Bibliotecas requeridas: pandas, requests, beautifulsoup4</li>
              <li>Conexión a Internet para acceder a las APIs</li>
            </ul>
            
            <h3 className="text-xl font-semibold mb-2">Instalación</h3>
            <ol className="list-decimal pl-6 mb-4">
              <li>Descargue todos los archivos Python en un mismo directorio</li>
              <li>Instale las dependencias necesarias:</li>
            </ol>
            <pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto mb-4">
              <code>pip install pandas requests beautifulsoup4</code>
            </pre>
            
            <h3 className="text-xl font-semibold mb-2">Uso del Script Principal</h3>
            <p className="mb-2">Para obtener todos los datos españoles equivalentes a los utilizados en PolicySpace2:</p>
            <pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto mb-4">
              <code>python adaptar_policyspace2_espana.py</code>
            </pre>
            <p>Esto ejecutará todos los módulos y guardará los resultados en el directorio <code>datos_espana</code>.</p>
          </div>
        </section>
      </main>

      <footer className="bg-gray-800 text-white py-6">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h3 className="text-lg font-semibold mb-2">PolicySpace2 - Adaptación al Contexto Español</h3>
              <p>Proyecto para adaptar PolicySpace2 al mercado español, recopilando datos equivalentes a los utilizados en el contexto brasileño original.</p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">Enlaces</h3>
              <ul>
                <li><a href="#" className="text-gray-300 hover:text-white">Introducción</a></li>
                <li><a href="#" className="text-gray-300 hover:text-white">Fuentes de Datos</a></li>
                <li><a href="#" className="text-gray-300 hover:text-white">Equivalencias</a></li>
                <li><a href="#" className="text-gray-300 hover:text-white">Scripts</a></li>
                <li><a href="#" className="text-gray-300 hover:text-white">Descargas</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">Recursos</h3>
              <ul>
                <li><a href="https://www.ine.es/" className="text-gray-300 hover:text-white" target="_blank" rel="noopener noreferrer">INE</a></li>
                <li><a href="https://datos.bancomundial.org/" className="text-gray-300 hover:text-white" target="_blank" rel="noopener noreferrer">Banco Mundial</a></li>
                <li><a href="https://www.hacienda.gob.es/" className="text-gray-300 hover:text-white" target="_blank" rel="noopener noreferrer">Ministerio de Hacienda</a></li>
              </ul>
            </div>
          </div>
          <hr className="border-gray-600 my-4" />
          <div className="text-center">
            <p>© 2025 PolicySpace2 España</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
