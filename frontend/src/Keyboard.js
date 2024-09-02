import React from 'react';
import './Keyboard.css';

const Keyboard = ({ language, onKeyPress, onClose }) => {
  const layouts = {
    ru: [
      ['ё', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
      ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ'],
      ['ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э'],
      ['я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', '.', '⇧'],
      [' ']
    ],
    en: [
      ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
      ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'],
      ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'"],
      ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '⇧'],
      [' ']
    ],
  };

  return (
    <div className="keyboard-container">
      <div className="keyboard">
        {layouts[language].map((row, rowIndex) => (
          <div key={rowIndex} className="keyboard-row">
            {row.map((key) => (
              <button
                key={key}
                className="keyboard-key"
                onClick={() => onKeyPress(key)}
              >
                {key}
              </button>
            ))}
          </div>
        ))}
        <button className="keyboard-close" onClick={onClose}>Закрыть</button>
      </div>
    </div>
  );
};

export default Keyboard;