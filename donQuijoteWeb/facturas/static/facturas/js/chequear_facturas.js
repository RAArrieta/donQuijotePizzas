document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.toggle-class').forEach(div => {
        div.addEventListener('click', () => {
            if (div.classList.contains('no-check')) {
                div.classList.remove('no-check');
                div.classList.add('check');
            } else {
                div.classList.remove('check');
                div.classList.add('no-check');
            }
        });
    });
});