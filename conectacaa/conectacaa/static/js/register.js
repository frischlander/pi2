const usernameField = document.querySelector('#usernameField');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const passwordField = document.querySelector('#passwordField');

const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "MOSTRAR") {
        showPasswordToggle.textContent = "ESCONDER";
        passwordField.setAttribute("type", "text");
    } else {
        showPasswordToggle.textContent = "MOSTRAR";
        passwordField.setAttribute("type", "password");
    }
};

showPasswordToggle.addEventListener('click', handleToggleInput);

usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    const feedbackArea = document.querySelector('.invalid_feedback');

    usernameField.classList.remove('is-invalid');
    feedbackArea.style.display = 'none';    

    if (usernameVal.length > 0) {
        fetch('/authentication/validate-username', {
            body: JSON.stringify({username: usernameVal}), 
            method: 'POST',
        })
        .then(res => res.json())
        .then(data => {
            console.log('data', data);
            if (data.username_error) {
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display = 'block';
                feedbackArea.innerHTML = '<p>Não são permitidos caracteres especiais. Tente novamente.</p>'
            }
        });
    }
});

