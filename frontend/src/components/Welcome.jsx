import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Welcome = () => {
    const [isSignUp, setIsSignUp] = useState(false);
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        password: '',
        confirm_password: ''
    });
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && e.target.form) {
            e.preventDefault();
            const form = e.target.form;
            const isValid = form.checkValidity();
            if (isValid) {
                handleSubmit(e);
            } else {
                form.reportValidity();
            }
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            let response;
            
            if (isSignUp) {
                // Registration
                if (formData.password !== formData.confirm_password) {
                    setError('Passwords do not match');
                    setIsLoading(false);
                    return;
                }
                
                response = await axios.post('http://localhost:8001/api/register/', {
                    email: formData.email,
                    username: formData.username || formData.email,
                    password: formData.password,
                    confirm_password: formData.confirm_password
                });
            } else {
                // Login
                response = await axios.post('http://localhost:8001/api/login/', {
                    email: formData.email,
                    password: formData.password
                });
            }
            
            if (response.data.token) {
                localStorage.setItem('token', response.data.token);
                localStorage.setItem('user', JSON.stringify(response.data.user));
                navigate(isSignUp ? '/userinfo' : '/home');
            }
        } catch (err) {
            console.error('Auth error:', err);
            let errorMessage = 'An error occurred';
            
            if (err.response?.data) {
                if (typeof err.response.data === 'string') {
                    errorMessage = err.response.data;
                } else if (err.response.data.error) {
                    errorMessage = err.response.data.error;
                } else if (err.response.data.detail) {
                    errorMessage = err.response.data.detail;
                } else if (err.response.data.non_field_errors) {
                    errorMessage = err.response.data.non_field_errors[0];
                }
            }
            
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center relative overflow-hidden">
            {/* Background Animation */}
            <div className="absolute inset-0">
                <div className="absolute top-0 -left-4 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
                <div className="absolute top-0 -right-4 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
                <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
            </div>

            <div className="relative z-10 bg-black bg-opacity-60 p-8 rounded-2xl shadow-xl backdrop-blur-sm w-96">
                <h1 className="text-4xl font-bold text-center mb-8 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
                    {isSignUp ? 'Create Account' : 'Welcome Back'}
                </h1>

                {error && (
                    <div className="mb-4 p-3 bg-red-500 bg-opacity-20 border border-red-500 rounded text-red-500">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium mb-2">Email</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleInputChange}
                            onKeyPress={handleKeyPress}
                            className="w-full p-3 bg-gray-900 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none transition-all"
                            required
                        />
                    </div>

                    {isSignUp && (
                        <div>
                            <label className="block text-sm font-medium mb-2">Username (optional)</label>
                            <input
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleInputChange}
                                onKeyPress={handleKeyPress}
                                className="w-full p-3 bg-gray-900 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none transition-all"
                            />
                        </div>
                    )}

                    <div>
                        <label className="block text-sm font-medium mb-2">Password</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleInputChange}
                            onKeyPress={handleKeyPress}
                            className="w-full p-3 bg-gray-900 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none transition-all"
                            required
                        />
                    </div>

                    {isSignUp && (
                        <div>
                            <label className="block text-sm font-medium mb-2">Confirm Password</label>
                            <input
                                type="password"
                                name="confirm_password"
                                value={formData.confirm_password}
                                onChange={handleInputChange}
                                onKeyPress={handleKeyPress}
                                className="w-full p-3 bg-gray-900 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none transition-all"
                                required
                            />
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={isLoading}
                        className={`w-full py-3 px-6 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg transition-all transform hover:scale-105 ${
                            isLoading ? 'opacity-70 cursor-not-allowed' : 'hover:opacity-90'
                        }`}
                    >
                        {isLoading ? 'Please wait...' : (isSignUp ? 'Sign Up' : 'Login')}
                    </button>
                </form>

                <div className="mt-6 text-center">
                    <button
                        onClick={() => {
                            setIsSignUp(!isSignUp);
                            setError('');
                            setFormData({
                                email: '',
                                username: '',
                                password: '',
                                confirm_password: ''
                            });
                        }}
                        className="text-sm text-purple-400 hover:text-purple-300"
                    >
                        {isSignUp
                            ? 'Already have an account? Login'
                            : "Don't have an account? Sign Up"}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Welcome;
