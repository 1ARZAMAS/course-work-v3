const tab1Btn = document.getElementById('tab1Btn');
const tab2Btn = document.getElementById('tab2Btn');
const tab1Content = document.getElementById('tab1Content');
const tab2Content = document.getElementById('tab2Content');

tab1Btn.addEventListener('click', () => {
    tab1Content.classList.add('active');
    tab2Content.classList.remove('active');
    tab1Btn.classList.add('active');
    tab2Btn.classList.remove('active');
});

tab2Btn.addEventListener('click', () => {
    tab2Content.classList.add('active');
    tab1Content.classList.remove('active');
    tab2Btn.classList.add('active');
    tab1Btn.classList.remove('active');
});

// Логика перехода к профилю и тестированию
function goToProfile() {
    tab1Btn.click();  // Переключаем на вкладку "Мой профиль"
}

function goToTests() {
    tab2Btn.click();  // Переключаем на вкладку "Тестирование"
}

// Логика получения данных о пользователе с сервера
async function loadUserData() {
    try {
        const response = await fetch('/api/user'); // Замените на ваш реальный API endpoint
        const data = await response.json();

        // Заполняем информацию о пользователе
        document.getElementById('userName').textContent = data.name;
        document.getElementById('userEmail').textContent = data.email;

        // Заполняем список пройденных тестов
        const userTests = document.getElementById('userTests');
        userTests.innerHTML = ''; // Очищаем перед добавлением
        data.tests.forEach(test => {
            const li = document.createElement('li');
            li.textContent = '${test.name} - ${test.status}';
            userTests.appendChild(li);
        });
    } catch (error) {
        console.error('Ошибка при загрузке данных о пользователе:', error);
    }
}

// Загружаем данные при загрузке страницы
loadUserData();