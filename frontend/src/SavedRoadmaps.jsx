import React, { useState, useEffect, useCallback } from 'react';
import { X, Trash2, Calendar, Target, TrendingUp, BookOpen, Loader } from 'lucide-react';
import { db } from './firebaseConfig';
import { collection, query, where, getDocs, deleteDoc, doc } from 'firebase/firestore';
import './SavedRoadmaps.css';

export function SavedRoadmaps({ userId, onClose, onViewRoadmap }) {
  const [roadmaps, setRoadmaps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deleting, setDeleting] = useState(null);

  const fetchRoadmaps = useCallback(async () => {
    try {
      setLoading(true);
      setError('');
      
      // Simple query without orderBy to avoid index issues
      const q = query(
        collection(db, 'saved_roadmaps'),
        where('user_id', '==', userId)
      );
      
      const snapshot = await getDocs(q);
      const roadmapData = [];
      
      snapshot.forEach((doc) => {
        roadmapData.push({
          id: doc.id,
          ...doc.data()
        });
      });
      
      // Sort in JavaScript instead of Firestore
      roadmapData.sort((a, b) => {
        const timeA = a.created_at?.seconds || 0;
        const timeB = b.created_at?.seconds || 0;
        return timeB - timeA; // Newest first
      });
      
      setRoadmaps(roadmapData);
      console.log(`✅ Loaded ${roadmapData.length} saved roadmaps`);
    } catch (err) {
      console.error('Error fetching roadmaps:', err);
      console.error('Full error:', err.message);
      setError(`Failed to load roadmaps: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchRoadmaps();
  }, [fetchRoadmaps]);

  const handleDelete = async (roadmapId) => {
    if (!window.confirm('Are you sure you want to delete this roadmap? This action cannot be undone.')) {
      return;
    }

    try {
      setDeleting(roadmapId);
      await deleteDoc(doc(db, 'saved_roadmaps', roadmapId));
      
      setRoadmaps(roadmaps.filter(r => r.id !== roadmapId));
      console.log('✅ Roadmap deleted');
    } catch (err) {
      console.error('Error deleting roadmap:', err);
      setError('Failed to delete roadmap');
    } finally {
      setDeleting(null);
    }
  };

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

  return (
    <div className="saved-roadmaps-overlay">
      <div className="saved-roadmaps-modal">
        {/* Header */}
        <div className="roadmaps-header">
          <div className="header-content">
            <BookOpen size={28} />
            <div>
              <h2>My Saved Roadmaps</h2>
              <p>You have {roadmaps.length}/3 saved roadmaps</p>
            </div>
          </div>
          <button onClick={onClose} className="close-btn" title="Close">
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="roadmaps-content">
          {loading ? (
            <div className="loading-state">
              <Loader size={48} className="spinner" />
              <p>Loading your roadmaps...</p>
            </div>
          ) : error ? (
            <div className="error-state">
              <p>⚠️ {error}</p>
              <button onClick={fetchRoadmaps} className="retry-btn">
                Try Again
              </button>
            </div>
          ) : roadmaps.length === 0 ? (
            <div className="empty-state">
              <BookOpen size={64} />
              <h3>No Saved Roadmaps Yet</h3>
              <p>Complete a resume analysis and save your roadmap to see it here!</p>
            </div>
          ) : (
            <div className="roadmaps-grid">
              {roadmaps.map((roadmap) => (
                <div key={roadmap.id} className="roadmap-card">
                  <div className="roadmap-card-header">
                    <div className="role-badge">
                      <Target size={16} />
                      {roadmap.target_role}
                    </div>
                    <button
                      onClick={() => handleDelete(roadmap.id)}
                      disabled={deleting === roadmap.id}
                      className="delete-icon-btn"
                      title="Delete roadmap"
                    >
                      {deleting === roadmap.id ? (
                        <Loader size={18} className="spinner-small" />
                      ) : (
                        <Trash2 size={18} />
                      )}
                    </button>
                  </div>

                  <div className="roadmap-stats">
                    <div className="stat-item">
                      <TrendingUp size={20} />
                      <div>
                        <span className="stat-value">{roadmap.match_score}%</span>
                        <span className="stat-label">Match Score</span>
                      </div>
                    </div>
                    
                    <div className="stat-item">
                      <Calendar size={20} />
                      <div>
                        <span className="stat-value">{roadmap.timeline_months}</span>
                        <span className="stat-label">Months</span>
                      </div>
                    </div>
                  </div>

                  <div className="roadmap-info">
                    <div className="info-row">
                      <span className="info-label">Skills to Learn:</span>
                      <span className="info-value">{roadmap.skill_gaps?.length || 0}</span>
                    </div>
                    <div className="info-row">
                      <span className="info-label">Roadmap Phases:</span>
                      <span className="info-value">{roadmap.roadmap?.length || 0}</span>
                    </div>
                    <div className="info-row">
                      <span className="info-label">Weekly Tasks:</span>
                      <span className="info-value">{roadmap.weekly_tasks?.length || 0}</span>
                    </div>
                  </div>

                  <div className="roadmap-date">
                    <Calendar size={14} />
                    Saved on {formatDate(roadmap.created_at)}
                  </div>

                  <button
                    onClick={() => {
                      onViewRoadmap(roadmap);
                      onClose();
                    }}
                    className="view-roadmap-btn"
                  >
                    View Full Roadmap
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="roadmaps-footer">
          <p>💡 Tip: You can save up to 3 roadmaps. Delete old ones to save new ones.</p>
          <button onClick={onClose} className="close-footer-btn">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}