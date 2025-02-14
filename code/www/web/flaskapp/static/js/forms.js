window.Telegram.WebApp.ready();  // Сообщаем Telegram, что приложение готово к работе

// Получаем данные пользователя
const userInfo = Telegram.WebApp.initDataUnsafe.user;
const userElement = document.getElementById('user-info');
userElement.innerHTML = `Hello, ${userInfo.first_name} ${userInfo.last_name}`;

// Отправка данных в бот
document.getElementById('send-data-btn').addEventListener('click', () => {
    const data = { message: "User clicked the button!" };
    Telegram.WebApp.sendData(JSON.stringify(data));  // Отправляем данные боту
});

document.addEventListener('DOMContentLoaded', function() {
    // Функции для отображения загрузки и ошибок
    function displayError(errorMessage, elementId) {
        document.getElementById(elementId).innerHTML = `<div class="error">${errorMessage}</div>`;
    }

    function displayLoader(elementId) {
        document.getElementById(elementId).innerHTML = `<div class="loading">Загрузка...</div>`;
    }

    // Функция для обработки форм
    function handleFormSubmit(formId, endpoint, resultId, renderFunction) {
        document.getElementById(formId).addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(document.getElementById(formId));
            const data = Object.fromEntries(formData.entries());

            displayLoader(resultId);

            fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    displayError(`Ошибка: ${data.error}`, resultId);
                } else {
                    renderFunction(data, resultId);
                }
            })
            .catch(error => {
                displayError(`Ошибка: ${error.message}`, resultId);
            });
        });
    }

    // Обработка форм
    handleFormSubmit('portScannerForm', '/api/scan', 'scanResult', function(data, resultId) {
        document.getElementById(resultId).innerHTML = `<div class="result">${data.result}</div>`;
    });

    handleFormSubmit('ipLookupForm', '/api/ip_lookup', 'ipInfo', function(data, resultId) {
        document.getElementById(resultId).innerHTML = `<div class="result">${data.info}</div>`;
    });
}
