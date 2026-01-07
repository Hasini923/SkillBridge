import React, { useState, useEffect } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth, db } from './firebaseConfig';
import { collection, query, where, getDocs, addDoc, serverTimestamp } from 'firebase/firestore';
import { Login, LogoutButton } from './Auth';
import { Logo } from './Logo';
import { ResumeBuilder } from './ResumeBuilder';
import { SkillsEditor } from './SkillsEditor';
import { ResumeManager } from './ResumeManager';
import { EnhancedSkillsDisplay } from './EnhancedSkillsDisplay';
import { SavedRoadmaps } from './SavedRoadmaps';
import TargetRoleSelector from './TargetRoleSelector';
import { extractTextFromPDF } from './pdfUtils';
import { FileText, BookOpen, Save, Check } from 'lucide-react';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export default function App() {
  // ==================== STATE MANAGEMENT ====================
  
  // Authentication
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);
  
  // Screen navigation
  const [currentScreen, setCurrentScreen] = useState('resume'); 
  
  // Resume data
  const [resumeText, setResumeText] = useState('');
  const [resumeSource, setResumeSource] = useState('');
  const [uploadCount, setUploadCount] = useState(0);
  
  // Skills data
  const [currentSkills, setCurrentSkills] = useState({
    technical: [],
    soft: [],
    tools: [],
    languages: []
  });
  
  // Target role
  const [targetRole, setTargetRole] = useState('');
  
  // Analysis results
  const [analysisData, setAnalysisData] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState('');

  // Resume Manager Modal
  const [showResumeManager, setShowResumeManager] = useState(false);

  // Saved Roadmaps
  const [showSavedRoadmaps, setShowSavedRoadmaps] = useState(false);
  const [roadmapCount, setRoadmapCount] = useState(0);
  const [savingRoadmap, setSavingRoadmap] = useState(false);
  const [roadmapSaved, setRoadmapSaved] = useState(false);

  // ==================== INITIALIZE AUTH ====================
  
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      setUser(currentUser);
      
      if (currentUser) {
        console.log('User logged in:', currentUser.email);
        await checkUploadCount(currentUser.uid);
        await checkRoadmapCount(currentUser.uid);
        setCurrentScreen('resume');
      } else {
        console.log('User logged out');
        setCurrentScreen('login');
      }
      
      setAuthLoading(false);
    });

    return unsubscribe;
  }, []);

  // ==================== FIREBASE FUNCTIONS ====================

  const checkUploadCount = async (userId) => {
    try {
      const q = query(
        collection(db, 'user_resumes'),
        where('user_id', '==', userId)
      );
      const querySnapshot = await getDocs(q);
      setUploadCount(querySnapshot.size);
    } catch (error) {
      console.error('Error checking upload count:', error);
      setUploadCount(0);
    }
  };

  const checkRoadmapCount = async (userId) => {
    try {
      const q = query(
        collection(db, 'saved_roadmaps'),
        where('user_id', '==', userId)
      );
      const querySnapshot = await getDocs(q);
      setRoadmapCount(querySnapshot.size);
      console.log(`User has ${querySnapshot.size}/3 saved roadmaps`);
    } catch (error) {
      console.error('Error checking roadmap count:', error);
      setRoadmapCount(0);
    }
  };

  const saveResumeToFirebase = async (text, source) => {
    if (!user) return;

    try {
      const resumeRef = collection(db, 'user_resumes');
      await addDoc(resumeRef, {
        user_id: user.uid,
        email: user.email,
        text: text,
        source: source,
        created_at: serverTimestamp()
      });

      console.log('Resume saved to Firebase');
      await checkUploadCount(user.uid);
    } catch (error) {
      console.error('Error saving resume:', error);
    }
  };

  const saveAnalysisToFirebase = async (data) => {
    if (!user) return;

    try {
      const analysisRef = collection(db, 'user_analyses');
      await addDoc(analysisRef, {
        user_id: user.uid,
        email: user.email,
        target_role: data.targetRole,
        current_skills: data.currentSkills,
        skill_gaps: data.skillGaps,
        match_score: data.matchScore,
        roadmap: data.roadmap,
        weekly_tasks: data.weeklyTasks,
        created_at: serverTimestamp()
      });

      console.log('Analysis saved to Firebase');
    } catch (error) {
      console.error('Error saving analysis:', error);
    }
  };

  // ==================== ROADMAP SAVING ====================

  const handleSaveRoadmap = async () => {
    if (!user || !analysisData) {
      alert('Please complete an analysis first');
      return;
    }

    if (roadmapCount >= 3) {
      alert('You have reached the maximum of 3 saved roadmaps. Please delete an old one to save a new one.');
      return;
    }

    try {
      setSavingRoadmap(true);
      
      const roadmapRef = collection(db, 'saved_roadmaps');
      await addDoc(roadmapRef, {
        user_id: user.uid,
        email: user.email,
        target_role: analysisData.targetRole,
        current_skills: analysisData.currentSkills,
        skill_gaps: analysisData.skillGaps,
        match_score: analysisData.matchScore,
        readiness: analysisData.readiness,
        timeline_months: analysisData.timelineMonths,
        difficulty: analysisData.difficulty,
        roadmap: analysisData.roadmap,
        weekly_tasks: analysisData.weeklyTasks,
        strengths: analysisData.strengths,
        competitive_advantages: analysisData.competitiveAdvantages,
        created_at: serverTimestamp()
      });

      console.log('✅ Roadmap saved successfully!');
      await checkRoadmapCount(user.uid);
      setRoadmapSaved(true);
      
      setTimeout(() => {
        setRoadmapSaved(false);
      }, 3000);
      
    } catch (error) {
      console.error('Error saving roadmap:', error);
      alert('Failed to save roadmap: ' + error.message);
    } finally {
      setSavingRoadmap(false);
    }
  };

  const handleViewSavedRoadmap = (roadmap) => {
    setAnalysisData({
      targetRole: roadmap.target_role,
      currentSkills: roadmap.current_skills,
      skillGaps: roadmap.skill_gaps,
      matchScore: roadmap.match_score,
      readiness: roadmap.readiness,
      timelineMonths: roadmap.timeline_months,
      difficulty: roadmap.difficulty,
      roadmap: roadmap.roadmap,
      weeklyTasks: roadmap.weekly_tasks,
      strengths: roadmap.strengths,
      competitiveAdvantages: roadmap.competitive_advantages
    });
    
    setCurrentScreen('analysis');
    setRoadmapSaved(false);
  };

  // ==================== RESUME HANDLERS ====================

  const handleResumeUpload = async (file) => {
    try {
      console.log('Starting PDF upload...');
      const text = await extractTextFromPDF(file);
      console.log(`Extracted ${text.length} characters`);
      
      setResumeText(text);
      setResumeSource('pdf');
      await saveResumeToFirebase(text, 'pdf');
      await extractSkillsFromResume(text);
      setCurrentScreen('skills');
    } catch (error) {
      console.error('Error uploading resume:', error);
      alert('Failed to upload resume: ' + error.message);
    }
  };

  const handleResumeBuild = async (text) => {
    try {
      console.log('Processing manually built resume...');
      setResumeText(text);
      setResumeSource('manual');
      await saveResumeToFirebase(text, 'manual');
      await extractSkillsFromResume(text);
      setCurrentScreen('skills');
    } catch (error) {
      console.error('Error processing resume:', error);
      alert('Failed to process resume: ' + error.message);
    }
  };

  // ==================== SKILLS HANDLERS ====================

  const extractSkillsFromResume = async (text) => {
    try {
      console.log('Extracting skills from resume...');
      
      const response = await fetch(`${API_URL}/analyze-resume`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_text: text,
          target_role: 'General Professional',
          user_id: user ? user.uid : 'anonymous'
        })
      });

      if (!response.ok) {
        throw new Error('Failed to extract skills');
      }

      const data = await response.json();
      setCurrentSkills(data.currentSkills);
      console.log('Skills extracted:', data.currentSkills);
    } catch (error) {
      console.error('Error extracting skills:', error);
      alert('Failed to extract skills from resume');
    }
  };

  const handleSkillsUpdate = (updatedSkills) => {
    console.log('Skills updated:', updatedSkills);
    setCurrentSkills(updatedSkills);
    setCurrentScreen('targetRole');
  };

  // ==================== ANALYSIS HANDLERS ====================

  const handleAnalyzeResume = async (role) => {
    try {
      setAnalysisLoading(true);
      setAnalysisError('');
      setRoadmapSaved(false);
      
      console.log(`Analyzing resume for role: ${role}`);
      
      const response = await fetch(`${API_URL}/analyze-resume`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_text: resumeText,
          target_role: role,
          user_id: user ? user.uid : 'anonymous'
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Analysis failed');
      }

      const data = await response.json();
      setAnalysisData(data);
      setTargetRole(role);
      await saveAnalysisToFirebase(data);
      setCurrentScreen('analysis');
      console.log('Analysis complete!');
    } catch (error) {
      console.error('Error analyzing resume:', error);
      setAnalysisError(error.message);
    } finally {
      setAnalysisLoading(false);
    }
  };

  const goBack = () => {
    if (currentScreen === 'skills') {
      setCurrentScreen('resume');
      setResumeText('');
      setCurrentSkills({ technical: [], soft: [], tools: [], languages: [] });
    } else if (currentScreen === 'targetRole') {
      setCurrentScreen('skills');
    } else if (currentScreen === 'analysis') {
      setCurrentScreen('targetRole');
    }
  };

  // ==================== RENDER ====================

  if (authLoading) {
    return (
      <div className="loading-screen">
        <h1>SkillBridge</h1>
        <p>Loading...</p>
      </div>
    );
  }

  if (!user) {
    return <Login onLoginSuccess={() => setCurrentScreen('resume')} />;
  }

  // ==================== MAIN APP UI ====================

  return (
    <div className="app-container">
      {/* Logout Button - Bottom Right */}
      <LogoutButton />

      {/* My Roadmaps Button - Top Right */}
      <button 
        onClick={() => setShowSavedRoadmaps(true)}
        className="floating-roadmaps-btn"
        title="View your saved roadmaps"
      >
        <BookOpen size={22} />
        <span>My Roadmaps</span>
        <span className="roadmap-badge">{roadmapCount}/3</span>
      </button>

      {/* Resume Manager Modal */}
      {showResumeManager && (
        <ResumeManager 
          userId={user.uid}
          onClose={() => setShowResumeManager(false)}
          onResumeDeleted={() => checkUploadCount(user.uid)}
        />
      )}

      {/* Saved Roadmaps Modal */}
      {showSavedRoadmaps && (
        <SavedRoadmaps
          userId={user.uid}
          onClose={() => setShowSavedRoadmaps(false)}
          onViewRoadmap={handleViewSavedRoadmap}
        />
      )}

      {/* SCREEN 1: Resume Upload/Build */}
      {currentScreen === 'resume' && (
        <div className="screen">
          <div className="screen-header">
            <button 
              onClick={() => setShowResumeManager(true)}
              className="manage-resumes-btn"
              title="Manage your uploaded resumes"
            >
              <FileText size={20} />
              My Resumes ({uploadCount}/3)
            </button>
          </div>
          <ResumeBuilder
            onUploadResume={handleResumeUpload}
            onResumeBuild={handleResumeBuild}
            uploadCount={uploadCount}
          />
        </div>
      )}

      {/* SCREEN 2: Skills Editor */}
      {currentScreen === 'skills' && (
        <div className="screen">
          <div className="screen-header">
            <button onClick={goBack} className="back-button">
              ← Back
            </button>
          </div>
          <div className="skills-screen">
            <div className="skills-preview">
              <h2>Your Extracted Skills</h2>
              <EnhancedSkillsDisplay skills={currentSkills} />
            </div>
            <div className="skills-editor-section">
              <SkillsEditor
                extractedSkills={currentSkills}
                onSkillsUpdate={handleSkillsUpdate}
                onContinue={() => setCurrentScreen('targetRole')}
              />
            </div>
          </div>
        </div>
      )}

      {/* SCREEN 3: Target Role Selection */}
      {currentScreen === 'targetRole' && (
        <div className="screen">
          <div className="screen-header">
            <button onClick={goBack} className="back-button">
              ← Back
            </button>
          </div>
          <TargetRoleSelector
            onAnalyze={handleAnalyzeResume}
            loading={analysisLoading}
            error={analysisError}
          />
        </div>
      )}

      {/* SCREEN 4: Analysis Results with Save Button */}
      {currentScreen === 'analysis' && analysisData && (
        <div className="screen">
          <div className="screen-header">
            <button onClick={() => setCurrentScreen('resume')} className="new-analysis-button">
              ↻ Start New Analysis
            </button>
            <button 
              onClick={handleSaveRoadmap}
              disabled={savingRoadmap || roadmapSaved}
              className={`save-roadmap-button ${roadmapSaved ? 'saved' : ''}`}
              title={roadmapSaved ? 'Roadmap saved!' : 'Save this roadmap'}
            >
              {roadmapSaved ? (
                <>
                  <Check size={20} />
                  Saved!
                </>
              ) : savingRoadmap ? (
                'Saving...'
              ) : (
                <>
                  <Save size={20} />
                  Save Roadmap
                </>
              )}
            </button>
          </div>
          <AnalysisResults data={analysisData} />
        </div>
      )}
    </div>
  );
}

