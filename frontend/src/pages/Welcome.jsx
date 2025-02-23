import React, { useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Welcome = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Add form validation and submission logic
    if (isLogin) {
      // Handle login
    } else {
      // Handle sign-up
      if (password !== confirmPassword) {
        toast.error('Passwords do not match!');
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-800 to-purple-600 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        <img src="/path/to/logo.png" alt="QuantumInvest Logo" className="mx-auto mb-4" />
        <h2 className="text-center text-2xl font-bold mb-4">AI-powered investment insights for smarter financial decisions.</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} className="border rounded w-full py-2 px-3" required />
          </div>
          <div className="mb-4">
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} className="border rounded w-full py-2 px-3" required />
          </div>
          {!isLogin && (
            <> 
              <div className="mb-4">
                <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} className="border rounded w-full py-2 px-3" required />
              </div>
              <div className="mb-4">
                <input type="password" placeholder="Confirm Password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="border rounded w-full py-2 px-3" required />
              </div>
            </>
          )}
          <button type="submit" className="bg-gradient-to-r from-blue-500 to-purple-500 text-white py-2 px-4 rounded w-full hover:opacity-80">{isLogin ? 'Sign In' : 'Sign Up'}</button>
          <button type="button" onClick={() => setIsLogin(!isLogin)} className="mt-4 text-blue-500 hover:underline">{isLogin ? 'Create an account' : 'Already have an account?'}</button>
        </form>
        <footer className="mt-6 text-center text-sm text-gray-600">
          <p>256-bit encryption • AI-driven analytics • SEC compliant</p>
        </footer>
      </div>
      <ToastContainer />
    </div>
  );
};

export default Welcome;
