document.addEventListener('DOMContentLoaded', function() {
    const categoriaSelect = document.getElementById('categoria-select');
    const productoSelects = document.querySelectorAll('[id^="producto-select-"]');
    const fechaInicio = document.getElementById('fecha_inicio');
    const fechaFin = document.getElementById('fecha_fin');
    const diaSemanaSelect = document.getElementById('dia_semana-select');
    const mediaSemanaSelect = document.getElementById('media_semana');
    const mesSelect = document.getElementById('id_mes');  
    const anoSelect = document.getElementById('id_ano');  
    const formProductos = document.getElementById('form-productos');

    // Desmarcar producto si se selecciona categoría
    categoriaSelect.addEventListener('change', function() {
        productoSelects.forEach(function(productoSelect) {
            productoSelect.selectedIndex = 0; 
        });
    });

    // Desmarcar categoría si se selecciona producto
    productoSelects.forEach(function(productoSelect) {
        productoSelect.addEventListener('change', function() {
            categoriaSelect.selectedIndex = 0; 
        });
    });

    // Desmarcar día de la semana y media semana si se selecciona fecha de inicio o fin
    fechaInicio.addEventListener('change', function() {
        diaSemanaSelect.selectedIndex = 0; 
        mediaSemanaSelect.selectedIndex = 0; 
    });

    fechaFin.addEventListener('change', function() {
        diaSemanaSelect.selectedIndex = 0; 
        mediaSemanaSelect.selectedIndex = 0; 
    });

    // Desmarcar fechas si se selecciona un día de la semana o media semana
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

    // Desmarcar fecha de inicio, fecha de fin, día de la semana y media semana cuando se seleccione mes o año
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