// scripts.js - Funcionalidad para el sitio web de PolicySpace2 España

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Función para cargar y mostrar los datos de equivalencias
    function loadEquivalenciasData() {
        // En un entorno real, esto cargaría el CSV desde el servidor
        // Aquí simulamos los datos para la demostración
        const equivalencias = [
            {
                "archivo_original": "ACPs_BR.csv",
                "archivo_espana": "municipios_codigos_espana.csv",
                "fuente": "INE API",
                "descripcion": "Códigos de comunidades autónomas y provincias",
                "variables": "ID;ACPs;state_code"
            },
            {
                "archivo_original": "ACPs_MUN_CODES.csv",
                "archivo_espana": "municipios_codigos_espana.csv",
                "fuente": "INE API",
                "descripcion": "Códigos de municipios",
                "variables": "ACPs;cod_mun"
            },
            {
                "archivo_original": "RM_BR_STATES.csv",
                "archivo_espana": "municipios_codigos_espana.csv",
                "fuente": "INE API",
                "descripcion": "Relación de municipios por provincias",
                "variables": "codmun"
            },
            {
                "archivo_original": "estimativas_pop.csv",
                "archivo_espana": "poblacion_municipio_sexo_edad_2021.csv",
                "fuente": "INE API",
                "descripcion": "Cifras de población por municipios",
                "variables": "mun_code;2001;2002;2003;2004;2005;2006;2008;2009;2011;2012;2013;2014;2015;2016;2017;2018;2019"
            },
            {
                "archivo_original": "firms_by_APs2000_t0_full.csv",
                "archivo_espana": "empresas_por_municipio.csv",
                "fuente": "INE API",
                "descripcion": "Empresas por municipio",
                "variables": "AP;num_firms"
            },
            {
                "archivo_original": "idhm_2000_2010.csv",
                "archivo_espana": "indicador_desarrollo_espana.csv",
                "fuente": "DataBank API",
                "descripcion": "Indicadores de desarrollo humano",
                "variables": "year;cod_mun;idhm"
            },
            {
                "archivo_original": "interest_fixed.csv",
                "archivo_espana": "tasas_interes_espana.csv",
                "fuente": "DataBank API",
                "descripcion": "Tipos de interés",
                "variables": "date;interest;mortgage"
            },
            {
                "archivo_original": "marriage_age_men.csv",
                "archivo_espana": "marriage_age_men_espana.csv",
                "fuente": "INE Web",
                "descripcion": "Edad media al matrimonio por sexo",
                "variables": "low;high;percentage"
            },
            {
                "archivo_original": "fertility_AC.csv",
                "archivo_espana": "fertilidad_ccaa_espana.csv",
                "fuente": "INE API",
                "descripcion": "Indicadores de fecundidad por comunidades autónomas",
                "variables": "age;2000;2001;2002;2003;2004;2005;2006;2007;2008;2009;2010;2011;2012;2013;2014;2015;2016;2017;2018;2019;2020;2021;2022;2023;2024;2025;2026;2027;2028;2029;2030"
            },
            {
                "archivo_original": "mortality_men_AC.csv",
                "archivo_espana": "mortalidad_hombres_ccaa_espana.csv",
                "fuente": "INE API",
                "descripcion": "Indicadores de mortalidad masculina por comunidades autónomas",
                "variables": "age;2000;2001;2002;2003;2004;2005;2006;2007;2008;2009;2010;2011;2012;2013;2014;2015;2016;2017;2018;2019;2020;2021;2022;2023;2024;2025;2026;2027;2028;2029;2030"
            }
        ];

        // Obtener la tabla y su cuerpo
        const tableBody = document.getElementById('equivalencias-table-body');
        if (!tableBody) return;

        // Limpiar la tabla
        tableBody.innerHTML = '';

        // Añadir filas a la tabla
        equivalencias.forEach(item => {
            const row = document.createElement('tr');
            
            // Añadir celdas con datos
            row.innerHTML = `
                <td>${item.archivo_original}</td>
                <td>${item.archivo_espana}</td>
                <td>${item.fuente}</td>
                <td>${item.descripcion}</td>
                <td><button class="btn btn-sm btn-outline-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${item.variables}">Ver variables</button></td>
            `;
            
            tableBody.appendChild(row);
        });

        // Reinicializar tooltips
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Cargar datos de equivalencias
    loadEquivalenciasData();

    // Filtro de búsqueda para la tabla de equivalencias
    document.getElementById('search-equivalencias').addEventListener('keyup', function() {
        const searchTerm = this.value.toLowerCase();
        const tableRows = document.querySelectorAll('#equivalencias-table-body tr');
        
        tableRows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });

    // Contador de visitas (simulado)
    let visits = localStorage.getItem('visits') || 0;
    visits = parseInt(visits) + 1;
    localStorage.setItem('visits', visits);
    document.getElementById('visit-counter').textContent = visits;

    // Animación de scroll suave para enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Mostrar/ocultar botón de volver arriba
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            document.getElementById('back-to-top').style.display = 'block';
        } else {
            document.getElementById('back-to-top').style.display = 'none';
        }
    });

    // Funcionalidad del botón volver arriba
    document.getElementById('back-to-top').addEventListener('click', function() {
        window.scrollTo({top: 0, behavior: 'smooth'});
    });

    // Simulación de descarga de archivos
    document.querySelectorAll('.download-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const fileName = this.getAttribute('data-file');
            alert(`Descarga simulada: ${fileName}\nEn un entorno de producción, esto descargaría el archivo real.`);
        });
    });

    // Inicializar gráfico de distribución de fuentes (si existe el elemento)
    const chartElement = document.getElementById('sources-chart');
    if (chartElement) {
        const ctx = chartElement.getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['INE API', 'DataBank API', 'Ministerio de Hacienda', 'INE Web'],
                datasets: [{
                    data: [65, 20, 10, 5],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Distribución de Fuentes de Datos'
                    }
                }
            }
        });
    }
});
