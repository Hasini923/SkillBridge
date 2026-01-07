import React, { useState } from 'react';
import { Upload, Plus } from 'lucide-react';
import { ResumeForm } from './ResumeForm';
import './ResumeBuilder.css';

export function ResumeBuilder({ onResumeBuild, onUploadResume, uploadCount = 0 }) {
  const [mode, setMode] = useState('select'); // select, upload, build
  const [fileName, setFileName] = useState('');

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.type !== 'application/pdf') {
      alert('Please upload a PDF file');
      return;
    }

    if (uploadCount >= 3) {
      alert('You have reached the maximum of 3 resume uploads. Please build manually or delete an old resume.');
      return;
    }

    setFileName(file.name);
    onUploadResume(file);
  };

  const handleFormSubmit = (resumeText) => {
    onResumeBuild(resumeText);
  };

  if (mode === 'select') {
    return (
      <div className="resume-selector">
        <h2>How would you like to create your resume profile?</h2>
        
        <div className="selector-options">
          <button
            onClick={() => setMode('upload')}
            disabled={uploadCount >= 3}
            className="selector-option upload-option"
          >
            <Upload size={40} />
            <h3>Upload Resume (PDF)</h3>
            <p>Upload and extract skills from your existing resume</p>
            <span className="upload-count">{uploadCount}/3 uploads used</span>
          </button>

          <button
            onClick={() => setMode('build')}
            className="selector-option build-option"
          >
            <Plus size={40} />
            <h3>Build from Scratch</h3>
            <p>Fill out a detailed form to create your professional resume</p>
          </button>
        </div>
      </div>
    );
  }

  if (mode === 'upload') {
    return (
      <div className="resume-upload">
        <button 
          onClick={() => setMode('select')}
          className="back-button"
        >
          ← Back
        </button>
        
        <h2>Upload Your Resume</h2>
        <p>Upload a PDF resume to extract your skills</p>

        <div className="upload-area">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            id="resume-file"
            className="file-input"
          />
          <label htmlFor="resume-file" className="upload-label">
            <Upload size={48} />
            <p>Click to upload or drag and drop</p>
            <span>PDF up to 10MB</span>
          </label>
        </div>

        {fileName && (
          <div className="file-info">
            ✅ {fileName}
          </div>
        )}
      </div>
    );
  }

  if (mode === 'build') {
    return (
      <ResumeForm 
        onSubmit={handleFormSubmit}
        onCancel={() => setMode('select')}
      />
    );
  }
}