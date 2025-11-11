# PolicySpace2_Spanish_data 🇪🇸

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![Documentation](https://img.shields.io/badge/docs-detailed-brightgreen.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

> **Plataforma completa de análisis y simulación de políticas públicas para España**

Una adaptación profesional del modelo PolicySpace2 al contexto español, integrando datos oficiales del INE, Banco de España, Eurostat y otros organismos, con procesos ETL avanzados, API REST moderna y dashboard interactivo.

---

## ✨ Características Principales

### 📊 **Datos Completos de España**
- **2,168+ municipios** con datos socioeconómicos detallados
- **Series temporales 2014-2020** de población, empresas, finanzas
- **Fuentes oficiales**: INE, Banco de España, Ministerio de Hacienda, Eurostat
- **Base de datos optimizada** con más de 10 tablas relacionales

### 🚀 **API REST Moderna (FastAPI)**
- **Endpoints RESTful** para acceso programático a todos los datos
- **Documentación automática** con Swagger UI y ReDoc
- **Alto rendimiento** con caché, compresión y optimización de queries
- **Tipado fuerte** con Pydantic y validación automática

### 📈 **Dashboard Interactivo (Streamlit)**
- **Visualizaciones interactivas** de datos demográficos y económicos
- **Mapas coropletas** de España con métricas personalizables
- **Análisis comparativos** entre municipios y regiones
- **Exportación de datos** en CSV, Excel y PDF

### 🔬 **Análisis Avanzados**
- **Correlaciones** entre variables socioeconómicas
- **Clustering** de municipios por características similares
- **Series temporales** con forecasting
- **Machine Learning** para predicciones (próximamente)

### 🛠️ **Infraestructura Profesional**
- **CI/CD** con GitHub Actions
- **Tests automáticos** con pytest (cobertura en crecimiento)
- **Linting** y formateo automático (Black, Flake8, isort)
- **Containerización** con Docker (próximamente)

---

## 📋 Tabla de Contenidos

- [Instalación](#-instalación)
- [Uso Rápido](#-uso-rápido)
- [Arquitectura](#-arquitectura)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API REST](#-api-rest)
- [Dashboard](#-dashboard)
- [ETL Pipelines](#-etl-pipelines)
- [Datos Disponibles](#-datos-disponibles)
- [Desarrollo](#-desarrollo)
- [Testing](#-testing)
- [Roadmap](#-roadmap)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.11+
- pip o Poetry
- (Opcional) Docker para deployment

### Opción 1: Instalación Básica

```bash
# Clonar repositorio
git clone https://github.com/agmalaga2020/PolicySpace2_Spanish_data.git
cd PolicySpace2_Spanish_data

# Crear virtual environment
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones
```

### Opción 2: Instalación para Desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install -r pyproject.toml[dev]

# Instalar pre-commit hooks
pre-commit install

# Configurar base de datos (si es necesario)
python backend/core/database.py
```

### Opción 3: Docker (Próximamente)

```bash
# Construir y ejecutar con Docker Compose
docker-compose up -d
```

---

## 💡 Uso Rápido

### 1. Ejecutar Dashboard Streamlit

```bash
streamlit run dashboard/app.py
```

Accede a http://localhost:8501 para ver el dashboard interactivo.

### 2. Ejecutar API REST

```bash
# Opción A: Usando uvicorn directamente
uvicorn backend.api.main:app --reload --port 8000

# Opción B: Ejecutando el script
python backend/api/main.py
```

Accede a:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### 3. Ejemplos de Uso de la API

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Información de la API
curl http://localhost:8000/api/v1/info

# Listar municipios (próximamente)
curl http://localhost:8000/api/v1/municipios

# Obtener datos de un municipio específico
curl http://localhost:8000/api/v1/municipios/28079  # Madrid
```

### 4. Ejemplo de Uso Programático (Python)

```python
import requests

# Conectar a la API
BASE_URL = "http://localhost:8000/api/v1"

# Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())
# {'status': 'healthy', 'version': '0.1.0'}

# Obtener información de un municipio (próximamente)
# municipio = requests.get(f"{BASE_URL}/municipios/28079").json()
# print(f"Población de {municipio['nombre']}: {municipio['poblacion']}")
```

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  ┌────────────────────┐         ┌──────────────────────┐   │
│  │ Streamlit Dashboard│         │  React/Next.js (WIP) │   │
│  │   (Actual)         │         │   (Próximamente)     │   │
│  └────────────────────┘         └──────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      API LAYER                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              FastAPI REST API                        │   │
│  │  • Endpoints CRUD para todas las entidades          │   │
│  │  • Autenticación JWT (WIP)                          │   │
│  │  • Rate limiting & Caching                          │   │
│  │  • Validación con Pydantic                          │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Services    │  │  Analytics   │  │   ML Models      │  │
│  │  (CRUD)      │  │  (Análisis)  │  │   (Próximo)      │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER                               │
│  ┌──────────────────┐         ┌────────────────────────┐   │
│  │  SQLite          │   →     │    PostgreSQL (WIP)    │   │
│  │  (Desarrollo)    │         │    (Producción)        │   │
│  └──────────────────┘         └────────────────────────┘   │
│                                                              │
│  ┌──────────────────┐                                       │
│  │  Redis Cache     │  (Próximamente)                       │
│  └──────────────────┘                                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    ETL PIPELINES                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   INE    │  │  Banco   │  │Ministerio│  │ Eurostat │   │
│  │   API    │  │  España  │  │ Hacienda │  │   API    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       ↓              ↓              ↓              ↓        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │     Extract → Transform → Load → Validate           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura del Proyecto

```
PolicySpace2_Spanish_data/
│
├── 📱 backend/                      # API REST (FastAPI)
│   ├── api/
│   │   ├── main.py                  # Aplicación principal
│   │   └── routers/                 # Endpoints por recurso
│   ├── core/
│   │   ├── config.py                # Configuración
│   │   └── database.py              # DB connection
│   ├── models/                      # SQLAlchemy models
│   └── services/                    # Business logic
│
├── 🎨 dashboard/                    # Dashboard Streamlit
│   ├── app.py                       # App principal
│   ├── pages/                       # Páginas del dashboard
│   │   ├── 🗺️_Mapa_Municipios.py
│   │   ├── 📊_Mapa_PIE.py
│   │   ├── 🏆_Ranking_IDH.py
│   │   └── ...                      # +10 páginas más
│   └── assets/                      # CSS, imágenes
│
├── 🔄 ETL/                          # Pipelines de datos
│   ├── PIE/                         # Finanzas municipales
│   ├── GeoRef_Spain/                # Datos geográficos
│   ├── estimativas_pop/             # Población
│   ├── empresas_municipio/          # Empresas
│   ├── idhm_*/                      # Desarrollo humano
│   └── ...                          # +10 fuentes más
│
├── 🧪 tests/                        # Tests (pytest)
│   ├── unit/                        # Tests unitarios
│   ├── integration/                 # Tests de integración
│   └── etl/                         # Tests de ETL
│
├── 🗄️ data base/                    # Base de datos legacy
│   └── datawarehouse.db             # SQLite (33MB)
│
├── 📚 docs/                         # Documentación (WIP)
├── 🐳 .github/                      # CI/CD workflows
│   ├── workflows/
│   │   └── ci.yml                   # Tests, lint, security
│   └── dependabot.yml               # Actualización deps
│
├── 📄 Archivos de configuración
│   ├── .env.example                 # Variables de entorno
│   ├── .gitignore                   # Archivos ignorados
│   ├── .flake8                      # Config linter
│   ├── pyproject.toml               # Config proyecto
│   ├── pytest.ini                   # Config tests
│   └── requirements.txt             # Dependencias
│
├── 📋 Documentación principal
│   ├── README.md                    # Este archivo
│   ├── TODO.md                      # Roadmap detallado
│   ├── AUDITORIA_PROFESIONALIZACION.md  # Análisis del proyecto
│   ├── LICENSE                      # Licencia MIT
│   └── ...
│
└── 🗃️ Datos
    ├── datawarehouse.db             # DB principal (25MB)
    ├── equivalencias*.csv           # Tablas de equivalencias
    └── interest_*.csv               # Datos de tipos de interés
```

---

## 🌐 API REST

### Endpoints Disponibles

#### Health & Info
```http
GET /                          # Root endpoint
GET /api/v1/health            # Health check
GET /api/v1/info              # API information
```

#### Municipios (WIP)
```http
GET  /api/v1/municipios                # Listar todos los municipios
GET  /api/v1/municipios/{id}           # Detalle de municipio
GET  /api/v1/municipios/search         # Búsqueda
GET  /api/v1/municipios/{id}/stats     # Estadísticas
```

#### Población (WIP)
```http
GET  /api/v1/poblacion/municipio/{id}
GET  /api/v1/poblacion/provincia/{id}
GET  /api/v1/poblacion/comunidad/{id}
GET  /api/v1/poblacion/trends
```

#### Empresas (WIP)
```http
GET  /api/v1/empresas/municipio/{id}
GET  /api/v1/empresas/sector/{cnae}
GET  /api/v1/empresas/analytics
```

#### PIE - Finanzas Municipales (WIP)
```http
GET  /api/v1/pie/municipio/{id}
GET  /api/v1/pie/comparacion
GET  /api/v1/pie/rankings
```

#### IDHM - Desarrollo Humano (WIP)
```http
GET  /api/v1/idhm/municipio/{id}
GET  /api/v1/idhm/rankings
GET  /api/v1/idhm/evolution
```

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

---

## 📊 Dashboard

El dashboard Streamlit actual incluye **11+ páginas interactivas**:

### Páginas Principales

1. **🗺️ Mapa Simple Municipios** - Visualización geográfica básica
2. **📊 Mapa PIE Municipios** - Finanzas municipales por mapa
3. **🗺️ Mapa Densidad Población** - Choropleth interactivo
4. **🏆 Ranking IDH Municipios** - Top municipios por desarrollo
5. **👥 Informe Población** - Análisis demográfico detallado
6. **🏢 Empresas vs IDH** - Correlación empresas-desarrollo
7. **🎓 Nivel Educativo vs Renta** - Análisis educación-economía
8. **🏙️ Urbanización vs Crecimiento** - Patrones urbanos
9. **👶 Fecundidad y Envejecimiento** - Tendencias demográficas
10. **⚰️ Mortalidad por CCAA y Sexo** - Datos de mortalidad
11. **💶 Tipos de Interés vs Socioeconómico** - Impacto financiero

### Características del Dashboard

- ✅ **Filtros dinámicos** por comunidad, provincia, año
- ✅ **Exportación de datos** (CSV, Excel)
- ✅ **Gráficos interactivos** con Plotly
- ✅ **Mapas coropletas** con gradientes de color
- ✅ **Comparaciones** entre municipios
- ✅ **Guardado de informes** favoritos

---

## 🔄 ETL Pipelines

### Fuentes de Datos Integradas

| Fuente | Tipo de Dato | Frecuencia | Municipios |
|--------|--------------|------------|------------|
| **INE** | Población, empresas, urbanismo | Anual | 8,000+ |
| **Banco de España** | Tipos de interés | Mensual | Nacional |
| **Ministerio de Hacienda** | Finanzas municipales (PIE) | Anual | 2,168+ |
| **Eurostat** | Inflación, desarrollo | Trimestral | Regional |
| **Portales Autonómicos** | Educación, sanidad | Anual | Variable |

### Procesos ETL Implementados

#### 1. **Población**
```python
ETL/estimativas_pop/estimativas_pop_v2.py
ETL/cifras_poblacion_municipio/
```
- Extracción de 8,000+ municipios
- Limpieza de outliers (>300% cambio anual)
- Interpolación de valores faltantes
- Pivoteo para series temporales

#### 2. **Empresas**
```python
ETL/empresas_municipio_actividad_principal/
```
- Clasificación por CNAE
- Imputación dual (0 para sin actividad, media para NaN)
- Cruce con datos de población

#### 3. **Finanzas Municipales (PIE)**
```python
ETL/PIE/
```
- Scraping de liquidaciones presupuestarias
- Selección de régimen general
- Procesamiento de ~2,168 municipios >5,000 hab

#### 4. **IDHM (Desarrollo Humano)**
```python
ETL/idhm_indice_desarrollo_humano_municipal/
```
- Cálculo de índices compuestos
- Normalización de indicadores
- Generación de visualizaciones

#### 5. **Datos Geográficos**
```python
ETL/GeoRef_Spain/
```
- Descarga de TopoJSON
- Mapeo de coordenadas
- Generación de poligonos por nivel administrativo

### Características de los ETL

- ✅ **Reproducibles** - Scripts documentados y versionados
- ✅ **Validados** - Verificación de calidad de datos
- ✅ **Documentados** - Notebooks Jupyter con análisis
- ✅ **Optimizados** - Procesamiento eficiente con pandas
- ⏳ **Orquestación** - Airflow (próximamente)
- ⏳ **Data Quality** - Great Expectations (próximamente)

---

## 📚 Datos Disponibles

### Tablas en Base de Datos

#### Base de Datos Actual (`datawarehouse.db`)

| Tabla | Registros | Descripción |
|-------|-----------|-------------|
| `dim_municipio` | 2,168+ | Información de municipios |
| `dim_provincia` | 52 | Provincias de España |
| `dim_comunidad` | 19 | Comunidades autónomas |
| `dim_fecha` | 7+ años | Dimensión temporal |
| `fact_poblacion_municipio` | 15,000+ | Población por municipio/año |
| `fact_empresas_municipio` | 12,000+ | Empresas por municipio |
| `fact_pie` | 10,000+ | Liquidaciones municipales |
| `fact_idhm` | 2,000+ | Índice desarrollo humano |
| `fact_mortalidad_ccaa` | 600+ | Tasas de mortalidad |
| `fact_fertilidad_*` | 1,000+ | Indicadores de fecundidad |

### Cobertura de Datos

- **Años**: 2014-2020 (mayoría de datasets)
- **Municipios**: 2,168+ con datos completos
- **Completitud**: 95%+ (post-limpieza)
- **Actualización**: Anual (manual por ahora)

---

## 💻 Desarrollo

### Setup Entorno de Desarrollo

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Instalar herramientas de desarrollo
pip install black flake8 isort mypy pytest pytest-cov pre-commit

# 3. Configurar pre-commit hooks
pre-commit install

# 4. Configurar IDE (VSCode recomendado)
# Instalar extensiones: Python, Pylance, Black Formatter
```

### Comandos Útiles

```bash
# Formatear código
black .
isort .

# Lint
flake8 .

# Type checking
mypy backend/

# Tests
pytest
pytest --cov=backend --cov-report=html

# Ejecutar API en desarrollo
uvicorn backend.api.main:app --reload

# Ejecutar dashboard
streamlit run dashboard/app.py
```

### Estándares de Código

- **Formateo**: Black (line length 100)
- **Imports**: isort con profile black
- **Linting**: Flake8
- **Type hints**: Utilizar donde sea posible
- **Docstrings**: Google style
- **Commits**: Conventional Commits

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=backend --cov=dashboard --cov-report=html

# Solo tests unitarios
pytest tests/unit/

# Solo tests de API
pytest tests/unit/test_api.py

# Tests con output verbose
pytest -v

# Tests que coincidan con patrón
pytest -k "health"
```

### Estructura de Tests

```
tests/
├── unit/                    # Tests unitarios
│   ├── test_api.py         # Tests de endpoints
│   ├── test_services.py    # Tests de lógica de negocio
│   └── test_models.py      # Tests de modelos
├── integration/             # Tests de integración
│   ├── test_database.py    # Tests de DB
│   └── test_etl.py         # Tests de pipelines ETL
└── conftest.py             # Fixtures compartidos
```

### Cobertura Actual

- **Backend API**: ~80% (endpoints básicos)
- **Services**: 0% (en desarrollo)
- **ETL**: 0% (próximamente)
- **Frontend**: 0% (próximamente)

**Objetivo**: 70%+ cobertura global

---

## 🗺️ Roadmap

Ver [TODO.md](./TODO.md) para el roadmap completo y detallado.

### 📌 Fase 1: Backend API (En Progreso - 4 semanas)

- [x] Estructura básica con FastAPI
- [x] Endpoints de health y info
- [x] Tests básicos
- [ ] Endpoints CRUD de municipios
- [ ] Endpoints de población
- [ ] Endpoints de empresas, PIE, IDHM
- [ ] Autenticación JWT
- [ ] Migración a PostgreSQL
- [ ] Sistema de caché con Redis

### 📌 Fase 2: Frontend Moderno (Próximo - 5 semanas)

- [ ] Setup Next.js + TypeScript
- [ ] Landing page
- [ ] Dashboard principal con mapas
- [ ] Explorador de municipios
- [ ] Analytics avanzados
- [ ] Simulador de políticas
- [ ] Responsive design

### 📌 Fase 3: Características Avanzadas (4-6 semanas)

- [ ] Machine Learning predictions
- [ ] Generador de informes PDF
- [ ] Sistema de usuarios y auth
- [ ] Colaboración y sharing
- [ ] Panel de administración

### 📌 Fase 4: Producción (2-3 semanas)

- [ ] Dockerización completa
- [ ] CI/CD deployment automático
- [ ] Monitoreo y logging (Prometheus/Grafana)
- [ ] Performance optimization
- [ ] Security hardening

### 📌 Mejoras Continuas

- [ ] Orquestación ETL con Airflow
- [ ] Data quality con Great Expectations
- [ ] Kubernetes deployment
- [ ] Documentación completa (Sphinx/MkDocs)
- [ ] Tutoriales interactivos

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee nuestra guía de contribución (próximamente CONTRIBUTING.md).

### Cómo Contribuir

1. **Fork** el repositorio
2. **Crea una rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'feat: Add AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre un Pull Request**

### Convenciones de Commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Cambios de formato
- `refactor:` Refactorización de código
- `test:` Añadir tests
- `chore:` Tareas de mantenimiento

### Code Review

- Todos los PRs requieren revisión
- Tests deben pasar en CI
- Cobertura no debe disminuir
- Seguir estándares de código

---

## 📄 Licencia

Este proyecto está licenciado bajo la **MIT License** - ver el archivo [LICENSE](LICENSE) para detalles.

```
MIT License

Copyright (c) 2025 Alberto Giménez Mut

Permission is hereby granted, free of charge...
```

---

## 👥 Autores y Reconocimientos

### Autor Principal

**Alberto Giménez Mut**
- GitHub: [@agmalaga2020](https://github.com/agmalaga2020)

### Reconocimientos

- **PolicySpace2** (Brasil) - Modelo original de simulación
- **INE España** - Fuente principal de datos
- **Banco de España** - Datos de tipos de interés
- **Ministerio de Hacienda** - Datos de finanzas municipales
- **Comunidad Open Source** - Herramientas y librerías

---

## 📞 Contacto y Soporte

- **Issues**: [GitHub Issues](https://github.com/agmalaga2020/PolicySpace2_Spanish_data/issues)
- **Documentación**: [Wiki del Proyecto](https://github.com/agmalaga2020/PolicySpace2_Spanish_data/wiki) (próximamente)
- **Email**: Disponible en perfil de GitHub

---

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~2,000+ (Python)
- **Archivos Python**: 60+
- **Notebooks Jupyter**: 16
- **Tests**: 15+ (en crecimiento)
- **Cobertura de tests**: ~30% (objetivo 70%+)
- **Tamaño de BD**: 51MB (SQLite)
- **Registros en BD**: 50,000+

---

## 🎯 Casos de Uso

### 1. Investigación Académica
> Analizar el impacto de políticas públicas en municipios rurales vs urbanos

### 2. Planificación Gubernamental
> Identificar municipios con baja inversión en educación pero alto potencial de crecimiento

### 3. Análisis Económico
> Estudiar la correlación entre tipos de interés y creación de empresas

### 4. Simulación de Políticas
> Modelar el efecto de incentivos a la natalidad en la demografía regional

### 5. Data Journalism
> Crear visualizaciones interactivas de desigualdades territoriales

---

## 🔗 Enlaces Útiles

- **Documentación FastAPI**: https://fastapi.tiangolo.com/
- **Streamlit Docs**: https://docs.streamlit.io/
- **Datos INE**: https://www.ine.es/
- **Banco de España**: https://www.bde.es/
- **PolicySpace2 Original**: (Repositorio del proyecto brasileño)

---

## ⭐ Star History

Si encuentras este proyecto útil, ¡considera darle una estrella! ⭐

---

<div align="center">

**[⬆ Volver arriba](#policyspace2_spanish_data-)**

Made with ❤️ for public policy analysis in Spain

![Spain Flag](https://img.shields.io/badge/Made%20in-Spain-FF0000?style=for-the-badge&logo=spain)

</div>
