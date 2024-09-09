let isCapsActive = false;
let isShiftActive = false;
let currentLanguage = 'russian'; // Язык по умолчанию — русский
let focused = null; // Переменная для хранения текущего активного поля ввода
	
async function addWord() {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const mansiWord = document.getElementById("mansi_word").value;
    const russianWord = document.getElementById("russian_word").value;
    const partOfSpeech = document.getElementById("part_of_speech").value;
    const comment = document.getElementById("comment").value;

    let valid = true;

    const data = {
        mansi_word: mansiWord,
        russian_word: russianWord,
        part_of_speech: partOfSpeech,
        comment: comment,
    };

    console.log(data)

    if (mansiWord == '') {
        alert('Пожалуйста, введите перевод на мансийском языке');
        return
    }
    if (russianWord == '') {
        alert('Пожалуйста, введите перевод на русском языке');
        return
    }
    if (partOfSpeech == '') {
        alert('Пожалуйста, выберите часть речи');
        return
    }

    console.log(valid)

    if (valid) {
        try {
            const response = await fetch('/add/word', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiToken}` // если требуется токен
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const keyboardSection = document.getElementById("keyboardSection");
                keyboardSection.classList.remove("visible");
                clearText();
                alert('Перевод успешно добавлен!');
            } else {
                alert('Ошибка при добавлении перевода!');
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при отправке запроса');
        }
    }
};

// Функция для загрузки клавиатуры в зависимости от активного поля и состояния Caps Lock и Shift
function loadKeyboard(language = currentLanguage) { // Используем текущий язык по умолчанию
    const filePrefix = language === 'russian' ? 'russian' : 'mansi';
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

// Добавляем обработчики клика на поля ввода
document.getElementById('mansi_word').addEventListener('focus', function () {
    currentLanguage = 'mansi';  // Устанавливаем текущий язык
    loadKeyboard('mansi');  // Включаем мансийскую клавиатуру при фокусе на этом поле
    focused = 'mansi_word'
    console.log('mansi_word focused');
});

document.getElementById('russian_word').addEventListener('focus', function () {
    currentLanguage = 'russian';  // Устанавливаем текущий язык
    loadKeyboard('russian');  // Включаем русскую клавиатуру при фокусе на этом поле
    focused = 'russian_word'
    console.log('russian_word focused');
});

document.getElementById('comment').addEventListener('focus', function () {
    currentLanguage = 'russian';  // Устанавливаем текущий язык
    loadKeyboard('russian');  // Включаем русскую клавиатуру при фокусе на этом поле
    focused = 'comment'
    console.log('comment focused');
});

function clearText() {
    document.getElementById("mansi_word").value = "";
    document.getElementById("russian_word").value = "";
    document.getElementById("comment").value = "";
}

// AJAX-запрос для загрузки клавиатуры из файла
function loadKeyboardFromFile(file) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', file, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById('keyboardSection').innerHTML = xhr.responseText;
        }
    };
    xhr.send();
}

// Показ/скрытие клавиатуры и обновление раскладки
function toggleKeyboard() {
    const keyboardSection = document.getElementById("keyboardSection");

    if (!keyboardSection.classList.contains("visible")) {
        loadKeyboard(); // Загружаем клавиатуру при открытии с текущим языком
        keyboardSection.classList.add("visible");
    } else {
        keyboardSection.classList.remove("visible");
    }
}

// Обработчики для специальных клавиш
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('keyboard_button')) {
        event.preventDefault();

        // Получаем текст кнопки
        const char = event.target.textContent.trim();

        // Проверяем, является ли это специальной клавишей
        if (char === '←') {
            handleBackspace();
        } else if (char === '↲') {
            console.log('Enter pressed');
            handleEnter();
        } else if (char === '⇑') {
            toggleShift();
        } else if (char === '⇆') {
            handleTab();
        } else if (char === 'Caps' || char === '⟰') { // Обрабатываем как Caps Lock
            toggleCapsLock();
        } else if (char === 'РУССКИЙ' || char === 'МАНСИЙСКИЙ') { 
            handleSpace();
        } else if (char === 'rus' || char === 'mansi') { 
            
        } else {
            addToInput(char); // Добавляем символ в поле ввода
        }
    }
});

// Функции для добавления символов и обработки специальных клавиш
function addToInput(char) {
    const input = document.getElementById(focused); // Вводим символ в активное поле
    console.log(focused)
    input.value += char;
}

function handleBackspace() {
    const input = document.getElementById(focused); // Вводим символ в активное поле
    input.value = input.value.slice(0, -1); // Удаляем последний символ
}

function handleEnter() {
    addWord();
}

function handleTab() {
    const input = document.getElementById(focused); // Вводим символ в активное поле
    input.value += '\t'; // Добавляем табуляцию
}

function handleSpace() {
    const input = document.getElementById(focused); // Вводим символ в активное поле
    input.value += ' '; // Добавляем пробел
}

// Переключение Caps Lock
function toggleCapsLock() {
    isCapsActive = !isCapsActive;
    loadKeyboard(currentLanguage); // Перезагружаем клавиатуру после изменения Caps Lock
}

// Переключение Shift
function toggleShift() {
    isShiftActive = !isShiftActive;
    loadKeyboard(currentLanguage); // Перезагружаем клавиатуру после изменения Shift
}
