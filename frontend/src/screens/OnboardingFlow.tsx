// src/screens/OnboardingFlow.tsx
import React, { useState } from 'react';
import { selectStarter } from '../mocks/authMock';
import { useAuth } from '../context/AuthContext';

const starters = ['Bulbasaur', 'Charmander', 'Squirtle']; // placeholder names

const OnboardingFlow: React.FC = () => {
  const [step, setStep] = useState<'dialog' | 'select'>('dialog');
  const { setOnboardingCompleted } = useAuth();

  const handleContinue = () => setStep('select');

  const handleSelect = async (name: string) => {
    await selectStarter(name);
    setOnboardingCompleted(true);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4 space-y-8">
      {step === 'dialog' && (
        <div className="flex flex-col items-center space-y-4">
          {/* Oak placeholder sprite */}
          <div className="w-32 h-32 bg-gray-400 flex items-center justify-center text-sm">
            Oak Sprite
          </div>
          <p className="text-center max-w-xs">The world is dangerous. You need a companion.</p>
          <button onClick={handleContinue} className="bg-blue-600 text-white px-4 py-2 rounded">
            Continue
          </button>
        </div>
      )}
      {step === 'select' && (
        <div className="flex flex-col items-center space-y-4">
          <p className="font-bold">Choose your starter</p>
          <div className="flex space-x-4">
            {starters.map((name) => (
              <button
                key={name}
                onClick={() => handleSelect(name)}
                className="w-20 h-20 bg-gray-300 flex items-center justify-center"
              >
                {name}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default OnboardingFlow;