/**
 * Analysis Results Component
 */
function AnalysisResults({ data }) {
  return (
    <div className="analysis-container">
      <h2>Your Career Analysis</h2>
      <p>Target Role: <strong>{data.targetRole}</strong></p>

      <div className="results-grid">
        <div className="result-card">
          <h3>Match Score</h3>
          <p className="big-number">{data.matchScore}%</p>
          <p className="subtitle">Readiness: {data.readiness}</p>
        </div>

        <div className="result-card">
          <h3>Timeline to Goal</h3>
          <p className="big-number">{data.timelineMonths}</p>
          <p className="subtitle">months</p>
        </div>

        <div className="result-card">
          <h3>Difficulty Level</h3>
          <p className="big-number">{data.difficulty}</p>
          <p className="subtitle">Based on skill gaps</p>
        </div>
      </div>

      <div className="section">
        <h3>Your Current Skills</h3>
        <EnhancedSkillsDisplay skills={data.currentSkills} />
      </div>

      <div className="section">
        <h3>Skills You Need ({data.skillGaps.length})</h3>
        <div className="gaps-list">
          {data.skillGaps.map((gap, idx) => (
            <div key={idx} className="gap-item">
              <strong>{gap.skill}</strong>
              <span className={`priority ${gap.importance.toLowerCase()}`}>
                {gap.importance}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="section">
        <h3>12-Week Learning Roadmap</h3>
        <div className="roadmap-phases">
          {data.roadmap.map((phase, idx) => (
            <div key={idx} className="phase">
              <h4>Week {phase.week}: {phase.phase}</h4>
              <p>{phase.focus}</p>
              <ul>
                {phase.tasks.map((task, taskIdx) => (
                  <li key={taskIdx}>{task}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {data.weeklyTasks && (
        <div className="section">
          <h3>Weekly Tasks (12 Weeks)</h3>
          <div className="tasks-list">
            {data.weeklyTasks.map((task, idx) => (
              <div key={idx} className="task-item">
                <strong>Week {task.week}: {task.task}</strong>
                <p>Outcome: {task.outcome}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="section">
        <h3>Your Strengths</h3>
        <ul>
          {data.strengths.map((strength, idx) => (
            <li key={idx}>{strength}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}