    const urlPedidoNuevo = "{% url 'pedido:pedido_nuevo' %}";
    let ultimoPedido = parseInt(localStorage.getItem("ultimoPedido")) || 0;

    setInterval(() => {
        fetch(`${urlPedidoNuevo}?ultimo_id=${ultimoPedido}`)
            .then(r => r.json())
            .then(data => {
                if (data.nuevo && data.ultimo_id > ultimoPedido) {
                    document.getElementById("plin").play();
                    ultimoPedido = data.ultimo_id;
                    localStorage.setItem("ultimoPedido", ultimoPedido);
                }
            });
    }, 5000);