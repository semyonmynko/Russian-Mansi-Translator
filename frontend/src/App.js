import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Keyboard from 'react-simple-keyboard';
import 'react-simple-keyboard/build/css/index.css';

function App() {
  const [sourceLanguage, setSourceLanguage] = useState('ru');
  const [targetLanguage, setTargetLanguage] = useState('en');
  const [sourceText, setSourceText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [loading, setLoading] = useState(false);
  const [showKeyboard, setShowKeyboard] = useState(false);
  const [showCopyMessage, setShowCopyMessage] = useState(false);

  const handleTranslate = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/translate', {
        text: sourceText,
        source_lang: sourceLanguage,
        target_lang: targetLanguage,
      });
      setTranslatedText(response.data.translated_text);
    } catch (error) {
      console.error('Error during translation:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (button) => {
    if (button === "{bksp}") {
      setSourceText(sourceText.slice(0, -1));
    } else if (button === "{space}") {
      setSourceText(sourceText + " ");
    } else if (button === "{enter}") {
      setSourceText(sourceText + "\n");
    } else {
      setSourceText(sourceText + button);
    }
  };

  const swapLanguages = () => {
    // Меняем местами языки
    setSourceLanguage(prev => prev === 'ru' ? 'en' : 'ru');
    setTargetLanguage(prev => prev === 'ru' ? 'en' : 'ru');

    // Меняем местами тексты
    setSourceText(translatedText);
    setTranslatedText(sourceText);
  };

  // Используем useEffect, чтобы автоматически инициировать перевод после смены языков
  useEffect(() => {
    if (sourceText) {
      handleTranslate(sourceText, sourceLanguage, targetLanguage);
    }
  }, [sourceLanguage, targetLanguage]);

  const handleCopyText = () => {
    navigator.clipboard.writeText(translatedText).then(() => {
      setShowCopyMessage(true);
      setTimeout(() => setShowCopyMessage(false), 2000);
    });
  };

  const handleSpeakText = () => {
    const utterance = new SpeechSynthesisUtterance(translatedText);
    utterance.lang = targetLanguage === 'ru' ? 'ru-RU' : 'en-US';
    window.speechSynthesis.speak(utterance);
  };

  const layouts = {
    ru: {
      default: [
        "ё 1 2 3 4 5 6 7 8 9 0 - = {bksp}",
        "й ц у к е н г ш щ з х ъ \\",
        "ф ы в а п р о л д ж э {enter}",
        "{shift} я ч с м и т ь б ю . {shift}",
        "{space}"
      ]
    },
    en: {
      default: [
        "` 1 2 3 4 5 6 7 8 9 0 - = {bksp}",
        "q w e r t y u i o p [ ] \\",
        "a s d f g h j k l ; ' {enter}",
        "{shift} z x c v b n m , . / {shift}",
        "{space}"
      ]
    }
  };

  return (
    <div className="translator-container">
      <header className="header">
        <h1 className="title">Переводчик</h1>
        <div className="lang-selector">
          {/* Кнопки выбора языка, которые не меняют своего положения */}
          <button className="lang-button">
            {sourceLanguage === 'ru' ? 'РУССКИЙ' : 'АНГЛИЙСКИЙ'}
          </button>
          {/* Кнопка смены языка, которая всегда остается на месте */}
          <button className="swap-button" onClick={swapLanguages}>↔</button>
          <button className="lang-button">
            {targetLanguage === 'ru' ? 'РУССКИЙ' : 'АНГЛИЙСКИЙ'}
          </button>
        </div>
      </header>

      <div className="text-area-container">
        <div className="input-container">
          <textarea
            className="source-textarea"
            value={sourceText}
            onChange={(e) => setSourceText(e.target.value)}
            placeholder="Введите текст для перевода..."
          />
          <span className="char-count">{sourceText.length} / 5000</span>
          <div className="action-buttons">
            <button className="translate-button" onClick={handleTranslate} disabled={loading}>
              {loading ? 'Перевод...' : 'Перевести'}
            </button>
            <button className="show-keyboard-button" onClick={() => setShowKeyboard(!showKeyboard)}>
              🧑‍💻
            </button>
          </div>
        </div>

        <div className="output-container">
          <textarea
            className="translated-textarea"
            value={translatedText}
            readOnly
            placeholder="Здесь появится перевод..."
          />
          <div className="output-buttons">
            <button className="output-button" onClick={handleCopyText}>📋 Копировать</button>
            <button className="output-button" onClick={handleSpeakText}>🔊 Озвучить</button>
          </div>
          {showCopyMessage && (
            <div className="copy-message">
              Текст скопирован в буфер обмена
            </div>
          )}
        </div>
      </div>

      {showKeyboard && (
        <div className="keyboard-container">
          <Keyboard
            layout={layouts[sourceLanguage]}
            layoutName="default"
            onKeyPress={handleKeyPress}
            theme="hg-theme-default hg-layout-default"
            display={{
              "{bksp}": "⌫",
              "{enter}": "⏎",
              "{shift}": "⇧",
              "{space}": " ",
            }}
          />
        </div>
      )}
    </div>
  );
}

export default App;
