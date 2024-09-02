import React from 'react';

const Header = () => {
  return (
    <header className="header">
      <div className="header-left">
        <button className="back-button">← Назад к порталу</button>
        <h1>Переводчик</h1>
      </div>
      <div className="header-right">
        <div className="user-info">
          <span>Иванов Иван Иванович</span>
          <span>Пользователь</span>
        </div>
        <button className="language-selector">РУС</button>
      </div>
    </header>
  );
};

export default Header;
