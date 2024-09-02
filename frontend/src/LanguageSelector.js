import React from 'react';

const LanguageSelector = ({ selectedLanguage, onChange }) => {
  return (
    <div className="language-selector">
      <select value={selectedLanguage} onChange={onChange}>
        <option value="RUS">РУС</option>
        <option value="MANS">МАНС</option>
      </select>
    </div>
  );
};

export default LanguageSelector;