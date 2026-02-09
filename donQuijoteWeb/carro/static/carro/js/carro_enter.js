document.getElementById('form-datos').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        e.stopPropagation();
        this.submit();
    }
});
