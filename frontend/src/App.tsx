// src/App.tsx
import React, { useState } from 'react';
import { useAuth } from './context/AuthContext';
import Signup from './screens/Signup';
import Login from './screens/Login';
import OnboardingFlow from './screens/OnboardingFlow';
import Home from './screens/Home';

const App = () => {
  const { user, token, signup, login, justSignedUp, setJustSignedUp, onboardingCompleted } = useAuth();
  const [authMode, setAuthMode] = useState<'login' | 'signup'>('login');

  // If not authenticated, show login/signup
  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
        {authMode === 'login' ? (
          <Login onSwitch={() => setAuthMode('signup')} />
        ) : (
          <Signup onSwitch={() => setAuthMode('login')} />
        )}
      </div>
    );
  }

  // If just signed up, show onboarding flow
  if (justSignedUp && !onboardingCompleted) {
    return <OnboardingFlow />;
  }

  // Otherwise, show home
  return <Home />;
};

export default App;
