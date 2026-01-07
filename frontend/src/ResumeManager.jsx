import React, { useState, useEffect } from 'react';
import { Trash2, FileText, Calendar, Loader } from 'lucide-react';
import './ResumeManager.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

/**
 * ResumeManager Component
 * Modal dialog to view and delete user resumes
 * 
 * Props:
 * - userId: User's Firebase UID (string)
 * - onClose: Callback when closing modal (function)
 * - onResumeDeleted: Callback when resume is deleted (function)
 */
export function ResumeManager({ userId, onClose, onResumeDeleted }) {
  // State management
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(null);
  const [error, setError] = useState('');

  // Fetch resumes when component mounts
  useEffect(() => {
    fetchResumes();
  }, [userId]);

  /**
   * Fetch all resumes for the current user
   */
  const fetchResumes = async () => {
    try {
      setLoading(true);
      setError('');
      
      const response = await fetch(`${API_URL}/get-resumes/${userId}`);
      const data = await response.json();
      
      if (response.ok) {
        setResumes(data.resumes || []);
        console.log('Resumes loaded:', data.resumes?.length || 0);
      } else {
        setError(data.error || 'Failed to load resumes');
        console.error('Failed to fetch resumes:', data.error);
      }
    } catch (err) {
      setError('Failed to load resumes. Please try again.');
      console.error('Error fetching resumes:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Delete a resume after user confirmation
   * @param {string} resumeId - ID of resume to delete
   */
  const handleDeleteResume = async (resumeId) => {
    // Ask for confirmation before deleting
    if (!window.confirm('Are you sure you want to delete this resume? This action cannot be undone.')) {
      return;
    }

    try {
      setDeleting(resumeId);
      const response = await fetch(
        `${API_URL}/delete-resume/${userId}/${resumeId}`,
        { method: 'DELETE' }
      );

      if (response.ok) {
        // Remove from local state
        setResumes(resumes.filter(r => r.id !== resumeId));
        console.log('Resume deleted successfully');
        
        // Notify parent component to update upload count
        if (onResumeDeleted) {
          onResumeDeleted();
        }
      } else {
        const data = await response.json();
        setError(data.error || 'Failed to delete resume');
        console.error('Failed to delete resume:', data.error);
      }
    } catch (err) {
      setError('Failed to delete resume. Please try again.');
      console.error('Error deleting resume:', err);
    } finally {
      setDeleting(null);
    }
  };

  /**
   * Format Firebase timestamp to readable date
   * @param {object} timestamp - Firebase timestamp object
   * @returns {string} Formatted date string
   */
  const formatDate = (timestamp) => {
    if (!timestamp) return 'Unknown';
    try {
      if (timestamp.seconds) {
        const date = new Date(timestamp.seconds * 1000);
        return date.toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'short', 
          day: 'numeric' 
        });
      }
      return 'Unknown';
    } catch {
      return 'Unknown';
    }
  };

  /**
   * Get badge color based on resume source
   * @param {string} source - 'pdf' or 'manual'
   * @returns {string} Color hex code
   */
  const getSourceBadgeColor = (source) => {
    return source === 'pdf' ? '#3b82f6' : '#10b981';
  };

  /**
   * Get badge label based on resume source
   * @param {string} source - 'pdf' or 'manual'
   * @returns {string} Formatted label
   */
  const getSourceLabel = (source) => {
    return source === 'pdf' ? '📄 PDF Upload' : '✍️ Manual Build';
  };

  /**
   * Calculate word count from text
   * @param {string} text - Resume text
   * @returns {number} Word count
   */
  const getWordCount = (text) => {
    if (!text) return 0;
    const words = text.trim().split(/\s+/).length;
    return words;
  };

  // ==================== LOADING STATE ====================
  if (loading) {
    return (
      <div className="resume-manager-overlay">
        <div className="resume-manager-modal">
          <div className="modal-header">
            <h2>My Resumes</h2>
            <button onClick={onClose} className="close-btn">✕</button>
          </div>
          <div className="loading-center">
            <Loader size={40} className="spinner" />
            <p>Loading your resumes...</p>
          </div>
        </div>
      </div>
    );
  }

  // ==================== MAIN RENDER ====================
  return (
    <div className="resume-manager-overlay">
      <div className="resume-manager-modal">
        {/* ========== HEADER ========== */}
        <div className="modal-header">
          <h2>My Resumes</h2>
          <button 
            onClick={onClose} 
            className="close-btn" 
            title="Close"
          >
            ✕
          </button>
        </div>

        {/* ========== ERROR MESSAGE ========== */}
        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {/* ========== CONTENT ========== */}
        {resumes.length === 0 ? (
          // Empty state
          <div className="empty-state">
            <FileText size={48} />
            <p>No resumes yet</p>
            <small>Upload or build your first resume to get started</small>
          </div>
        ) : (
          // Resume list
          <div className="resumes-list">
            {resumes.map((resume, index) => (
              <div key={resume.id} className="resume-item">
                {/* Resume Information */}
                <div className="resume-info">
                  <div className="resume-icon">
                    <FileText size={24} />
                  </div>
                  <div className="resume-details">
                    <h3>Resume #{index + 1}</h3>
                    
                    {/* Resume Metadata */}
                    <div className="resume-meta">
                      <span 
                        className="source-badge" 
                        style={{ backgroundColor: getSourceBadgeColor(resume.source) }}
                      >
                        {getSourceLabel(resume.source)}
                      </span>
                      <span className="date-badge">
                        <Calendar size={14} />
                        {formatDate(resume.created_at)}
                      </span>
                      <span className="text-length">
                        {getWordCount(resume.text)} words
                      </span>
                    </div>
                    
                    {/* Preview Text */}
                    <p className="resume-preview">
                      {resume.text.substring(0, 150).trim()}...
                    </p>
                  </div>
                </div>

                {/* Delete Button */}
                <button
                  onClick={() => handleDeleteResume(resume.id)}
                  disabled={deleting === resume.id}
                  className="delete-btn"
                  title="Delete this resume"
                >
                  {deleting === resume.id ? (
                    <Loader size={20} className="spinner-small" />
                  ) : (
                    <Trash2 size={20} />
                  )}
                </button>
              </div>
            ))}
          </div>
        )}

        {/* ========== FOOTER ========== */}
        <div className="modal-footer">
          <button onClick={onClose} className="close-modal-btn">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}