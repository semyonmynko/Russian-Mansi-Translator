let isCapsActive = false;
let isShiftActive = false;
let currentLanguage = 'russian'; // Язык по умолчанию — русский

// Функция для загрузки клавиатуры в зависимости от состояния Caps Lock и Shift
function loadKeyboard() {
    const inputText = document.getElementById("source_lang").textContent
    const filePrefix = inputText === 'РУССКИЙ' ? 'russian' : 'mansi';
    let fileName;

    if (isShiftActive) {
        fileName = `/keyboard/${filePrefix}-shift`;
    } else if (isCapsActive) {
        fileName = `/keyboard/${filePrefix}-upper`;
    } else {
        fileName = `/keyboard/${filePrefix}-lower`;
    }

    loadKeyboardFromFile(fileName);
}

// AJAX-запрос для загрузки клавиатуры из файла
function loadKeyboardFromFile(file) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', file, true);
    //xhr.setRequestHeader('Authorization', `Bearer ${apiToken}`);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById('keyboardSection').innerHTML = xhr.responseText;
        }
    };
    xhr.send();
}

// Функция для определения языка на основе содержимого inputText
function switchLanguage() {
    const inputText = document.getElementById("inputText").value;
    currentLanguage = /[а-яА-ЯёЁ]/.test(inputText) ? 'russian' : 'mansi';
}

// Показ/скрытие клавиатуры и определение языка
function toggleKeyboard() {
    const keyboardSection = document.getElementById("keyboardSection");

    if (!keyboardSection.classList.contains("visible")) {
        // Определить язык перед отображением клавиатуры
        switchLanguage();

        // Загружаем клавиатуру при открытии
        loadKeyboard();
        keyboardSection.classList.add("visible");
    } else {
        keyboardSection.classList.remove("visible");
    }
}

document.addEventListener('click', function(event) {
    if (event.target.classList.contains('keyboard_button')) {
        event.preventDefault();

        // Получаем текст кнопки
        const char = event.target.textContent.trim();

        // Проверяем, является ли это специальной клавишей
        if (char === '←') {
            handleBackspace();
        } else if (char === '↲') {
            handleEnter();
        } else if (char === '⇑') {
            toggleShift();
        } else if (char === '⇆') {
            handleTab();
        } else if (char === 'Caps' || char === '⟰') { // Обрабатываем как Caps Lock
            toggleCapsLock();
        } else if (char === 'РУССКИЙ' || char === 'МАНСИЙСКИЙ') { 
            handleSpace();
        } else if (char === 'rus' || char === 'man') { 
            
        } else {
            addToInput(char); // Добавляем символ в поле ввода
        }
    }
});

function addToInput(char) {
    const input = document.getElementById("inputText");

    input.value += char;
}

// Переключение Caps Lock
function toggleCapsLock() {
    isCapsActive = !isCapsActive;
    loadKeyboard();
}

// Переключение Shift
function toggleShift() {
    isShiftActive = !isShiftActive;
    loadKeyboard();
}

function handleBackspace() {
    const input = document.getElementById("inputText");
    input.value = input.value.slice(0, -1); // Удаляем последний символ
}

function handleEnter() {
    translateText()
}

function handleTab() {
    const input = document.getElementById("inputText");
    input.value += '\t'; // Добавляем символ табуляции
}

function handleSpace() {
    const input = document.getElementById("inputText");
    input.value += ' '; // Добавляем пробел
}

// Добавляем обработчик клика для иконки клавиатуры
document.getElementById('keyboardIcon').addEventListener('click', (event) => {
    event.preventDefault(); // Предотвращаем переход по ссылке
    toggleKeyboard(); // Показываем клавиатуру и определяем язык
});

// Обработка клика на клавиатуру
document.getElementById('keyboardSection').addEventListener('click', (event) => {
    event.stopPropagation(); // Остановка всплытия события
});