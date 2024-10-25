function copiarAlPortapapeles(button) {
    var categoriaContainer = button.closest('.card');

    var titulo = categoriaContainer.querySelector('.categoria-titulo').innerText;

    var informacionContainer = categoriaContainer.querySelector('.categoria-info');

    var informacion = informacionContainer.innerText;

    var textoACopiar = titulo + "\n" + informacion;

    var lineas = textoACopiar.split('\n');
    var textoFiltrado = lineas.filter(function(linea) {
        return linea.trim() !== '';
    }).join('\n');

    var tempInput = document.createElement('textarea');
    tempInput.value = textoFiltrado;
    document.body.appendChild(tempInput);

    tempInput.select();
    tempInput.setSelectionRange(0, 99999); 

    document.execCommand('copy');

    document.body.removeChild(tempInput);

    alert('Información copiada al portapapeles');
}
