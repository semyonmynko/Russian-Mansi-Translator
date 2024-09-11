let isCapsActive = false;
let isShiftActive = false;
let currentLanguage = 'russian'; // Язык по умолчанию — русский
let focused = null; // Переменная для хранения текущего активного поля ввода
	
async function searchInDictionary(query, language) {
    // const sourceLang = document.getElementById("source_lang").value;
    // const targetLang = document.getElementById("target_lang").value;
    if (currentLanguage === 'russian') {
        sourceLang = 'russian';
        targetLang = 'mansi';
    } else {
        sourceLang = 'mansi';
        targetLang = 'russian';
    }

    // Поиск слова
    const wordResponse = await fetch(`/search/word?query=${query}&language=${language}&limit=9`,{
    method: "GET",
    headers: {
        "Authorization": `Bearer ${apiToken}`, // Добавляем заголовок Authorization
        "Content-Type": "application/json"
        }
    });

    if (wordResponse.ok) {
        const words = await wordResponse.json();
        console.log("Слова с API:", words);
        displayWords(words, language);
    }

    // Поиск фразы
    const phraseResponse = await fetch(`/search/phrase?query=${query}&language=${language}&limit=5`,{
    method: "GET",
    headers: {
        "Authorization": `Bearer ${apiToken}`, // Добавляем заголовок Authorization
        "Content-Type": "application/json"
        }
    });
    if (phraseResponse.ok) {
        const phrases = await phraseResponse.json();
        console.log("Фразы с API:", phrases);
        displayPhrases(phrases, language);
    }
}

// Функция для отображения найденных слов
function displayWords(words, language) {
    const wordContainer = document.getElementById("wordDictionary");
    wordContainer.innerHTML = "";  // Очищаем контейнер перед добавлением новых слов

    words.forEach(word => {
        const wordElement = document.createElement("li");
        if (language == 'russian'){
            wordElement.innerHTML = `<li><p class="target_example">${word.russian_word}<p class="target_example"> :</li>`; 
            wordElement.innerHTML +=`<li>${word.mansi_word}</li>`
        } else {
            wordElement.innerHTML = `<li><p class="target_example">${word.mansi_word}<p class="target_example"> :</li>`; 
            wordElement.innerHTML +=`<li>${word.russian_word}</li>`
        }
        wordContainer.appendChild(wordElement);
    });
}

// Функция для отображения найденных фраз
function displayPhrases(phrases, language) {
    const phraseContainer = document.getElementById("phraseDictionary");
    phraseContainer.innerHTML = "";  // Очищаем контейнер перед добавлением новых фраз

    phrases.forEach(phrase => {
        const phraseElement = document.createElement("li");
        if (language == 'russian') {
            phraseElement.innerHTML = `<li><p class="target_example">${phrase.russian_phrase}<p class="target_example"> :</li>`; 
            phraseElement.innerHTML +=`<li>${phrase.mansi_phrase}</li>`
        } else {
            phraseElement.innerHTML = `<li><p class="target_example">${phrase.mansi_phrase}<p class="target_example"> :</li>`; 
            phraseElement.innerHTML +=`<li>${phrase.russian_phrase}</li>`
        }
        phraseContainer.appendChild(phraseElement);
    });
}

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
        } else if (char === 'rus' || char === 'man') { 
            handleLanguageSwitch();
        } else {
            addToInput(char); // Добавляем символ в поле ввода
        }
    }
});

function handleLanguageSwitch() {
    if (currentLanguage === 'mansi') {
        currentLanguage = 'russian';
        loadKeyboard('russian');
    } else {
        currentLanguage = 'mansi';
        loadKeyboard('mansi');
    }
}

function addToInput(char) {
    const input = document.getElementById("inputText");

    input.value += char;
}

function handleBackspace() {
    const input = document.getElementById("inputText");
    input.value = input.value.slice(0, -1); // Удаляем последний символ
}

function handleEnter() {
    const inputText = document.getElementById("inputText").value;
    console.log(inputText)
    searchInDictionary(inputText, currentLanguage);
    toggleKeyboard();
}

function startSearch() {
    const inputText = document.getElementById("inputText").value;
    console.log(inputText)
    searchInDictionary(inputText, currentLanguage);
}

function handleTab() {
    const input = document.getElementById("inputText");
    input.value += '\t'; // Добавляем табуляцию
}

function handleSpace() {
    const input = document.getElementById("inputText");
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
