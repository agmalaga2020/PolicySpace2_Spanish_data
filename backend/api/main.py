"""
FastAPI application entry point.

Este archivo contiene la configuración principal de la aplicación FastAPI,
incluyendo middleware, CORS, y la inclusión de routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="PolicySpace2 Spanish Data API",
    description="""
    API REST para acceder a datos socioeconómicos de España procesados
    para análisis de políticas públicas y simulaciones.

    ## Características

    * **Municipios**: Datos de más de 2000 municipios españoles
    * **Población**: Series temporales de población
    * **Empresas**: Datos de empresas por municipio y sector
    * **PIE**: Finanzas municipales (liquidaciones)
    * **IDHM**: Índice de Desarrollo Humano Municipal
    * **Analytics**: Análisis avanzados y correlaciones

    ## Fuentes de Datos

    - INE (Instituto Nacional de Estadística)
    - Banco de España
    - Ministerio de Hacienda
    - Eurostat
    """,
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8501",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Comprimir respuestas
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz de la API.

    Returns:
        dict: Información básica de la API
    """
    return {
        "message": "PolicySpace2 Spanish Data API",
        "version": "0.1.0",
        "docs": "/api/docs",
        "health": "/api/v1/health"
    }


@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint para monitoreo.

    Returns:
        dict: Estado de salud de la API
    """
    return {
        "status": "healthy",
        "version": "0.1.0",
        "service": "policyspace2-api"
    }


@app.get("/api/v1/info", tags=["Info"])
async def api_info():
    """
    Información detallada sobre la API.

    Returns:
        dict: Metadatos de la API
    """
    return {
        "name": "PolicySpace2 Spanish Data API",
        "version": "0.1.0",
        "description": "API para análisis de datos socioeconómicos de España",
        "endpoints": {
            "municipios": "/api/v1/municipios",
            "poblacion": "/api/v1/poblacion",
            "empresas": "/api/v1/empresas",
            "pie": "/api/v1/pie",
            "idhm": "/api/v1/idhm",
            "analytics": "/api/v1/analytics"
        },
        "data_coverage": {
            "municipios": "2168+",
            "years": "2014-2020",
            "sources": ["INE", "Banco de España", "Ministerio de Hacienda"]
        }
    }


# TODO: Incluir routers cuando estén implementados
# from .routers import municipios, poblacion, empresas, pie, idhm, analytics
# app.include_router(municipios.router, prefix="/api/v1", tags=["municipios"])
# app.include_router(poblacion.router, prefix="/api/v1", tags=["poblacion"])
# app.include_router(empresas.router, prefix="/api/v1", tags=["empresas"])
# app.include_router(pie.router, prefix="/api/v1", tags=["pie"])
# app.include_router(idhm.router, prefix="/api/v1", tags=["idhm"])
# app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
