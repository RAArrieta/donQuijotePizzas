document.getElementById('form-datos').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        this.submit();
    }
});