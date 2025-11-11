# 📋 TODO PRINCIPAL - PolicySpace2_Spanish_data

**Última actualización:** 2025-11-11
**Estado del proyecto:** En desarrollo activo
**Nivel de profesionalismo:** Básico-Intermedio (34%) - Ver `AUDITORIA_PROFESIONALIZACION.md`

---

## 📊 RESUMEN DE ESTADO

### Tareas Completadas: ✅
- Adaptación inicial de PolicySpace2 al contexto español
- Implementación de ETL para múltiples fuentes de datos
- Dashboard Streamlit funcional
- Documentación básica del proyecto
- Base de datos creada y poblada

### Tareas Pendientes: ⏳
- **Profesionalización del código** (ver Fase 1-3 en auditoría)
- Completar database 2 con nuevo esquema
- Mejorar testing y CI/CD
- Dockerización completa

---

## 🔴 PRIORIDAD CRÍTICA (INMEDIATO - Semana 1-2)

### 1. Gestión de Dependencias
- [ ] **Fijar versiones en requirements.txt** (2h)
  - Estado actual: Solo nombres sin versiones ❌
  - Acción: `pip freeze > requirements-frozen.txt` y limpiar
  - Impacto: CRÍTICO - Proyecto no reproducible
  - Archivo: `requirements.txt`

### 2. Testing Básico
- [ ] **Crear estructura de tests** (1h)
  - `mkdir -p tests/{unit,integration,etl}`
  - Configurar pytest
  - Archivo: `tests/conftest.py`

- [ ] **Implementar tests unitarios básicos** (8-10h)
  - [ ] Tests para `ine_api.py`
  - [ ] Tests para `databank_api.py`
  - [ ] Tests para funciones ETL core
  - Target: 30% cobertura mínima

- [ ] **Configurar pytest-cov** (1h)
  - Instalar: `pip install pytest pytest-cov`
  - Crear: `pytest.ini`

### 3. CI/CD Básico
- [ ] **Crear GitHub Actions workflow** (4h)
  - Archivo: `.github/workflows/ci.yml`
  - Jobs: test, lint, security-scan
  - Triggers: push, pull_request

- [ ] **Configurar branch protection rules**
  - Require CI passing before merge
  - Require code review

### 4. Seguridad Básica
- [ ] **Mejorar .gitignore** (30min) ✅ COMPLETADO
  - Añadir patrones Python estándar
  - Añadir `.env`, `*.db`, `*.log`

- [ ] **Crear .env.example** (30min)
  - Documentar variables de entorno necesarias

- [ ] **Configurar Dependabot** (30min)
  - Archivo: `.github/dependabot.yml`
  - Escaneo semanal de dependencias

**Total Fase Crítica:** 16-20 horas

---

## 🟡 PRIORIDAD ALTA (Semana 3-4)

### 5. Calidad de Código
- [ ] **Configurar Black (formatter)** (2h)
  - Instalar y configurar en `pyproject.toml`
  - Formatear todo el código: `black .`

- [ ] **Configurar Flake8 (linter)** (2h)
  - Crear `.flake8`
  - Integrar en pre-commit

- [ ] **Configurar isort (imports)** (1h)
  - Configurar en `pyproject.toml`
  - Ordenar imports: `isort .`

- [ ] **Configurar pre-commit hooks** (2h)
  - Crear `.pre-commit-config.yaml`
  - Instalar: `pre-commit install`

### 6. Gestión de Proyecto
- [ ] **Crear pyproject.toml** (4h)
  - Migrar desde requirements.txt
  - Configurar metadata del proyecto
  - Configurar herramientas (black, pytest, mypy)

- [ ] **Crear setup.py o usar setuptools** (2h)
  - Hacer proyecto instalable
  - Definir entry points

### 7. Seguridad Avanzada
- [ ] **Implementar Bandit** (2h)
  - Instalar y configurar
  - Integrar en CI

- [ ] **Implementar Safety** (1h)
  - Escaneo de vulnerabilidades en dependencias
  - Integrar en CI

### 8. Expandir Tests
- [ ] **Tests de integración ETL** (8h)
  - Tests para pipelines completos
  - Validación de datos

- [ ] **Tests de validación de datos** (4h)
  - Schemas, tipos, rangos
  - Detección de outliers

- [ ] **Aumentar cobertura a 50%** (10h)

**Total Fase Alta:** 38 horas

---

## 🟢 PRIORIDAD MEDIA (Semana 5-8)

### 9. Containerización
- [ ] **Crear Dockerfile** (4h)
  - Multi-stage build
  - Optimizado para producción

- [ ] **Crear docker-compose.yml** (3h)
  - Servicio dashboard
  - Servicio ETL
  - Volúmenes para datos

- [ ] **Crear .dockerignore** (30min)

### 10. Automatización
- [ ] **Crear Makefile** (4h)
  - Comandos: install, test, lint, format, clean, docker-*

- [ ] **Crear scripts de setup** (2h)
  - `scripts/setup_env.sh`
  - `scripts/deploy.sh`

