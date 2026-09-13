// src/context/AuthContext.tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';
import { signup, login, AuthResponse } from '../mocks/authMock';

type User = { id: number; email: string; username: string };

type AuthContextType = {
  user: User | null;
  token: string | null;
  signup: (email: string, password: string) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  justSignedUp: boolean;
  setJustSignedUp: React.Dispatch<React.SetStateAction<boolean>>;
  onboardingCompleted: boolean;
  setOnboardingCompleted: React.Dispatch<React.SetStateAction<boolean>>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [justSignedUp, setJustSignedUp] = useState<boolean>(false);
  const [onboardingCompleted, setOnboardingCompleted] = useState<boolean>(false);

  const handleSignup = async (email: string, password: string) => {
    const res: AuthResponse = await signup(email, password);
    setUser(res.user);
    setToken(res.token);
    setJustSignedUp(true);
    setOnboardingCompleted(false);
  };

  const handleLogin = async (email: string, password: string) => {
    const res: AuthResponse = await login(email, password);
    setUser(res.user);
    setToken(res.token);
    setJustSignedUp(false);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        signup: handleSignup,
        login: handleLogin,
        justSignedUp,
        setJustSignedUp,
        onboardingCompleted,
        setOnboardingCompleted,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
