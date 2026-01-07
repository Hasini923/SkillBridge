import React, { useState } from 'react';
import { Plus, Trash2, User, Briefcase, GraduationCap, Code, Award, FileText } from 'lucide-react';
import './ResumeForm.css';

export function ResumeForm({ onSubmit, onCancel }) {
  // Personal Information
  const [personalInfo, setPersonalInfo] = useState({
    fullName: '',
    email: '',
    phone: '',
    location: '',
    linkedin: '',
    portfolio: '',
    github: ''
  });

  // Professional Summary
  const [summary, setSummary] = useState('');

  // Education (array of entries)
  const [education, setEducation] = useState([
    { degree: '', institution: '', location: '', year: '', gpa: '', description: '' }
  ]);

  // Work Experience (array of entries)
  const [experience, setExperience] = useState([
    { company: '', position: '', location: '', duration: '', responsibilities: [''] }
  ]);

  // Projects (array of entries)
  const [projects, setProjects] = useState([
    { name: '', description: '', technologies: '', link: '' }
  ]);

  // Skills
  const [skills, setSkills] = useState({
    technical: '',
    tools: '',
    soft: '',
    languages: ''
  });

  // Certifications
  const [certifications, setCertifications] = useState(['']);

  // Achievements
  const [achievements, setAchievements] = useState(['']);

  // ==================== HANDLERS ====================

  const handlePersonalInfoChange = (field, value) => {
    setPersonalInfo({ ...personalInfo, [field]: value });
  };

  const addEducation = () => {
    setEducation([...education, { degree: '', institution: '', location: '', year: '', gpa: '', description: '' }]);
  };

  const removeEducation = (index) => {
    setEducation(education.filter((_, i) => i !== index));
  };

  const updateEducation = (index, field, value) => {
    const updated = [...education];
    updated[index][field] = value;
    setEducation(updated);
  };

  const addExperience = () => {
    setExperience([...experience, { company: '', position: '', location: '', duration: '', responsibilities: [''] }]);
  };

  const removeExperience = (index) => {
    setExperience(experience.filter((_, i) => i !== index));
  };

  const updateExperience = (index, field, value) => {
    const updated = [...experience];
    updated[index][field] = value;
    setExperience(updated);
  };

  const addResponsibility = (expIndex) => {
    const updated = [...experience];
    updated[expIndex].responsibilities.push('');
    setExperience(updated);
  };

  const removeResponsibility = (expIndex, respIndex) => {
    const updated = [...experience];
    updated[expIndex].responsibilities = updated[expIndex].responsibilities.filter((_, i) => i !== respIndex);
    setExperience(updated);
  };

  const updateResponsibility = (expIndex, respIndex, value) => {
    const updated = [...experience];
    updated[expIndex].responsibilities[respIndex] = value;
    setExperience(updated);
  };

  const addProject = () => {
    setProjects([...projects, { name: '', description: '', technologies: '', link: '' }]);
  };

  const removeProject = (index) => {
    setProjects(projects.filter((_, i) => i !== index));
  };

  const updateProject = (index, field, value) => {
    const updated = [...projects];
    updated[index][field] = value;
    setProjects(updated);
  };

  const addCertification = () => {
    setCertifications([...certifications, '']);
  };

  const removeCertification = (index) => {
    setCertifications(certifications.filter((_, i) => i !== index));
  };

  const updateCertification = (index, value) => {
    const updated = [...certifications];
    updated[index] = value;
    setCertifications(updated);
  };

  const addAchievement = () => {
    setAchievements([...achievements, '']);
  };

  const removeAchievement = (index) => {
    setAchievements(achievements.filter((_, i) => i !== index));
  };

  const updateAchievement = (index, value) => {
    const updated = [...achievements];
    updated[index] = value;
    setAchievements(updated);
  };

  // ==================== GENERATE RESUME TEXT ====================

  const generateResumeText = () => {
    let resume = '';

    // Personal Information
    resume += `${personalInfo.fullName}\n`;
    if (personalInfo.email) resume += `Email: ${personalInfo.email}\n`;
    if (personalInfo.phone) resume += `Phone: ${personalInfo.phone}\n`;
    if (personalInfo.location) resume += `Location: ${personalInfo.location}\n`;
    if (personalInfo.linkedin) resume += `LinkedIn: ${personalInfo.linkedin}\n`;
    if (personalInfo.portfolio) resume += `Portfolio: ${personalInfo.portfolio}\n`;
    if (personalInfo.github) resume += `GitHub: ${personalInfo.github}\n`;
    resume += '\n';

    // Professional Summary
    if (summary) {
      resume += 'PROFESSIONAL SUMMARY\n';
      resume += `${summary}\n\n`;
    }

    // Education
    const validEducation = education.filter(edu => edu.degree || edu.institution);
    if (validEducation.length > 0) {
      resume += 'EDUCATION\n';
      validEducation.forEach(edu => {
        resume += `${edu.degree}${edu.institution ? ` - ${edu.institution}` : ''}\n`;
        if (edu.location) resume += `${edu.location}\n`;
        if (edu.year) resume += `${edu.year}\n`;
        if (edu.gpa) resume += `GPA: ${edu.gpa}\n`;
        if (edu.description) resume += `${edu.description}\n`;
        resume += '\n';
      });
    }

    // Work Experience
    const validExperience = experience.filter(exp => exp.company || exp.position);
    if (validExperience.length > 0) {
      resume += 'WORK EXPERIENCE\n';
      validExperience.forEach(exp => {
        resume += `${exp.position}${exp.company ? ` at ${exp.company}` : ''}\n`;
        if (exp.location) resume += `${exp.location}\n`;
        if (exp.duration) resume += `${exp.duration}\n`;
        const validResponsibilities = exp.responsibilities.filter(r => r.trim());
        if (validResponsibilities.length > 0) {
          validResponsibilities.forEach(resp => {
            resume += `• ${resp}\n`;
          });
        }
        resume += '\n';
      });
    }

    // Projects
    const validProjects = projects.filter(proj => proj.name || proj.description);
    if (validProjects.length > 0) {
      resume += 'PROJECTS\n';
      validProjects.forEach(proj => {
        if (proj.name) resume += `${proj.name}\n`;
        if (proj.description) resume += `${proj.description}\n`;
        if (proj.technologies) resume += `Technologies: ${proj.technologies}\n`;
        if (proj.link) resume += `Link: ${proj.link}\n`;
        resume += '\n';
      });
    }

    // Skills
    const hasSkills = Object.values(skills).some(s => s.trim());
    if (hasSkills) {
      resume += 'SKILLS\n';
      if (skills.technical) resume += `Technical Skills: ${skills.technical}\n`;
      if (skills.tools) resume += `Tools & Platforms: ${skills.tools}\n`;
      if (skills.soft) resume += `Soft Skills: ${skills.soft}\n`;
      if (skills.languages) resume += `Languages: ${skills.languages}\n`;
      resume += '\n';
    }

    // Certifications
    const validCertifications = certifications.filter(cert => cert.trim());
    if (validCertifications.length > 0) {
      resume += 'CERTIFICATIONS\n';
      validCertifications.forEach(cert => {
        resume += `• ${cert}\n`;
      });
      resume += '\n';
    }

    // Achievements
    const validAchievements = achievements.filter(ach => ach.trim());
    if (validAchievements.length > 0) {
      resume += 'ACHIEVEMENTS\n';
      validAchievements.forEach(ach => {
        resume += `• ${ach}\n`;
      });
      resume += '\n';
    }

    return resume;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validation
    if (!personalInfo.fullName.trim()) {
      alert('Please enter your full name');
      return;
    }

    if (!summary.trim() && education.every(e => !e.degree) && experience.every(e => !e.position)) {
      alert('Please fill in at least your summary, education, or work experience');
      return;
    }

    const resumeText = generateResumeText();
    onSubmit(resumeText);
  };

  return (
    <div className="resume-form-container">
      <div className="form-header">
        <h2>Build Your Professional Resume</h2>
        <p>Fill in your details to create a comprehensive resume</p>
      </div>

      <form onSubmit={handleSubmit} className="resume-form">
        
        {/* ==================== PERSONAL INFORMATION ==================== */}
        <section className="form-section">
          <div className="section-header">
            <User size={24} />
            <h3>Personal Information</h3>
          </div>
          
          <div className="form-grid">
            <div className="form-group full-width">
              <label>Full Name *</label>
              <input
                type="text"
                value={personalInfo.fullName}
                onChange={(e) => handlePersonalInfoChange('fullName', e.target.value)}
                placeholder="John Doe"
                required
              />
            </div>

            <div className="form-group">
              <label>Email *</label>
              <input
                type="email"
                value={personalInfo.email}
                onChange={(e) => handlePersonalInfoChange('email', e.target.value)}
                placeholder="john@example.com"
                required
              />
            </div>

            <div className="form-group">
              <label>Phone</label>
              <input
                type="tel"
                value={personalInfo.phone}
                onChange={(e) => handlePersonalInfoChange('phone', e.target.value)}
                placeholder="+1 234 567 8900"
              />
            </div>

            <div className="form-group">
              <label>Location</label>
              <input
                type="text"
                value={personalInfo.location}
                onChange={(e) => handlePersonalInfoChange('location', e.target.value)}
                placeholder="City, Country"
              />
            </div>

            <div className="form-group">
              <label>LinkedIn</label>
              <input
                type="url"
                value={personalInfo.linkedin}
                onChange={(e) => handlePersonalInfoChange('linkedin', e.target.value)}
                placeholder="linkedin.com/in/yourprofile"
              />
            </div>

            <div className="form-group">
              <label>GitHub</label>
              <input
                type="url"
                value={personalInfo.github}
                onChange={(e) => handlePersonalInfoChange('github', e.target.value)}
                placeholder="github.com/username"
              />
            </div>

            <div className="form-group">
              <label>Portfolio</label>
              <input
                type="url"
                value={personalInfo.portfolio}
                onChange={(e) => handlePersonalInfoChange('portfolio', e.target.value)}
                placeholder="yourportfolio.com"
              />
            </div>
          </div>
        </section>

        {/* ==================== PROFESSIONAL SUMMARY ==================== */}
        <section className="form-section">
          <div className="section-header">
            <FileText size={24} />
            <h3>Professional Summary</h3>
          </div>
          
          <div className="form-group full-width">
            <textarea
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
              placeholder="Write a brief professional summary highlighting your experience, skills, and career goals..."
              rows="4"
            />
          </div>
        </section>

        {/* ==================== EDUCATION ==================== */}
        <section className="form-section">
          <div className="section-header">
            <GraduationCap size={24} />
            <h3>Education</h3>
            <button type="button" onClick={addEducation} className="add-btn">
              <Plus size={18} /> Add Education
            </button>
          </div>

          {education.map((edu, index) => (
            <div key={index} className="entry-card">
              {education.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeEducation(index)}
                  className="remove-btn"
                >
                  <Trash2 size={18} />
                </button>
              )}

              <div className="form-grid">
                <div className="form-group">
                  <label>Degree *</label>
                  <input
                    type="text"
                    value={edu.degree}
                    onChange={(e) => updateEducation(index, 'degree', e.target.value)}
                    placeholder="Bachelor of Science in Computer Science"
                  />
                </div>

                <div className="form-group">
                  <label>Institution *</label>
                  <input
                    type="text"
                    value={edu.institution}
                    onChange={(e) => updateEducation(index, 'institution', e.target.value)}
                    placeholder="University Name"
                  />
                </div>

                <div className="form-group">
                  <label>Location</label>
                  <input
                    type="text"
                    value={edu.location}
                    onChange={(e) => updateEducation(index, 'location', e.target.value)}
                    placeholder="City, State"
                  />
                </div>

                <div className="form-group">
                  <label>Year</label>
                  <input
                    type="text"
                    value={edu.year}
                    onChange={(e) => updateEducation(index, 'year', e.target.value)}
                    placeholder="2020 - 2024"
                  />
                </div>

                <div className="form-group">
                  <label>GPA (optional)</label>
                  <input
                    type="text"
                    value={edu.gpa}
                    onChange={(e) => updateEducation(index, 'gpa', e.target.value)}
                    placeholder="3.8/4.0"
                  />
                </div>

                <div className="form-group full-width">
                  <label>Description (optional)</label>
                  <textarea
                    value={edu.description}
                    onChange={(e) => updateEducation(index, 'description', e.target.value)}
                    placeholder="Relevant coursework, honors, activities..."
                    rows="2"
                  />
                </div>
              </div>
            </div>
          ))}
        </section>

        {/* ==================== WORK EXPERIENCE ==================== */}
        <section className="form-section">
          <div className="section-header">
            <Briefcase size={24} />
            <h3>Work Experience</h3>
            <button type="button" onClick={addExperience} className="add-btn">
              <Plus size={18} /> Add Experience
            </button>
          </div>

          {experience.map((exp, expIndex) => (
            <div key={expIndex} className="entry-card">
              {experience.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeExperience(expIndex)}
                  className="remove-btn"
                >
                  <Trash2 size={18} />
                </button>
              )}

              <div className="form-grid">
                <div className="form-group">
                  <label>Position *</label>
                  <input
                    type="text"
                    value={exp.position}
                    onChange={(e) => updateExperience(expIndex, 'position', e.target.value)}
                    placeholder="Software Engineer"
                  />
                </div>

                <div className="form-group">
                  <label>Company *</label>
                  <input
                    type="text"
                    value={exp.company}
                    onChange={(e) => updateExperience(expIndex, 'company', e.target.value)}
                    placeholder="Company Name"
                  />
                </div>

                <div className="form-group">
                  <label>Location</label>
                  <input
                    type="text"
                    value={exp.location}
                    onChange={(e) => updateExperience(expIndex, 'location', e.target.value)}
                    placeholder="City, State"
                  />
                </div>

                <div className="form-group">
                  <label>Duration</label>
                  <input
                    type="text"
                    value={exp.duration}
                    onChange={(e) => updateExperience(expIndex, 'duration', e.target.value)}
                    placeholder="Jan 2022 - Present"
                  />
                </div>

                <div className="form-group full-width">
                  <label>Responsibilities</label>
                  {exp.responsibilities.map((resp, respIndex) => (
                    <div key={respIndex} className="responsibility-row">
                      <input
                        type="text"
                        value={resp}
                        onChange={(e) => updateResponsibility(expIndex, respIndex, e.target.value)}
                        placeholder="Describe your responsibility or achievement..."
                      />
                      {exp.responsibilities.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeResponsibility(expIndex, respIndex)}
                          className="remove-responsibility-btn"
                        >
                          <Trash2 size={16} />
                        </button>
                      )}
                    </div>
                  ))}
                  <button
                    type="button"
                    onClick={() => addResponsibility(expIndex)}
                    className="add-responsibility-btn"
                  >
                    <Plus size={16} /> Add Responsibility
                  </button>
                </div>
              </div>
            </div>
          ))}
        </section>

        {/* ==================== PROJECTS ==================== */}
        <section className="form-section">
          <div className="section-header">
            <Code size={24} />
            <h3>Projects</h3>
            <button type="button" onClick={addProject} className="add-btn">
              <Plus size={18} /> Add Project
            </button>
          </div>

          {projects.map((proj, index) => (
            <div key={index} className="entry-card">
              {projects.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeProject(index)}
                  className="remove-btn"
                >
                  <Trash2 size={18} />
                </button>
              )}

              <div className="form-grid">
                <div className="form-group">
                  <label>Project Name</label>
                  <input
                    type="text"
                    value={proj.name}
                    onChange={(e) => updateProject(index, 'name', e.target.value)}
                    placeholder="E-commerce Platform"
                  />
                </div>

                <div className="form-group">
                  <label>Technologies Used</label>
                  <input
                    type="text"
                    value={proj.technologies}
                    onChange={(e) => updateProject(index, 'technologies', e.target.value)}
                    placeholder="React, Node.js, MongoDB"
                  />
                </div>

                <div className="form-group full-width">
                  <label>Description</label>
                  <textarea
                    value={proj.description}
                    onChange={(e) => updateProject(index, 'description', e.target.value)}
                    placeholder="Describe the project, your role, and key achievements..."
                    rows="3"
                  />
                </div>

                <div className="form-group full-width">
                  <label>Project Link (optional)</label>
                  <input
                    type="url"
                    value={proj.link}
                    onChange={(e) => updateProject(index, 'link', e.target.value)}
                    placeholder="https://github.com/username/project"
                  />
                </div>
              </div>
            </div>
          ))}
        </section>

        {/* ==================== SKILLS ==================== */}
        <section className="form-section">
          <div className="section-header">
            <Award size={24} />
            <h3>Skills</h3>
          </div>

          <div className="form-grid">
            <div className="form-group full-width">
              <label>Technical Skills</label>
              <input
                type="text"
                value={skills.technical}
                onChange={(e) => setSkills({ ...skills, technical: e.target.value })}
                placeholder="Python, JavaScript, React, Machine Learning, etc."
              />
            </div>

            <div className="form-group full-width">
              <label>Tools & Platforms</label>
              <input
                type="text"
                value={skills.tools}
                onChange={(e) => setSkills({ ...skills, tools: e.target.value })}
                placeholder="Git, Docker, AWS, VS Code, etc."
              />
            </div>

            <div className="form-group full-width">
              <label>Soft Skills</label>
              <input
                type="text"
                value={skills.soft}
                onChange={(e) => setSkills({ ...skills, soft: e.target.value })}
                placeholder="Leadership, Communication, Problem Solving, etc."
              />
            </div>

            <div className="form-group full-width">
              <label>Languages</label>
              <input
                type="text"
                value={skills.languages}
                onChange={(e) => setSkills({ ...skills, languages: e.target.value })}
                placeholder="English (Native), Spanish (Fluent), etc."
              />
            </div>
          </div>
        </section>

        {/* ==================== CERTIFICATIONS ==================== */}
        <section className="form-section">
          <div className="section-header">
            <Award size={24} />
            <h3>Certifications</h3>
            <button type="button" onClick={addCertification} className="add-btn">
              <Plus size={18} /> Add Certification
            </button>
          </div>

          {certifications.map((cert, index) => (
            <div key={index} className="list-item">
              <input
                type="text"
                value={cert}
                onChange={(e) => updateCertification(index, e.target.value)}
                placeholder="AWS Certified Solutions Architect - 2023"
              />
              {certifications.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeCertification(index)}
                  className="remove-list-btn"
                >
                  <Trash2 size={18} />
                </button>
              )}
            </div>
          ))}
        </section>

        {/* ==================== ACHIEVEMENTS ==================== */}
        <section className="form-section">
          <div className="section-header">
            <Award size={24} />
            <h3>Achievements & Awards</h3>
            <button type="button" onClick={addAchievement} className="add-btn">
              <Plus size={18} /> Add Achievement
            </button>
          </div>

          {achievements.map((ach, index) => (
            <div key={index} className="list-item">
              <input
                type="text"
                value={ach}
                onChange={(e) => updateAchievement(index, e.target.value)}
                placeholder="Won first place in National Hackathon 2023"
              />
              {achievements.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeAchievement(index)}
                  className="remove-list-btn"
                >
                  <Trash2 size={18} />
                </button>
              )}
            </div>
          ))}
        </section>

        {/* ==================== FORM ACTIONS ==================== */}
        <div className="form-actions">
          <button type="button" onClick={onCancel} className="cancel-btn">
            Cancel
          </button>
          <button type="submit" className="submit-btn">
            Generate Resume & Continue
          </button>
        </div>
      </form>
    </div>
  );
}