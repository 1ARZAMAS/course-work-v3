document.getElementById('login.html').addEventListener('submit', async function (event) {
    event.preventDefault(); // Остановить стандартное поведение формы

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/api/users/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
        alert('Login successful!');
        window.location.href = '/'; // Перенаправление после успешного входа
    } else {
        alert('Invalid username or password');
    }
});