import React, { useState } from 'react';
import { 
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  signOut 
} from 'firebase/auth';
import { auth } from './firebaseConfig';
import { LogOut, Mail, Lock, Chrome } from 'lucide-react';
import './Auth.css';

const googleProvider = new GoogleAuthProvider();

export function Login({ onLoginSuccess }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignup, setIsSignup] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Email/Password Authentication
  const handleAuth = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isSignup) {
        await createUserWithEmailAndPassword(auth, email, password);
        console.log('Account created successfully');
      } else {
        await signInWithEmailAndPassword(auth, email, password);
        console.log('Signed in successfully');
      }
      
      onLoginSuccess();
    } catch (err) {
      if (err.code === 'auth/email-already-in-use') {
        setError('Email already in use. Try logging in instead.');
      } else if (err.code === 'auth/weak-password') {
        setError('Password must be at least 6 characters.');
      } else if (err.code === 'auth/invalid-email') {
        setError('Invalid email address.');
      } else if (err.code === 'auth/user-not-found') {
        setError('No account found with this email.');
      } else if (err.code === 'auth/wrong-password') {
        setError('Incorrect password.');
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  // Google Sign-In
  const handleGoogleSignIn = async () => {
    setLoading(true);
    setError('');

    try {
      const result = await signInWithPopup(auth, googleProvider);
      console.log('Signed in with Google:', result.user.email);
      onLoginSuccess();
    } catch (err) {
      if (err.code === 'auth/operation-not-allowed') {
        setError('Google Sign-In is not enabled. Go to Firebase Console → Authentication → Sign-in method → Enable Google');
      } else if (err.code === 'auth/popup-blocked') {
        setError('Popup was blocked. Please allow popups and try again.');
      } else if (err.code !== 'auth/cancelled-popup-request') {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1 className="auth-title">SkillBridge</h1>
        <p className="auth-subtitle">AI Career & Skill Gap Advisor</p>

        <form onSubmit={handleAuth} className="auth-form">
          <div className="input-group">
            <label className="input-label">
              <Mail className="input-icon" />
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              className="input-field"
              required
            />
          </div>

          <div className="input-group">
            <label className="input-label">
              <Lock className="input-icon" />
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="input-field"
              required
              minLength="6"
            />
          </div>

          {error && <div className="error-alert">{error}</div>}

          <button type="submit" disabled={loading} className="auth-button">
            {loading ? 'Loading...' : isSignup ? 'Sign Up' : 'Login'}
          </button>
        </form>

        <div className="divider">
          <span>OR</span>
        </div>

        <button
          onClick={handleGoogleSignIn}
          disabled={loading}
          className="google-button"
        >
          <Chrome size={20} />
          Sign in with Google
        </button>

        <button
          onClick={() => {
            setIsSignup(!isSignup);
            setError('');
          }}
          className="toggle-button"
        >
          {isSignup ? 'Already have an account? Login' : "Don't have an account? Sign Up"}
        </button>
      </div>

      <div className="auth-help">
        <p>Having trouble? Make sure Google Sign-In is enabled in Firebase Console</p>
      </div>
    </div>
  );
}

export function LogoutButton() {
  const [loading, setLoading] = useState(false);

  const handleLogout = async () => {
    setLoading(true);
    try {
      await signOut(auth);
      console.log('Logged out successfully');
    } catch (err) {
      console.error('Logout error:', err);
      alert('Error logging out: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleLogout}
      disabled={loading}
      className="logout-btn"
      title="Click to logout"
    >
      <LogOut size={20} />
      <span>{loading ? 'Logging out...' : 'Logout'}</span>
    </button>
  );
}