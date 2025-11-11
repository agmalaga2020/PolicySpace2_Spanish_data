"""
Configuración de pytest y fixtures compartidos.

Este archivo contiene fixtures globales y configuración para todos los tests.
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Añadir el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


@pytest.fixture
def api_client():
    """
    Cliente de prueba para la API FastAPI.

    Returns:
        TestClient: Cliente de prueba configurado
    """
    from backend.api.main import app
    return TestClient(app)


@pytest.fixture
def sample_municipio_data():
    """
    Datos de ejemplo de un municipio para tests.

    Returns:
        dict: Datos de municipio de ejemplo
    """
    return {
        "codigo": "28079",
        "nombre": "Madrid",
        "provincia": "Madrid",
        "comunidad": "Comunidad de Madrid",
        "poblacion": 3266126,
        "superficie_km2": 604.3
    }


@pytest.fixture
def sample_poblacion_data():
    """
    Datos de ejemplo de población para tests.

    Returns:
        dict: Datos de población de ejemplo
    """
    return {
        "municipio_codigo": "28079",
        "year": 2020,
        "poblacion_total": 3266126,
        "hombres": 1540810,
        "mujeres": 1725316
    }
