import React, { useState } from 'react';
import { Edit2, Save, X, Plus } from 'lucide-react';
import './SkillsEditor.css';

export function SkillsEditor({ extractedSkills, onSkillsUpdate, onContinue }) {
  const [isEditing, setIsEditing] = useState(false);
  const [skills, setSkills] = useState(extractedSkills);
  const [newSkill, setNewSkill] = useState('');
  const [category, setCategory] = useState('technical');

  const handleAddSkill = () => {
    if (!newSkill.trim()) return;
    
    setSkills({
      ...skills,
      [category]: [...(skills[category] || []), newSkill]
    });
    setNewSkill('');
  };

  const handleRemoveSkill = (category, index) => {
    setSkills({
      ...skills,
      [category]: skills[category].filter((_, i) => i !== index)
    });
  };

  const handleSave = () => {
    onSkillsUpdate(skills);
    setIsEditing(false);
  };

  const categories = [
    { key: 'technical', label: 'Technical Skills', color: '#dbeafe' },
    { key: 'soft', label: 'Soft Skills', color: '#fecaca' },
    { key: 'tools', label: 'Tools & Platforms', color: '#d1fae5' },
    { key: 'languages', label: 'Languages', color: '#fef3c7' }
  ];

  return (
    <div className="skills-editor-container">
      <div className="editor-header">
        <h2>Verify & Edit Your Skills</h2>
        <p>Review extracted skills and make corrections if needed</p>
      </div>

      <div className="skills-display">
        {categories.map(cat => (
          <div key={cat.key} className="skill-category">
            <h3 className="category-title">{cat.label}</h3>
            <div className="skills-list">
              {skills[cat.key]?.map((skill, idx) => (
                <div key={idx} className="skill-tag" style={{ backgroundColor: cat.color }}>
                  <span>{skill}</span>
                  {isEditing && (
                    <button
                      onClick={() => handleRemoveSkill(cat.key, idx)}
                      className="remove-skill"
                    >
                      ×
                    </button>
                  )}
                </div>
              )) || <p className="no-skills">No skills in this category</p>}
            </div>
          </div>
        ))}
      </div>

      {isEditing && (
        <div className="add-skill-section">
          <h3>Add Missing Skills</h3>
          <div className="add-skill-form">
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="category-select"
            >
              {categories.map(cat => (
                <option key={cat.key} value={cat.key}>{cat.label}</option>
              ))}
            </select>
            <input
              type="text"
              value={newSkill}
              onChange={(e) => setNewSkill(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAddSkill()}
              placeholder="Type a skill and press Enter"
              className="skill-input"
            />
            <button onClick={handleAddSkill} className="add-skill-btn">
              <Plus size={20} />
              Add
            </button>
          </div>
        </div>
      )}

      <div className="editor-actions">
        {!isEditing ? (
          <>
            <button onClick={() => setIsEditing(true)} className="edit-button">
              <Edit2 size={20} />
              Edit Skills
            </button>
            <button onClick={onContinue} className="continue-button">
              Continue
            </button>
          </>
        ) : (
          <>
            <button onClick={handleSave} className="save-button">
              <Save size={20} />
              Save Changes
            </button>
            <button 
              onClick={() => setIsEditing(false)} 
              className="cancel-button"
            >
              <X size={20} />
              Cancel
            </button>
          </>
        )}
      </div>
    </div>
  );
}