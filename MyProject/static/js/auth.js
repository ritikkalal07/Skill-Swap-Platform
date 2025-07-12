document.addEventListener('DOMContentLoaded', () => {
    const passwordToggles = document.querySelectorAll('.password-toggle');

    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const inputId = toggle.dataset.for;
            const passwordInput = document.getElementById(inputId);

            if (passwordInput) {
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    toggle.textContent = '🙈';
                } else {
                    passwordInput.type = 'password';
                    toggle.textContent = '👁️';
                }
            }
        });
    });
});

