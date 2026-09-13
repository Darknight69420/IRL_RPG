// src/screens/Login.tsx
import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

type Props = { onSwitch: () => void };

const Login: React.FC<Props> = ({ onSwitch }) => {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login(email, password);
    } catch (err) {
      setError('Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-sm space-y-4">
      <h1 className="text-2xl font-bold text-center">Log In</h1>
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
          {loading ? 'Logging in...' : 'Log In'}
        </button>
      </form>
      <p className="text-center text-sm">
        Don't have an account?{' '}
        <button onClick={onSwitch} className="text-blue-600 underline">
          Sign up
        </button>
      </p>
    </div>
  );
};

export default Login;
