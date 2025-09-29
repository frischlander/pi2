document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.getElementById('passwordField');
    const showPasswordToggle = document.querySelector('.showPasswordToggle');

    showPasswordToggle.addEventListener('click', function() {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        this.textContent = type === 'password' ? 'MOSTRAR' : 'OCULTAR';
    });
}); 