import React, { useState } from 'react';
import { Search, Loader } from 'lucide-react';
import './TargetRoleSelector.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

/**
 * Target Role Selector Component with Autocomplete
 * Shows dropdown suggestions as user types
 * Supports 50+ different roles
 */
function TargetRoleSelector({ onAnalyze, loading, error }) {
  const [role, setRole] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [loadingSuggestions, setLoadingSuggestions] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);

  // Fetch role suggestions as user types
  const fetchSuggestions = async (searchQuery) => {
    if (!searchQuery || searchQuery.trim().length < 1) {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    try {
      setLoadingSuggestions(true);
      const response = await fetch(
        `${API_URL}/search-roles?q=${encodeURIComponent(searchQuery)}`
      );
      const data = await response.json();
      setSuggestions(data.roles || []);
      setShowSuggestions(true);
      setSelectedIndex(-1);
    } catch (err) {
      console.error('Error fetching suggestions:', err);
      setSuggestions([]);
    } finally {
      setLoadingSuggestions(false);
    }
  };

  // Handle input change
  const handleInputChange = (e) => {
    const value = e.target.value;
    setRole(value);
    fetchSuggestions(value);
  };

  // Handle suggestion click
  const handleSuggestionClick = (suggestion) => {
    setRole(suggestion);
    setShowSuggestions(false);
    setSuggestions([]);
  };

  // Handle keyboard navigation
  const handleKeyDown = (e) => {
    if (!showSuggestions || suggestions.length === 0) {
      if (e.key === 'Enter' && role.trim()) {
        handleSubmit(e);
      }
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev =>
          prev < suggestions.length - 1 ? prev + 1 : prev
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => (prev > 0 ? prev - 1 : -1));
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0) {
          handleSuggestionClick(suggestions[selectedIndex]);
        } else if (role.trim()) {
          handleSubmit(e);
        }
        break;
      case 'Escape':
        setShowSuggestions(false);
        break;
      default:
        break;
    }
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!role.trim()) {
      alert('Please enter or select a target role');
      return;
    }
    setShowSuggestions(false);
    onAnalyze(role);
  };

  return (
    <div className="target-role-container">
      <h2>What's Your Target Role?</h2>
      <p>Enter the job position you're aiming for</p>

      <form onSubmit={handleSubmit}>
        {/* Search Input with Autocomplete */}
        <div className="search-wrapper">
          <div className="search-input-group">
            <Search size={20} className="search-icon" />
            <input
              type="text"
              value={role}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              onFocus={() => role && setShowSuggestions(true)}
              placeholder="e.g., Frontend Engineer, Data Scientist, DevOps..."
              className="role-input"
              autoComplete="off"
            />
            {loadingSuggestions && (
              <Loader size={20} className="loading-spinner" />
            )}
          </div>

          {/* Autocomplete Dropdown */}
          {showSuggestions && suggestions.length > 0 && (
            <div className="suggestions-dropdown">
              <div className="suggestions-header">
                <p className="suggestions-count">
                  {suggestions.length} matching role{suggestions.length !== 1 ? 's' : ''}
                </p>
              </div>
              <div className="suggestions-list">
                {suggestions.map((suggestion, index) => (
                  <div
                    key={index}
                    className={`suggestion-item ${
                      index === selectedIndex ? 'selected' : ''
                    }`}
                    onClick={() => handleSuggestionClick(suggestion)}
                    onMouseEnter={() => setSelectedIndex(index)}
                  >
                    <span className="suggestion-icon">💼</span>
                    <span className="suggestion-text">{suggestion}</span>
                  </div>
                ))}
              </div>
              <div className="suggestions-footer">
                <small>Use arrow keys to navigate, Enter to select</small>
              </div>
            </div>
          )}

          {/* No suggestions message */}
          {showSuggestions && role && suggestions.length === 0 && !loadingSuggestions && (
            <div className="suggestions-dropdown">
              <div className="no-suggestions">
                <p>No roles found matching "{role}"</p>
                <small>Try typing a different role name</small>
              </div>
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && <div className="error-message">⚠️ {error}</div>}

        {/* Submit Button */}
        <button type="submit" disabled={loading} className="analyze-button">
          {loading ? (
            <>
              <Loader size={18} className="button-spinner" />
              Analyzing...
            </>
          ) : (
            'Analyze Resume'
          )}
        </button>
      </form>

      {/* Available Roles Hint */}
      <div className="roles-hint">
        <p>
          <strong>Popular roles:</strong> Frontend Engineer, Backend Engineer,
          Full Stack Developer, Data Scientist, DevOps Engineer, Machine Learning
          Engineer, Cybersecurity Analyst, Cloud Architect, Mobile App Developer,
          QA Engineer, Prompt Engineer, Solutions Architect, Product Manager, IoT
          Engineer, and 30+ more roles available!
        </p>
      </div>
    </div>
  );
}

export default TargetRoleSelector;