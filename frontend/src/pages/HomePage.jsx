import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const HomePage = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState(JSON.parse(localStorage.getItem('user') || '{}'));
    const [profile, setProfile] = useState(null);
    const [marketData, setMarketData] = useState({
        trends: [],
        recommendations: [],
        loading: true,
        error: null
    });

    useEffect(() => {
        fetchUserProfile();
        fetchMarketData();
    }, []);

    const fetchUserProfile = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/');
                return;
            }

            const response = await axios.get('http://localhost:8001/api/profiles/me/', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            setProfile(response.data);
        } catch (err) {
            console.error('Error fetching profile:', err);
            if (err.response?.status === 401) {
                navigate('/');
            }
        }
    };

    const fetchMarketData = async () => {
        try {
            const token = localStorage.getItem('token');
            setMarketData(prev => ({ ...prev, loading: true, error: null }));

            // Simulated market data API call
            const response = await axios.get('http://localhost:8001/api/market/trends/', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });

            setMarketData({
                trends: response.data.trends || [],
                recommendations: response.data.recommendations || [],
                loading: false,
                error: null
            });
        } catch (err) {
            console.error('Error fetching market data:', err);
            setMarketData(prev => ({
                ...prev,
                loading: false,
                error: 'Failed to load market data'
            }));
        }
    };

    const handleLogout = () => {
        localStorage.clear();
        navigate('/');
    };

    const handleRefreshData = () => {
        fetchMarketData();
    };

    const handleUpdateProfile = () => {
        navigate('/profile');
    };

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
                <div className="flex justify-between items-center mb-8">
                    <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-600 text-transparent bg-clip-text">
                        Welcome, {profile?.full_name || user.email}!
                    </h2>
                    <div className="space-x-4">
                        <button
                            onClick={handleRefreshData}
                            className="px-4 py-2 bg-purple-500 hover:bg-purple-600 rounded-lg transition-colors"
                            disabled={marketData.loading}
                        >
                            {marketData.loading ? 'Refreshing...' : 'Refresh Data'}
                        </button>
                        <button
                            onClick={handleUpdateProfile}
                            className="px-4 py-2 bg-pink-500 hover:bg-pink-600 rounded-lg transition-colors"
                        >
                            Update Profile
                        </button>
                    </div>
                </div>

                {marketData.error && (
                    <div className="mb-6 p-4 bg-red-500 bg-opacity-20 border border-red-500 rounded-lg text-red-500">
                        {marketData.error}
                    </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                        <h3 className="text-xl font-semibold mb-4 text-purple-400">Investment Overview</h3>
                        {profile && (
                            <div className="space-y-2 text-gray-300">
                                <p>Risk Tolerance: {profile.risk_tolerance}/10</p>
                                <p>Investment Style: {profile.investment_style}</p>
                                <p>Experience Level: {profile.investment_experience}</p>
                            </div>
                        )}
                    </div>

                    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                        <h3 className="text-xl font-semibold mb-4 text-purple-400">Market Trends</h3>
                        {marketData.loading ? (
                            <p className="text-gray-400">Loading market data...</p>
                        ) : (
                            <div className="space-y-2">
                                {marketData.trends.map((trend, index) => (
                                    <div key={index} className="p-2 bg-gray-700 rounded">
                                        <p className="text-sm">{trend.description}</p>
                                        <p className="text-xs text-gray-400 mt-1">{trend.date}</p>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                        <h3 className="text-xl font-semibold mb-4 text-purple-400">AI Insights</h3>
                        {marketData.loading ? (
                            <p className="text-gray-400">Generating insights...</p>
                        ) : (
                            <div className="space-y-2">
                                {marketData.recommendations.map((rec, index) => (
                                    <div key={index} className="p-2 bg-gray-700 rounded">
                                        <p className="font-medium">{rec.title}</p>
                                        <p className="text-sm text-gray-300 mt-1">{rec.description}</p>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HomePage;
