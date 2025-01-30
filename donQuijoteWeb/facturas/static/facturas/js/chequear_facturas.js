document.addEventListener("DOMContentLoaded", function () {
    const noCheckSrc = "/static/facturas/img/no_check.png";
    const checkSrc = "/static/facturas/img/check.png";

    document.querySelectorAll(".icono-opc").forEach(img => {
        img.addEventListener("click", function () {
            img.src = img.src.includes("no_check.png") ? checkSrc : noCheckSrc;
        });
    });
});
