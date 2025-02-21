// Register component

import React, { useState } from 'react';
import axios from 'axios';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    try {
      await axios.post('http://localhost:5000/api/register', { email, password });
      // Redirect to login or profile setup
      window.location.href = '/profile-setup'; // Change this as needed
    } catch (err) {
      setError('Registration failed. Please try again.');
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold">Register</h2>
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} className="border p-2 mb-2 w-full" required />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} className="border p-2 mb-2 w-full" required />
        <input type="password" placeholder="Confirm Password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="border p-2 mb-2 w-full" required />
        <button type="submit" className="bg-blue-500 text-white p-2">Register</button>
      </form>
    </div>
  );
};

export default Register;
