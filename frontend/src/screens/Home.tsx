// src/screens/Home.tsx
import React from 'react';
import { useAuth } from '../context/AuthContext';

const Home: React.FC = () => {
  const { user } = useAuth();
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold">Welcome, {user?.username || 'Guest'}!</h1>
    </div>
  );
};

export default Home;
