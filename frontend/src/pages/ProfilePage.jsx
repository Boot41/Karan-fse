import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const ProfilePage = () => {
    const navigate = useNavigate();
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get('http://localhost:8001/api/profiles/me/', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            setProfile(response.data);
            localStorage.setItem('userProfile', JSON.stringify(response.data));
        } catch (err) {
            setError('Failed to load profile');
            console.error('Profile fetch error:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.clear();
        navigate('/');
    };

    if (loading) {
        return <div className="min-h-screen bg-black text-white flex items-center justify-center">Loading...</div>;
    }

    return (
        <div className="min-h-screen bg-black text-white">
            <nav className="bg-gray-900 p-4">
                <div className="container mx-auto flex justify-between items-center">
                    <h1 className="text-2xl font-bold text-purple-500">AI Investment Platform</h1>
                    <div className="flex space-x-4">
                        <button onClick={() => navigate('/home')} className="text-white hover:text-purple-400">Home</button>
                        <button onClick={() => navigate('/profile')} className="text-white hover:text-purple-400">Profile</button>
                        <button onClick={() => navigate('/about')} className="text-white hover:text-purple-400">About</button>
                        <button onClick={handleLogout} className="text-red-400 hover:text-red-300">Logout</button>
                    </div>
                </div>
            </nav>

            <div className="container mx-auto px-4 py-8">
                <div className="max-w-2xl mx-auto bg-gray-900 rounded-xl shadow-lg p-8">
                    <h2 className="text-3xl font-bold mb-6 text-center bg-gradient-to-r from-purple-400 to-pink-600 text-transparent bg-clip-text">
                        Your Profile
                    </h2>

                    {error && (
                        <div className="mb-4 p-3 bg-red-500 bg-opacity-20 border border-red-500 rounded text-red-500">
                            {error}
                        </div>
                    )}

                    {profile && (
                        <div className="space-y-6">
                            <div className="border-b border-gray-700 pb-4">
                                <h3 className="text-xl font-semibold mb-2 text-purple-400">Personal Information</h3>
                                <p><span className="text-gray-400">Email:</span> {user.email}</p>
                                <p><span className="text-gray-400">Full Name:</span> {profile.full_name}</p>
                            </div>

                            <div className="border-b border-gray-700 pb-4">
                                <h3 className="text-xl font-semibold mb-2 text-purple-400">Investment Profile</h3>
                                <p><span className="text-gray-400">Risk Tolerance:</span> {profile.risk_tolerance}/10</p>
                                <p><span className="text-gray-400">Investment Style:</span> {profile.investment_style}</p>
                                <p><span className="text-gray-400">Income Range:</span> {profile.income_range} LPA</p>
                            </div>

                            <div>
                                <h3 className="text-xl font-semibold mb-2 text-purple-400">Investment Details</h3>
                                <p><span className="text-gray-400">Investment Goal:</span> {profile.investment_goal}</p>
                                <p><span className="text-gray-400">Experience Level:</span> {profile.investment_experience}</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;
