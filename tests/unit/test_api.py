"""
Tests unitarios para la API FastAPI.

Tests básicos de endpoints y funcionalidad core de la API.
"""

import pytest
from fastapi import status


class TestHealthEndpoints:
    """Tests para endpoints de salud y estado."""

    def test_root_endpoint(self, api_client):
        """Test del endpoint raíz."""
        response = api_client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "0.1.0"

    def test_health_check_endpoint(self, api_client):
        """Test del endpoint de health check."""
        response = api_client.get("/api/v1/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "0.1.0"
        assert data["service"] == "policyspace2-api"

    def test_api_info_endpoint(self, api_client):
        """Test del endpoint de información de la API."""
        response = api_client.get("/api/v1/info")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "endpoints" in data
        assert "data_coverage" in data


class TestAPIDocumentation:
    """Tests para documentación automática de la API."""

    def test_openapi_schema_available(self, api_client):
        """Test que el schema OpenAPI está disponible."""
        response = api_client.get("/api/openapi.json")
        assert response.status_code == status.HTTP_200_OK
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "PolicySpace2 Spanish Data API"

    def test_swagger_docs_available(self, api_client):
        """Test que Swagger UI está disponible."""
        response = api_client.get("/api/docs")
        assert response.status_code == status.HTTP_200_OK

    def test_redoc_available(self, api_client):
        """Test que ReDoc está disponible."""
        response = api_client.get("/api/redoc")
        assert response.status_code == status.HTTP_200_OK


class TestCORS:
    """Tests para configuración CORS."""

    def test_cors_headers_present(self, api_client):
        """Test que los headers CORS están presentes."""
        response = api_client.options(
            "/api/v1/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        # CORS headers deberían estar presentes
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]


# TODO: Añadir más tests cuando se implementen endpoints
# class TestMunicipiosEndpoints:
#     """Tests para endpoints de municipios."""
#     pass
#
# class TestPoblacionEndpoints:
#     """Tests para endpoints de población."""
#     pass