### 11. Documentación Avanzada
- [ ] **Crear CONTRIBUTING.md** (3h)
  - Guía de contribución
  - Estándares de código
  - Proceso de PR

- [ ] **Crear CHANGELOG.md** (2h)
  - Formato Keep a Changelog
  - Historial de versiones

- [ ] **Crear CODE_OF_CONDUCT.md** (1h)
  - Usar Contributor Covenant

- [ ] **Añadir badges al README** (1h)
  - License, Python version, Build status, Coverage

- [ ] **Configurar Sphinx/MkDocs** (4h)
  - Generación automática de docs

### 12. Reestructuración del Proyecto
- [ ] **Renombrar carpetas con espacios** (1h)
  - `data base` → `database_legacy`
  - `database 2` → `database_v2`

- [ ] **Crear estructura src/** (4h)
  - Mover código a `src/policyspace2/`
  - Crear `__init__.py` en cada módulo

- [ ] **Consolidar bases de datos** (3h)
  - Mover a `data/database/`
  - Actualizar rutas en código

- [ ] **Mover scripts sueltos** (2h)
  - Organizar en `scripts/`
  - Actualizar imports

**Total Fase Media:** 34 horas

---

## 🔵 MEJORA CONTINUA (Ongoing)

### Testing
- [ ] Aumentar cobertura a 70%+
- [ ] Implementar property-based testing (Hypothesis)
- [ ] Tests de performance

### Documentación
- [ ] Diagramas de arquitectura (Mermaid/PlantUML)
- [ ] Tutoriales paso a paso
- [ ] Video demos

### Calidad
- [ ] Configurar mypy strict
- [ ] Implementar logging estructurado
- [ ] Code complexity monitoring (radon)

### CI/CD
- [ ] Deployment automático a producción
- [ ] Staging environment
- [ ] Automated release notes

### Monitoreo
- [ ] Configurar observability
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring

---

## 📂 TAREAS POR COMPONENTE

### 🗄️ Database (`database 2/` - Ver database 2/TODO.md)

#### Estado General:
- ✅ Carpeta `database 2` creada
- ✅ Base de datos `datawarehouse.db` (51MB) poblada
- ✅ Script ETL `etl_load_data.py` creado
- ⚠️ Esquema relacional parcialmente implementado

#### Pendiente:
- [ ] **Completar tratamiento de datos específicos:**
  - [ ] Tamaño medio de hogares: implementar imputación 2014-2020
  - [ ] Datos no municipales: mapear usando tabla_equivalencias
  - [ ] Datos nacionales (interest_data): validar rangos de fechas

- [ ] **Generar esquema relacional actualizado:**
  - Referencia: `esquema_db_record_referencia.png`
  - Herramienta: SQLAlchemy + graphviz o similar

- [ ] **Validación de integridad:**
  - [ ] Tests de integridad referencial
  - [ ] Verificación de rangos de fechas (2014-2020)
  - [ ] Conteo de municipios (esperado: ~2168)

- [ ] **Documentación:**
  - [ ] Actualizar `info_tablas.md` con esquema final
  - [ ] Documentar proceso de migración

### 📊 Dashboard (Ver dashboard/TODO.md)

#### Estado General:
- ✅ Dashboard Streamlit funcional
- ✅ Múltiples páginas implementadas (11 páginas)
- ✅ Conexión a base de datos
- ✅ Visualizaciones con Plotly
- ✅ Exportación CSV/Excel
- ✅ Sistema de guardado de informes

#### Pendiente:
- [ ] **Optimización:**
  - [ ] Mejorar caching (`@st.cache_data`)
  - [ ] Lazy loading de datos grandes
  - [ ] Optimizar queries SQL

- [ ] **UX/UI:**
  - [ ] Añadir logo/branding
  - [ ] Mejorar responsive design
  - [ ] Añadir tooltips y ayuda contextual
  - [ ] Manejo de errores más robusto

- [ ] **Funcionalidades:**
  - [ ] Exportar informes como PDF/HTML
  - [ ] Comparación de escenarios
  - [ ] Filtros avanzados
  - [ ] Búsqueda de municipios

- [ ] **Tests:**
  - [ ] Tests unitarios para funciones de procesamiento
  - [ ] Tests de integración con base de datos

### 🔄 ETL Pipelines

#### Estado General:
- ✅ ETL para población (estimativas_pop)
- ✅ ETL para empresas
- ✅ ETL para PIE (finanzas municipales)
- ✅ ETL para mortalidad
- ✅ ETL para fecundidad
- ✅ ETL para nivel educativo
- ✅ ETL para distribución urbana
- ✅ ETL para IDHM
- ✅ ETL para tasas de interés

#### Pendiente:
- [ ] **Validación de datos:**
  - [ ] Implementar Great Expectations o Pandera
  - [ ] Tests de calidad de datos
  - [ ] Detección automática de anomalías

- [ ] **Orquestación:**
  - [ ] Implementar Airflow o Prefect
  - [ ] Definir DAGs de dependencias
  - [ ] Scheduling automático

- [ ] **Logging:**
  - [ ] Logging estructurado consistente
  - [ ] Tracking de métricas ETL
  - [ ] Alertas de fallos

- [ ] **Optimización:**
  - [ ] Paralelización de procesos
  - [ ] Incremental loading (no full refresh)
  - [ ] Particionamiento de datos

### 🌐 APIs (ine_api.py, databank_api.py)

#### Pendiente:
- [ ] **Robustez:**
  - [ ] Rate limiting
  - [ ] Retry logic con exponential backoff
  - [ ] Timeout handling
  - [ ] Circuit breaker pattern

- [ ] **Validación:**
  - [ ] Validación de respuestas API
  - [ ] Type hints completos
  - [ ] Documentación de endpoints

- [ ] **Testing:**
  - [ ] Tests con mocks (responses library)
  - [ ] Tests de integración (opcional, con API real)
  - [ ] Fixtures de datos de prueba

- [ ] **Caché:**
  - [ ] Implementar caché de respuestas API
  - [ ] Evitar llamadas duplicadas

---

## 🎯 METAS POR MILESTONE

### Milestone 1: "Production Ready" (8 semanas)
**Objetivo:** Proyecto listo para uso en producción

Criterios de éxito:
- ✅ Tests: 70%+ cobertura
- ✅ CI/CD: Pipeline completo funcionando
- ✅ Docker: Imagen publicada
- ✅ Documentación: Completa y actualizada
- ✅ Seguridad: Análisis automático implementado
- ✅ Código: Formateado y linted automáticamente

### Milestone 2: "Enterprise Grade" (16 semanas)
**Objetivo:** Proyecto nivel enterprise

Criterios adicionales:
- ✅ Tests: 80%+ cobertura
- ✅ Monitoreo: Observability implementado
- ✅ Performance: Optimizado y documentado
- ✅ Escalabilidad: Arquitectura escalable
- ✅ Documentación: API docs generados automáticamente

### Milestone 3: "Open Source Excellence" (24 semanas)
**Objetivo:** Proyecto ejemplar de código abierto

Criterios adicionales:
- ✅ Comunidad: CONTRIBUTING, CODE_OF_CONDUCT
- ✅ Tests: 90%+ cobertura
- ✅ Tutoriales: Múltiples guías y ejemplos
- ✅ CI/CD: Automated releases
- ✅ Internacionalización: Soporte multiidioma

---

## 📝 NOTAS Y DECISIONES

### Decisiones de Arquitectura:
1. **Base de datos:** SQLite para desarrollo, considerar PostgreSQL para producción
2. **Dashboard:** Streamlit (rápido desarrollo), considerar Dash/FastAPI+React para más control
3. **ETL:** Scripts Python actuales, migrar a Airflow/Prefect cuando escale

### Deuda Técnica Conocida:
1. Carpetas con espacios en nombres (`data base`, `database 2`)
2. Duplicación de bases de datos (raíz vs carpetas)
3. Estructura no sigue paquete Python estándar
4. Requirements sin versiones (CRÍTICO)
5. Logging inconsistente
6. Sin gestión de configuración centralizada

### Próximas Decisiones Necesarias:
- [ ] ¿Migrar a PostgreSQL o mantener SQLite?
- [ ] ¿Usar Poetry o pip-tools para dependencias?
- [ ] ¿Implementar Airflow para ETL?
- [ ] ¿Desplegar dashboard en Streamlit Cloud o servidor propio?

---

## 🔗 REFERENCIAS

- **Auditoría Completa:** `AUDITORIA_PROFESIONALIZACION.md`
- **TODOs Específicos:**
  - `database 2/TODO.md` - Tareas de base de datos
  - `dashboard/TODO.md` - Tareas del dashboard
  - `home/ubuntu/todo.md` - Tareas legacy de adaptación
- **Documentación:**
  - `README.md` - Documentación principal
  - `guia_uso.md` - Guía de uso
  - `fuentes_datos_espanolas.md` - Fuentes de datos

---

## ✅ CHECKLIST DE PROFESIONALIZACIÓN RÁPIDA

### Puedes hacer EN 1 DÍA:
- [ ] Fijar versiones en requirements.txt (2h)
- [ ] Mejorar .gitignore (30min) ✅
- [ ] Crear .env.example (30min)
- [ ] Configurar Dependabot (30min)
- [ ] Crear estructura de tests (1h)
- [ ] Añadir badges al README (30min)
- [ ] Corregir typo en LICENSE (5min)

**Total: ~5 horas - GRAN IMPACTO**

### Puedes hacer EN 1 SEMANA:
Todo lo anterior +
- [ ] Tests básicos (30% cobertura) - 10h
- [ ] GitHub Actions CI - 4h
- [ ] Configurar Black y Flake8 - 4h
- [ ] Pre-commit hooks - 2h

**Total: ~25 horas - TRANSFORMACIÓN SIGNIFICATIVA**

---

**Última actualización:** 2025-11-11
**Revisión recomendada:** Semanal durante Fase 1-3, mensual después
