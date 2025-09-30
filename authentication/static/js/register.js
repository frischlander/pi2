const usernameField = document.querySelector('#usernameField');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const passwordField = document.querySelector('#passwordField');
const submitBtn = document.querySelector('.submit-btn');
const form = document.querySelector('form');

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
    const successOutput = document.querySelector('.usernameSuccessOutput');

    usernameField.classList.remove('is-invalid');
    feedbackArea.style.display = 'none';    
    successOutput.style.display = 'none';

    if (usernameVal.length > 0) {
        fetch('/authentication/validate-username', {
            body: JSON.stringify({username: usernameVal}), 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(res => res.json())
        .then(data => {
            console.log('data', data);
            if (data.username_error) {
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display = 'block';
                feedbackArea.innerHTML = '<p>Username não autorizado ou não encontrado no sistema.</p>';
                submitBtn.disabled = true;
            } else if (data.username_success) {
                successOutput.style.display = 'block';
                successOutput.innerHTML = '<p>Username autorizado encontrado!</p>';
                submitBtn.disabled = false;
            }
        });
    }
});

form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const formData = new FormData(form);
    
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect_url;
        } else {
            const feedbackArea = document.querySelector('.invalid_feedback');
            feedbackArea.style.display = 'block';
            feedbackArea.innerHTML = `<p>${data.error}</p>`;
        }
    });
});

