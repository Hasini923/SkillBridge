import React from 'react';
import './Logo.css';

export function Logo({ size = 'medium', showText = true, className = '' }) {
  const sizes = {
    small: { container: 80, cap: 40, book: 30, text: 18 },
    medium: { container: 120, cap: 60, book: 45, text: 24 },
    large: { container: 180, cap: 90, book: 68, text: 36 },
    xlarge: { container: 240, cap: 120, book: 90, text: 48 }
  };

  const s = sizes[size];

  return (
    <div className={`skillbridge-logo ${className}`} style={{ width: s.container }}>
      {/* Logo Icon */}
      <div className="logo-icon" style={{ height: s.container * 0.8 }}>
        {/* Open Book */}
        <svg 
          viewBox="0 0 200 150" 
          style={{ width: '100%', height: '100%' }}
          className="book-svg"
        >
          {/* Book base */}
          <path 
            d="M 40 80 Q 100 100 160 80 L 160 120 Q 100 140 40 120 Z" 
            fill="#60a5fa"
            className="book-pages"
          />
          {/* Book left page */}
          <path 
            d="M 40 80 Q 100 100 100 100 L 100 140 Q 100 140 40 120 Z" 
            fill="#93c5fd"
            className="book-left"
          />
          {/* Book right page */}
          <path 
            d="M 100 100 Q 160 80 160 80 L 160 120 Q 100 140 100 140 Z" 
            fill="#bfdbfe"
            className="book-right"
          />
          
          {/* Graduation Cap */}
          <g className="cap-group">
            {/* Cap base */}
            <polygon 
              points="100,40 60,60 100,70 140,60" 
              fill="#1e3a8a"
              className="cap-base"
            />
            {/* Cap top */}
            <ellipse 
              cx="100" 
              cy="60" 
              rx="40" 
              ry="8" 
              fill="#1e40af"
              className="cap-top"
            />
            {/* Tassel */}
            <g className="tassel">
              <line 
                x1="100" 
                y1="40" 
                x2="120" 
                y2="30" 
                stroke="#1e3a8a" 
                strokeWidth="2"
              />
              <circle 
                cx="120" 
                cy="30" 
                r="3" 
                fill="#1e3a8a"
              />
            </g>
          </g>
        </svg>
      </div>

      {/* Logo Text */}
      {showText && (
        <div className="logo-text" style={{ fontSize: s.text }}>
          <span className="logo-skill">SKILL</span>
          <span className="logo-bridge">BRIDGE</span>
        </div>
      )}
    </div>
  );
}

export default Logo;