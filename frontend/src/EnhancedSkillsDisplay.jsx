import React from 'react';
import { BarChart3, TrendingUp, Code, Zap, Globe } from 'lucide-react';
import './EnhancedSkillsDisplay.css';

/**
 * EnhancedSkillsDisplay Component
 * Beautiful visualization of skills with progress bars, stats, and categories
 * 
 * Props:
 * - skills: Object with technical, soft, tools, and languages arrays
 *   Example: {
 *     technical: ['Python', 'JavaScript', 'React'],
 *     soft: ['Communication', 'Leadership'],
 *     tools: ['Git', 'Docker'],
 *     languages: ['English', 'Spanish']
 *   }
 */
export function EnhancedSkillsDisplay({ skills }) {
  
  // ==================== SKILL CATEGORIES ====================
  /**
   * Define all skill categories with their properties
   * - key: Unique identifier for the category
   * - label: Display name
   * - icon: Lucide React icon component
   * - color: Primary color (hex)
   * - bgColor: Background color (light)
   * - borderColor: Border color
   * - gradient: CSS gradient for progress bar
   */
  const categories = [
    { 
      key: 'technical', 
      label: 'Technical Skills',
      icon: Code,
      color: '#3b82f6',
      bgColor: '#eff6ff',
      borderColor: '#bfdbfe',
      gradient: 'linear-gradient(135deg, #3b82f6 0%, #1e40af 100%)'
    },
    { 
      key: 'soft', 
      label: 'Soft Skills',
      icon: Zap,
      color: '#f59e0b',
      bgColor: '#fffbeb',
      borderColor: '#fcd34d',
      gradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
    },
    { 
      key: 'tools', 
      label: 'Tools & Platforms',
      icon: BarChart3,
      color: '#10b981',
      bgColor: '#f0fdf4',
      borderColor: '#86efac',
      gradient: 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
    },
    { 
      key: 'languages', 
      label: 'Languages',
      icon: Globe,
      color: '#8b5cf6',
      bgColor: '#faf5ff',
      borderColor: '#ddd6fe',
      gradient: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)'
    }
  ];

  // ==================== HELPER FUNCTIONS ====================

  /**
   * Calculate total number of skills across all categories
   * @returns {number} Total skill count
   */
  const getTotalSkills = () => {
    return categories.reduce((total, cat) => {
      return total + (skills?.[cat.key]?.length || 0);
    }, 0);
  };

  /**
   * Calculate percentage of skills in a specific category
   * @param {number} count - Number of skills in category
   * @returns {number} Percentage (0-100)
   */
  const getSkillsPercentage = (count) => {
    const total = getTotalSkills();
    return total > 0 ? Math.round((count / total) * 100) : 0;
  };

  // Calculate total once
  const total = getTotalSkills();

  // ==================== RENDER ====================

  return (
    <div className="enhanced-skills-display">
      
      {/* ==================== OVERVIEW STATS DASHBOARD ==================== */}
      
      <div className="skills-overview">
        {/* Total Skills Card */}
        <div className="overview-card">
          <div className="overview-icon">
            <TrendingUp size={24} />
          </div>
          <div className="overview-content">
            <h4>Total Skills</h4>
            <p className="big-number">{total}</p>
          </div>
        </div>

        {/* Technical Skills Card */}
        <div className="overview-card">
          <div className="overview-icon">
            <Code size={24} />
          </div>
          <div className="overview-content">
            <h4>Technical Skills</h4>
            <p className="big-number">{skills?.technical?.length || 0}</p>
          </div>
        </div>

        {/* Soft Skills Card */}
        <div className="overview-card">
          <div className="overview-icon">
            <Zap size={24} />
          </div>
          <div className="overview-content">
            <h4>Soft Skills</h4>
            <p className="big-number">{skills?.soft?.length || 0}</p>
          </div>
        </div>
      </div>

      {/* ==================== SKILLS GRID CARDS ==================== */}

      <div className="skills-grid">
        {categories.map(cat => {
          // Get the icon component
          const Icon = cat.icon;
          
          // Get skills for this category (or empty array if none)
          const categorySkills = skills?.[cat.key] || [];
          
          // Calculate percentage for progress bar
          const percentage = getSkillsPercentage(categorySkills.length);

          return (
            <div key={cat.key} className="skills-card">
              
              {/* ========== CARD HEADER ========== */}
              <div className="card-header">
                {/* Icon Wrapper */}
                <div 
                  className="icon-wrapper" 
                  style={{ backgroundColor: cat.bgColor }}
                >
                  <Icon size={24} color={cat.color} />
                </div>
                
                {/* Title and Count */}
                <div className="header-content">
                  <h3>{cat.label}</h3>
                  <p className="skill-count">{categorySkills.length} skills</p>
                </div>
              </div>

              {/* ========== PROGRESS BAR ========== */}
              <div className="progress-wrapper">
                <div className="progress-bar-bg">
                  <div 
                    className="progress-bar-fill" 
                    style={{ 
                      width: `${percentage}%`,
                      background: cat.gradient
                    }}
                  />
                </div>
                <span className="progress-text">{percentage}% of total</span>
              </div>

              {/* ========== SKILLS CONTAINER ========== */}
              <div className="skills-container">
                {categorySkills.length > 0 ? (
                  <>
                    {/* Display first 6 skills as badges */}
                    <div className="skills-tags">
                      {categorySkills.slice(0, 6).map((skill, idx) => (
                        <span 
                          key={idx} 
                          className="skill-badge"
                          style={{ 
                            backgroundColor: cat.bgColor,
                            borderColor: cat.borderColor,
                            color: cat.color
                          }}
                          title={skill}
                        >
                          ✓ {skill}
                        </span>
                      ))}
                    </div>

                    {/* Show "+N more" button if there are additional skills */}
                    {categorySkills.length > 6 && (
                      <div className="more-skills">
                        <span 
                          className="more-badge"
                          style={{ background: cat.gradient }}
                        >
                          +{categorySkills.length - 6} more
                        </span>
                        {/* Dropdown list of remaining skills */}
                        <div className="more-list">
                          {categorySkills.slice(6).map((skill, idx) => (
                            <span 
                              key={idx} 
                              className="more-item" 
                              title={skill}
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </>
                ) : (
                  /* No skills message */
                  <p className="no-skills">No skills in this category</p>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* ==================== COMPLETE SKILLS INVENTORY ==================== */}

      {total > 0 && (
        <div className="all-skills-section">
          <h3>Complete Skills Inventory</h3>
          
          <div className="skills-list">
            {categories.map(cat => {
              // Get skills for this category
              const categorySkills = skills?.[cat.key] || [];
              
              // Only render if there are skills in this category
              return (
                categorySkills.length > 0 && (
                  <div key={cat.key} className="skill-group">
                    {/* Category Title */}
                    <h4 style={{ color: cat.color }}>
                      {cat.label} ({categorySkills.length})
                    </h4>
                    
                    {/* Skills List */}
                    <div className="skill-list-items">
                      {categorySkills.map((skill, idx) => (
                        <span 
                          key={idx} 
                          className="skill-item"
                          title={skill}
                        >
                          {/* Colored dot */}
                          <span 
                            className="skill-dot" 
                            style={{ backgroundColor: cat.color }}
                          ></span>
                          {/* Skill name */}
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}