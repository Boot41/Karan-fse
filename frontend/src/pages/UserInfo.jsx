import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const UserInfo = () => {
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [formData, setFormData] = useState({
        full_name: '',
        risk_tolerance: 5,
        investment_style: 'Moderate',
        income_range: '',
        investment_goal: '',
        investment_experience: 'Beginner'
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/');
                return;
            }

            // First, create/update the profile
            const response = await axios.post(
                'http://localhost:8001/api/profiles/',
                formData,
                {
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json'
                    }
                }
            );

            if (response.data) {
                // Store the profile data in localStorage
                localStorage.setItem('userProfile', JSON.stringify(response.data));
                
                // Navigate to home page
                navigate('/home');
            }
        } catch (err) {
            console.error('Profile creation error:', err);
            setError(err.response?.data?.detail || 'Failed to create profile. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-black text-white py-8 px-4">
            <div className="max-w-2xl mx-auto">
                <h1 className="text-3xl font-bold mb-8 text-center bg-gradient-to-r from-purple-400 to-pink-600 text-transparent bg-clip-text">
                    Complete Your Profile
                </h1>

                {error && (
                    <div className="mb-6 p-4 bg-red-500 bg-opacity-20 border border-red-500 rounded-lg text-red-500">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block mb-2">Full Name</label>
                        <input
                            type="text"
                            name="full_name"
                            value={formData.full_name}
                            onChange={handleChange}
                            required
                            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-purple-500"
                        />
                    </div>

                    <div>
                        <label className="block mb-2">Risk Tolerance (1-10)</label>
                        <input
                            type="number"
                            name="risk_tolerance"
                            min="1"
                            max="10"
                            value={formData.risk_tolerance}
                            onChange={handleChange}
                            required
                            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-purple-500"
                        />
                    </div>

                    <div>
                        <label className="block mb-2">Investment Style</label>
                        <select
                            name="investment_style"
                            value={formData.investment_style}
                            onChange={handleChange}
                            required
                            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-purple-500"
                        >
                            <option value="Conservative">Conservative</option>
                            <option value="Moderate">Moderate</option>
                            <option value="Aggressive">Aggressive</option>
                        </select>
                    </div>

                    <div>
                        <label className="block mb-2">Income Range</label>
                        <select
                            name="income_range"
                            value={formData.income_range}
                            onChange={handleChange}
                            required
                            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-purple-500"
                        >
                            <option value="">Select Income Range</option>
                            <option value="0-5">0-5 LPA</option>
                            <option value="5-10">5-10 LPA</option>
                            <option value="10-20">10-20 LPA</option>
                            <option value="20+">20+ LPA</option>
                        </select>
                    </div>

                    <div>
                        <label className="block mb-2">Investment Goal</label>
                        <select
                            name="investment_goal"
                            value={formData.investment_goal}
                            onChange={handleChange}
                            required
                            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-purple-500"
                        >
                            <option value="">Select Investment Goal</option>
                            <option value="Retirement">Retirement</option>
                            <option value="Wealth Building">Wealth Building</option>
                            <option value="Short Term">Short Term Gains</option>
                            <option value="Regular Income">Regular Income</option>
                        </select>
                    </div>

                    <div>
                        <label className="block mb-2">Investment Experience</label>
                        <select
                            name="investment_experience"
                            value={formData.investment_experience}
                            onChange={handleChange}
                            required
                            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-purple-500"
                        >
                            <option value="Beginner">Beginner</option>
                            <option value="Intermediate">Intermediate</option>
                            <option value="Expert">Expert</option>
                        </select>
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading}
                        className={`w-full py-3 rounded-lg font-semibold ${
                            isLoading
                                ? 'bg-gray-600 cursor-not-allowed'
                                : 'bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600'
                        }`}
                    >
                        {isLoading ? 'Creating Profile...' : 'Complete Profile'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default UserInfo;
