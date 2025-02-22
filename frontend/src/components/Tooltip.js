import React from 'react';

const Tooltip = ({ children, text, position = 'top' }) => {
  return (
    <div className="relative group">
      {children}
      <span className={`absolute hidden group-hover:block bg-gray-800 text-white text-xs p-2 rounded shadow-lg ${position === 'top' ? '-top-8 left-1/2 -translate-x-1/2' : 'bottom-full left-1/2 -translate-x-1/2'}`}>
        {text}
        <div className="absolute w-2 h-2 bg-gray-800 rotate-45 -bottom-1 left-1/2 -translate-x-1/2"></div>
      </span>
    </div>
  );
};

export default Tooltip;