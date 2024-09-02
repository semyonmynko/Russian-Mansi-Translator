import React from 'react';

const TextArea = ({ value, onChange, placeholder }) => {
  return (
    <textarea
      className="text-area"
      value={value}
      onChange={onChange}
      placeholder={placeholder}
    />
  );
};

export default TextArea;
