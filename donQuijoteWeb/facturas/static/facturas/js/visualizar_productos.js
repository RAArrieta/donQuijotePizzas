function toggleProductos(facturaId) {
    var productosDiv = document.getElementById('productos-' + facturaId);
    if (productosDiv.style.display === 'none') {
        productosDiv.style.display = 'block';
    } else {
        productosDiv.style.display = 'none';
    }
}