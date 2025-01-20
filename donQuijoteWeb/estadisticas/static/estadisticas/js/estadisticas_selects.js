document.addEventListener('DOMContentLoaded', function() {
    const categoriaSelect = document.getElementById('categoria-select');
    const productoSelects = document.querySelectorAll('[id^="producto-select-"]');
    const envioSelect = document.getElementById('envios');

    const fechaInicio = document.getElementById('fecha_inicio');
    const fechaFin = document.getElementById('fecha_fin');
    const diaSemanaSelect = document.getElementById('dia_semana-select');
    const mediaSemanaSelect = document.getElementById('media_semana');
    const mesSelect = document.getElementById('id_mes');  
    const anoSelect = document.getElementById('id_ano');  

    const formProductos = document.getElementById('form-productos');

    categoriaSelect.addEventListener('change', function() {
        productoSelects.forEach(function(productoSelect) {
            productoSelect.selectedIndex = 0; 
            envioSelect.selectedIndex = 0; 
        });
    });

    productoSelects.forEach(function(productoSelect) {
        productoSelect.addEventListener('change', function() {
            categoriaSelect.selectedIndex = 0;
            envioSelect.selectedIndex = 0; 


            productoSelects.forEach(function(otherSelect) {
                if (otherSelect !== productoSelect) { 
                    otherSelect.selectedIndex = 0;
                }
            });
        });
    });

    envioSelect.addEventListener('change', function() {
        categoriaSelect.selectedIndex = 0;
        productoSelects.forEach(select => select.selectedIndex = 0);
    });



    fechaInicio.addEventListener('change', function() {
        diaSemanaSelect.selectedIndex = 0; 
        mediaSemanaSelect.selectedIndex = 0; 
    });

    fechaFin.addEventListener('change', function() {
        diaSemanaSelect.selectedIndex = 0; 
        mediaSemanaSelect.selectedIndex = 0; 
    });

    diaSemanaSelect.addEventListener('change', function() {
        fechaInicio.value = ''; 
        fechaFin.value = '';    
        mediaSemanaSelect.selectedIndex = 0;
    });

    mediaSemanaSelect.addEventListener('change', function() {
        fechaInicio.value = ''; 
        fechaFin.value = '';    
        diaSemanaSelect.selectedIndex = 0; 
    });

    mesSelect.addEventListener('change', function() {
        fechaInicio.value = ''; 
        fechaFin.value = '';    
        diaSemanaSelect.selectedIndex = 0; 
        mediaSemanaSelect.selectedIndex = 0; 
    });

    anoSelect.addEventListener('change', function() {
        fechaInicio.value = ''; 
        fechaFin.value = '';    
        diaSemanaSelect.selectedIndex = 0; 
        mediaSemanaSelect.selectedIndex = 0;
    });


    formProductos.addEventListener('submit', function(event) {
        const inicio = new Date(fechaInicio.value);
        const fin = new Date(fechaFin.value);

        if ((fechaInicio.value && !fechaFin.value) || (!fechaInicio.value && fechaFin.value)) {
            alert("Debes ingresar ambas fechas (inicio y fin)..."); 
            event.preventDefault(); 
        } else if (fechaInicio.value && fechaFin.value && inicio > fin) {
            alert("La fecha de inicio debe ser anterior a la fecha de fin...");
            event.preventDefault(); 
        }
    });
});