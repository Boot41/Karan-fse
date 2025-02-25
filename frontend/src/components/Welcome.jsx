import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Welcome = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirm_password: '',
  });
  const [error, setError] = useState('');
  const [isSignUp, setIsSignUp] = useState(false); // Sign-up toggle
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      let response;

      if (isSignUp) {
        // Validation for required fields
        if (formData.password !== formData.confirm_password) {
          setError('Passwords do not match');
          setIsLoading(false);
          return;
        }

        if (!formData.email || !formData.password) {
          setError('Email and Password are required');
          setIsLoading(false);
          return;
        }

        // API request for sign-up
        response = await axios.post('http://127.0.0.1:8000/api/auth/register/', {
          email: formData.email,
          password: formData.password,
        });

        console.log('Sign-up response:', response.data); // Log the response for debugging

        if (response.data) {
          // After successful registration, automatically log in
          const loginResponse = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
            email: formData.email,
            password: formData.password,
          });

          // Store tokens and user info
          localStorage.setItem('jwtToken', loginResponse.data.access);
          localStorage.setItem('refreshToken', loginResponse.data.refresh);
          localStorage.setItem('user', JSON.stringify(loginResponse.data.user));

          onLogin(); // Notify App component
          navigate('/userinfo'); // Redirect to complete profile
        }
      } else {
        // API request for login
        response = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
          email: formData.email,
          password: formData.password,
        });

        console.log('Login response:', response.data); // Log the response for debugging
      }

      // Handle successful login response
      if (response?.data?.access && response?.data?.refresh && response?.data?.user) {
        localStorage.setItem('jwtToken', response.data.access);  // Store access token
        localStorage.setItem('refreshToken', response.data.refresh); // Store refresh token
        localStorage.setItem('user', JSON.stringify(response.data.user));  // Store user info

        onLogin(); // Notify App component about the login
        navigate('/home'); // Redirect to HomePage after login success
      }
    } catch (err) {
      console.error('Error during request:', err);

      if (err.response) {
        let errorMessage = 'An error occurred';

        if (err.response.data) {
          if (err.response.data.detail) {
            errorMessage = err.response.data.detail;  
          } else if (err.response.data.non_field_errors) {
            errorMessage = err.response.data.non_field_errors[0]; 
          } else if (err.response.data.email) {
            errorMessage = 'This email is already registered. Please try another one.';
          }
        }

        setError(errorMessage);  
      } else if (err.request) {
        setError('Server did not respond');
      } else {
        setError('Something went wrong. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-blue-500 via-purple-600 to-pink-500 p-4">
      <div className="bg-white shadow-lg rounded-lg p-8 max-w-sm w-full transform transition-all duration-300 ease-in-out hover:scale-105">
        <h2 className="text-3xl font-semibold text-center mb-6 text-blue-600">
          {isSignUp ? 'Sign Up' : 'Login'}
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-medium text-gray-600">
              Email
            </label>
            <input
              type="email"
              name="email"
              id="email"
              value={formData.email}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 mt-2 border rounded-md text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-400 transition-transform hover:scale-105"
            />
          </div>

          <div className="mb-4">
            <label htmlFor="password" className="block text-sm font-medium text-gray-600">
              Password
            </label>
            <input
              type="password"
              name="password"
              id="password"
              value={formData.password}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 mt-2 border rounded-md text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-400 transition-transform hover:scale-105"
            />
          </div>

          {isSignUp && (
            <>
              <div className="mb-4">
                <label htmlFor="confirm_password" className="block text-sm font-medium text-gray-600">
                  Confirm Password
                </label>
                <input
                  type="password"
                  name="confirm_password"
                  id="confirm_password"
                  value={formData.confirm_password}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-2 mt-2 border rounded-md text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-400 transition-transform hover:scale-105"
                />
              </div>
            </>
          )}

          {error && <div className="text-red-500 text-sm mb-4">{error}</div>}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-2 mt-4 rounded-md focus:outline-none hover:bg-blue-700 disabled:bg-gray-400 transition-all duration-300 ease-in-out transform hover:scale-105"
          >
            {isLoading ? 'Loading...' : isSignUp ? 'Sign Up' : 'Login'}
          </button>
        </form>

        <div className="text-center mt-4">
          {isSignUp ? (
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <button
                onClick={() => setIsSignUp(false)}
                className="text-blue-500 hover:underline"
              >
                Login
              </button>
            </p>
          ) : (
            <p className="text-sm text-gray-600">
              Don't have an account?{' '}
              <button
                onClick={() => setIsSignUp(true)}
                className="text-blue-500 hover:underline"
              >
                Sign Up
              </button>
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Welcome;
