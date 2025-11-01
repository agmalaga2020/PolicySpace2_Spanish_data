# 🤝 Guía de Contribución - PolicySpace2 España

¡Gracias por tu interés en contribuir al proyecto PolicySpace2 España! Esta guía te ayudará a participar de manera efectiva en el desarrollo del proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo Puedo Contribuir?](#cómo-puedo-contribuir)
- [Configuración del Entorno de Desarrollo](#configuración-del-entorno-de-desarrollo)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Guía de Estilo](#guía-de-estilo)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas un ambiente respetuoso y constructivo para todos los colaboradores.

## 🎯 ¿Cómo Puedo Contribuir?

Hay muchas formas de contribuir al proyecto:

### 1. 🐛 Reportar Bugs
- Usa la plantilla de issues para reportar bugs
- Incluye pasos detallados para reproducir el problema
- Proporciona información sobre tu entorno (OS, versión de Python, etc.)

### 2. 💡 Sugerir Mejoras
- Revisa primero los issues existentes para evitar duplicados
- Explica claramente el caso de uso y los beneficios
- Considera el alcance y la complejidad de la implementación

### 3. 📝 Mejorar Documentación
- Corregir errores tipográficos o gramaticales
- Añadir ejemplos y casos de uso
- Mejorar explicaciones técnicas
- Traducir documentación

### 4. 💻 Contribuir Código
- Implementar nuevas funcionalidades
- Corregir bugs existentes
- Optimizar rendimiento
- Añadir tests

### 5. 📊 Mejorar Procesos ETL
- Actualizar fuentes de datos
- Mejorar limpieza de datos
- Añadir nuevas transformaciones
- Validar calidad de datos

## 🛠️ Configuración del Entorno de Desarrollo

### Requisitos Previos

- Python 3.8 o superior
- Git
- pip o conda

### Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/agmalaga2020/PolicySpace2_Spanish_data.git
   cd PolicySpace2_Spanish_data
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar dependencias del dashboard (opcional):**
   ```bash
   cd dashboard
   pip install -r requirements.txt
   ```

5. **Verificar la instalación:**
   ```bash
   python check_database_health.py
   ```

## 📁 Estructura del Proyecto

```
PolicySpace2_Spanish_data/
├── ETL/                          # Procesos de extracción, transformación y carga
│   ├── empresas_municipio_actividad_principal/
│   ├── estimativas_pop/
│   ├── df_mortalidad_ccaa_sexo/
│   └── ...                       # Otros procesos ETL
├── dashboard/                    # Dashboard Streamlit
│   ├── app.py                    # Aplicación principal
│   ├── pages/                    # Páginas adicionales
│   ├── assets/                   # Recursos estáticos
│   └── requirements.txt
├── data base/                    # Base de datos
│   └── datawarehouse.db
├── Papers/                       # Documentos académicos
├── transformaciones/             # Scripts de transformación
├── *.py                          # Scripts principales
├── *.md                          # Documentación
├── requirements.txt              # Dependencias del proyecto
└── README.md                     # Documentación principal
```

## 🎨 Guía de Estilo

### Python

1. **Seguir PEP 8:**
   - Indentación de 4 espacios
   - Líneas de máximo 79-88 caracteres
   - Nombres de variables en snake_case
   - Nombres de clases en PascalCase

2. **Documentación:**
   ```python
   def funcion_ejemplo(parametro1, parametro2):
       """
       Breve descripción de la función.
       
       Args:
           parametro1 (tipo): Descripción del parámetro
           parametro2 (tipo): Descripción del parámetro
           
       Returns:
           tipo: Descripción del valor retornado
           
       Raises:
           ExcepcionTipo: Cuándo se lanza la excepción
       """
       pass
   ```

3. **Comentarios:**
   - Escribe comentarios claros y concisos
   - Explica el "por qué", no solo el "qué"
   - Actualiza los comentarios cuando cambies el código

### Notebooks Jupyter

1. **Estructura clara:**
   - Título y descripción al inicio
   - Secciones bien definidas con markdown
   - Conclusiones al final

2. **Código limpio:**
   - Elimina celdas de prueba antes de commit
   - Limpia outputs si son muy grandes
   - Documenta cada paso del proceso

### SQL

1. **Convenciones:**
   - Palabras clave en MAYÚSCULAS
   - Nombres de tablas y columnas en snake_case
   - Indentación consistente

## 🔄 Proceso de Pull Request

1. **Crear una rama:**
   ```bash
   git checkout -b feature/nombre-descriptivo
   # o
   git checkout -b fix/nombre-del-bug
   ```

2. **Hacer commits atómicos:**
   ```bash
   git add archivo_modificado.py
   git commit -m "feat: agregar función de validación de datos"
   ```

3. **Seguir convención de commits:**
   - `feat:` nueva funcionalidad
   - `fix:` corrección de bug
   - `docs:` cambios en documentación
   - `style:` formato, sin cambios en código
   - `refactor:` refactorización de código
   - `test:` añadir o modificar tests
   - `chore:` cambios en build, dependencias, etc.

4. **Actualizar tu rama:**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

5. **Push y crear PR:**
   ```bash
   git push origin feature/nombre-descriptivo
   ```
   
6. **Descripción del PR:**
   - Título claro y descriptivo
   - Descripción detallada de los cambios
   - Referencias a issues relacionados (#123)
   - Screenshots si hay cambios visuales
   - Lista de verificación de pruebas realizadas

## 🐛 Reportar Bugs

Cuando reportes un bug, incluye:

1. **Descripción clara y concisa** del problema
2. **Pasos para reproducir:**
   - Paso 1
   - Paso 2
   - ...
3. **Comportamiento esperado:** Qué debería suceder
4. **Comportamiento actual:** Qué está sucediendo
5. **Screenshots** (si aplica)
6. **Entorno:**
   - OS: [e.g. Ubuntu 22.04]
   - Python: [e.g. 3.10.5]
   - Versión del proyecto: [e.g. commit hash]
7. **Contexto adicional:** Cualquier información relevante

## 💡 Sugerir Mejoras

Para sugerir una mejora:

1. **Título descriptivo:** Resumen de la mejora en una línea
2. **Problema a resolver:** ¿Qué problema actual aborda?
3. **Solución propuesta:** ¿Cómo resolver el problema?
4. **Alternativas consideradas:** Otras opciones evaluadas
5. **Impacto:** ¿A quién beneficia y cómo?
6. **Implementación:** Complejidad estimada y pasos necesarios

## 📊 Trabajar con Datos

### Añadir Nuevas Fuentes de Datos

1. Documentar la fuente en `fuentes_datos_espanolas.md`
2. Crear notebook ETL en carpeta correspondiente en `ETL/`
3. Documentar proceso de limpieza y transformación
4. Añadir validaciones de calidad de datos
5. Actualizar `equivalencias_datos_espana.csv`

### Actualizar Datos Existentes

1. Verificar compatibilidad con esquema actual
2. Documentar cambios en el notebook ETL
3. Ejecutar validaciones de calidad
4. Actualizar visualizaciones afectadas

## ✅ Checklist antes de Enviar PR

- [ ] El código sigue la guía de estilo del proyecto
- [ ] He añadido documentación para nuevas funcionalidades
- [ ] He actualizado la documentación existente si es necesario
- [ ] Mis cambios no generan nuevos warnings
- [ ] He añadido tests para cubrir mis cambios (si aplica)
- [ ] Todos los tests pasan exitosamente
- [ ] He verificado que no hay problemas con el health check de la BD
- [ ] He actualizado el archivo TODO.md si es relevante
- [ ] El PR tiene una descripción clara y completa

## 📞 ¿Necesitas Ayuda?

- Revisa la [documentación del proyecto](README.md)
- Consulta los [issues existentes](https://github.com/agmalaga2020/PolicySpace2_Spanish_data/issues)
- Lee la [guía de uso](guia_uso.md)
- Contacta a los maintainers del proyecto

## 🙏 Agradecimientos

¡Gracias por contribuir a PolicySpace2 España! Tu trabajo ayuda a mejorar el análisis y simulación de políticas públicas en España.

---

**Nota:** Esta guía está en constante evolución. Si encuentras formas de mejorarla, ¡no dudes en contribuir!
