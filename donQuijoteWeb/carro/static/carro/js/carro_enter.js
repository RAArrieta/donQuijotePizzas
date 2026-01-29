// document.getElementById('form-datos').addEventListener('keypress', function (e) {
//     if (e.key === 'Enter') {
//         e.preventDefault();
//         this.submit();
//     }
// });

document.getElementById('form-datos').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        e.stopPropagation();
        this.submit();
    }
});
