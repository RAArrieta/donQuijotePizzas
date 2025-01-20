const selects = document.querySelectorAll('.selects');

function deseleccionarOtrosYEnviar(event) {
    const selectActual = event.target;
    
    selects.forEach(select => {
        if (select !== selectActual) {
            select.selectedIndex = 0;
        }
    });

    document.getElementById('form-productos').submit();
}