// src/screens/Signup.tsx
import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

type Props = { onSwitch: () => void };

const Signup: React.FC<Props> = ({ onSwitch }) => {
  const { signup } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await signup(email, password);
    } catch (err) {
      setError('Signup failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-sm space-y-4">
      <h1 className="text-2xl font-bold text-center">Sign Up</h1>
      {error && <p className="text-red-500 text-center">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white p-2 rounded"
        >
          {loading ? 'Signing up...' : 'Sign Up'}
        </button>
      </form>
      <p className="text-center text-sm">
        Already have an account?{' '}
        <button onClick={onSwitch} className="text-blue-600 underline">
          Log in
        </button>
      </p>
    </div>
  );
};

export default Signup;
