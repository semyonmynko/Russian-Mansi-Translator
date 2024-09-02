import React from 'react';

const ActionButtons = ({ onSwapLanguages, onCopy }) => {
  return (
    <div className="action-buttons">
      <button onClick={onSwapLanguages}>↔</button>
      <button onClick={onCopy}>📋</button>
      <button>🔊</button>
    </div>
  );
};

export default ActionButtons;
