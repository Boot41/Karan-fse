import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Welcome = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirm_password: '',
        username: ''
    });
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isSignUp, setIsSignUp] = useState(false); // Toggle between signup and login
    const navigate = useNavigate();

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
    
                response = await axios.post('http://127.0.0.1:8000/api/auth/register/', {
                    email: formData.email,
                    username: formData.username || formData.email,
                    password: formData.password,
                });
            } else {
                // Login
                if (!formData.email || !formData.password) {
                    setError('Email and Password are required');
                    setIsLoading(false);
                    return;
                }
    
                response = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
                    email: formData.email,
                    password: formData.password
                });
            }
    
            // Ensure response contains access and refresh tokens
            if (response.data.access && response.data.refresh && response.data.user) {
                // Save tokens and user info to localStorage
                localStorage.setItem('token', response.data.access);
                localStorage.setItem('refresh_token', response.data.refresh);
                localStorage.setItem('user', JSON.stringify(response.data.user));
    
                // Redirect to appropriate page after login or signup
                navigate(isSignUp ? '/userinfo' : '/home');
            } else {
                setError('Invalid response from server');
            }
        } catch (err) {
            console.error('Auth error:', err);
            let errorMessage = 'An error occurred';
    
            if (err.response?.data) {
                // Enhanced error handling
                if (typeof err.response.data === 'string') {
                    errorMessage = err.response.data;
                } else if (err.response.data.error) {
                    errorMessage = err.response.data.error;
                } else if (err.response.data.detail) {
                    errorMessage = err.response.data.detail;
                } else if (err.response.data.non_field_errors) {
                    errorMessage = err.response.data.non_field_errors[0];
                } else {
                    errorMessage = 'Unknown error';
                }
            }
    
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };
    

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value
        }));
    };

    return (
        <div className="flex justify-center items-center min-h-screen bg-gray-50">
            <div className="w-full max-w-md bg-white p-8 rounded-lg shadow-lg">
                <h1 className="text-3xl font-semibold text-center mb-6">{isSignUp ? 'Sign Up' : 'Login'}</h1>

                <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                        <label className="block text-gray-700">Email</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleInputChange}
                            required
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    <div className="mb-4">
                        <label className="block text-gray-700">Password</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleInputChange}
                            required
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    {isSignUp && (
                        <>
                            <div className="mb-4">
                                <label className="block text-gray-700">Confirm Password</label>
                                <input
                                    type="password"
                                    name="confirm_password"
                                    value={formData.confirm_password}
                                    onChange={handleInputChange}
                                    required
                                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                />
                            </div>

                            <div className="mb-4">
                                <label className="block text-gray-700">Username</label>
                                <input
                                    type="text"
                                    name="username"
                                    value={formData.username}
                                    onChange={handleInputChange}
                                    required
                                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                />
                            </div>
                        </>
                    )}

                    {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        {isLoading ? 'Processing...' : isSignUp ? 'Sign Up' : 'Login'}
                    </button>
                </form>

                <button
                    onClick={() => setIsSignUp(!isSignUp)}
                    className="mt-4 text-blue-500 hover:underline w-full text-center"
                >
                    {isSignUp ? 'Already have an account? Login' : 'Need an account? Sign Up'}
                </button>
            </div>
        </div>
    );
};

export default Welcome;
