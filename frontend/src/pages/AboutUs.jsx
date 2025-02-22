import React from 'react';
import { useNavigate } from 'react-router-dom';

const AboutUs = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.clear();
        navigate('/');
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
                <div className="max-w-4xl mx-auto">
                    <h2 className="text-4xl font-bold mb-8 text-center bg-gradient-to-r from-purple-400 to-pink-600 text-transparent bg-clip-text">
                        About AI Investment Platform
                    </h2>

                    <div className="grid gap-8">
                        <div className="bg-gray-900 rounded-xl p-6 shadow-lg">
                            <h3 className="text-2xl font-semibold mb-4 text-purple-400">Our Mission</h3>
                            <p className="text-gray-300">
                                We aim to democratize investment decision-making by leveraging artificial intelligence 
                                to provide personalized, data-driven investment insights to investors of all levels.
                            </p>
                        </div>

                        <div className="bg-gray-900 rounded-xl p-6 shadow-lg">
                            <h3 className="text-2xl font-semibold mb-4 text-purple-400">What We Offer</h3>
                            <ul className="list-disc list-inside text-gray-300 space-y-2">
                                <li>AI-powered investment recommendations</li>
                                <li>Personalized risk assessment</li>
                                <li>Real-time market analysis</li>
                                <li>Portfolio optimization strategies</li>
                                <li>Educational resources for investors</li>
                            </ul>
                        </div>

                        <div className="bg-gray-900 rounded-xl p-6 shadow-lg">
                            <h3 className="text-2xl font-semibold mb-4 text-purple-400">Why Choose Us</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="p-4 bg-gray-800 rounded-lg">
                                    <h4 className="text-xl font-semibold mb-2 text-purple-300">Advanced AI</h4>
                                    <p className="text-gray-400">Cutting-edge algorithms for market analysis</p>
                                </div>
                                <div className="p-4 bg-gray-800 rounded-lg">
                                    <h4 className="text-xl font-semibold mb-2 text-purple-300">Personalization</h4>
                                    <p className="text-gray-400">Tailored recommendations for your goals</p>
                                </div>
                                <div className="p-4 bg-gray-800 rounded-lg">
                                    <h4 className="text-xl font-semibold mb-2 text-purple-300">Security</h4>
                                    <p className="text-gray-400">Bank-grade security for your data</p>
                                </div>
                                <div className="p-4 bg-gray-800 rounded-lg">
                                    <h4 className="text-xl font-semibold mb-2 text-purple-300">Support</h4>
                                    <p className="text-gray-400">24/7 customer support</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AboutUs;
