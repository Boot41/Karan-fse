import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [userProfile, setUserProfile] = useState(null); // State for user data
  const [error, setError] = useState(null); // State to handle any potential errors

  useEffect(() => {
    try {
      // Load user data from localStorage or wherever it is stored
      const profileData = localStorage.getItem('userProfile');
      if (profileData) {
        setUserProfile(JSON.parse(profileData)); // Set the user profile in state
      }
    } catch (err) {
      console.error('Error parsing user profile data:', err);
      setError('Failed to load user profile data');
    }
  }, []);

  const handleSearch = () => {
    console.log('Searching for:', searchQuery);
    // You can navigate to a search results page or filter data based on the query
  };

  return (
    <div className="bg-gradient-to-r from-blue-500 via-purple-600 to-pink-500 min-h-screen p-8">
      {/* Navigation Bar */}
      <div className="flex justify-between items-center bg-gray-800 p-4 rounded-lg shadow-md mb-8">
        <h1 className="text-3xl font-bold text-white">AI-Driven Investment Advisory</h1>
        <div className="flex space-x-4">
          <button 
            className="bg-blue-600 text-white px-4 py-2 rounded-lg transition-transform transform hover:scale-110 hover:shadow-lg hover:bg-blue-700 active:scale-95 active:shadow-none"
            onClick={() => navigate('/dashboard')}
          >
            Dashboard
          </button>
        </div>
      </div>

      {/* Hero Section */}
      <div className="text-center text-white mb-12">
        <h2 className="text-4xl font-semibold mb-4">Unlock Your Investment Potential</h2>
        <p className="text-lg mb-8">Get personalized AI-driven recommendations based on your preferences, risk tolerance, and real-time market data.</p>
        <button
          className="bg-green-600 text-white px-6 py-3 rounded-lg text-lg transition-transform transform hover:scale-110 hover:shadow-lg active:scale-95 active:shadow-none"
          onClick={() => navigate('/get-started')} // This will redirect the user to the 'get-started' page
        >
          Get Started
        </button>
      </div>

      {/* Profile Section */}
      {userProfile ? (
        <div className="bg-white p-6 rounded-lg shadow-md mb-12">
          <h2 className="text-2xl font-semibold mb-4">Your Profile</h2>
          <p><strong>Name:</strong> {userProfile.name}</p>
          <p><strong>Investment Experience:</strong> {userProfile.investment_experience}</p>
          <p><strong>Income Range:</strong> {userProfile.income_range}</p>
          <p><strong>Risk Tolerance:</strong> {userProfile.risk_tolerance}</p>
          <p><strong>Investment Type:</strong> {userProfile.investment_type}</p>
          <p><strong>Investment Reason:</strong> {userProfile.investment_reason}</p>
        </div>
      ) : error ? (
        <div className="bg-red-100 p-6 rounded-lg shadow-md mb-12 text-red-800">
          <h2 className="text-2xl font-semibold mb-4">Error</h2>
          <p>{error}</p>
        </div>
      ) : (
        <div className="bg-gray-100 p-6 rounded-lg shadow-md mb-12 text-gray-600">
          <h2 className="text-2xl font-semibold mb-4">Loading Profile...</h2>
        </div>
      )}

      {/* Search Section */}
      <div className="bg-white p-8 rounded-lg shadow-md mb-12">
        <h2 className="text-2xl font-semibold mb-4 text-center">Ask AI for Investment Advice</h2>
        <div className="flex justify-center space-x-4">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Type your investment question..."
            className="flex-1 p-3 border border-gray-300 rounded-lg text-gray-700 focus:ring-2 focus:ring-blue-500 transition-transform transform hover:scale-105"
          />
          <button
            onClick={handleSearch}
            className="bg-green-600 text-white px-6 py-3 rounded-lg transition-transform transform hover:scale-110 hover:shadow-lg active:scale-95 active:shadow-none"
          >
            Ask AI
          </button>
        </div>
      </div>

      {/* Market Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
        <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow transform hover:scale-105">
          <h3 className="text-xl font-semibold mb-4">Latest Market News</h3>
          <ul className="space-y-3">
            <li><a href="#" className="text-blue-600 hover:underline">Tech stocks surge as earnings reports exceed expectations.</a></li>
            <li><a href="#" className="text-blue-600 hover:underline">Healthcare sector shows resilience amid economic uncertainty.</a></li>
            <li><a href="#" className="text-blue-600 hover:underline">Investors eye renewable energy as a long-term growth opportunity.</a></li>
          </ul>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow transform hover:scale-105">
          <h3 className="text-xl font-semibold mb-4">Personalized Investment Tips</h3>
          <p className="text-gray-700 mb-4">Based on your profile and market trends, consider the following:</p>
          <ul className="space-y-2 text-gray-700">
            <li>Diversify your portfolio to mitigate risks.</li>
            <li>Invest in sectors that align with future trends, such as AI and renewable energy.</li>
            <li>Regularly review your investments and adjust based on market conditions.</li>
          </ul>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow transform hover:scale-105">
          <h3 className="text-xl font-semibold mb-4">Educational Resources</h3>
          <p className="text-gray-700 mb-4">Enhance your investment knowledge with these resources:</p>
          <ul className="space-y-2 text-gray-700">
            <li><a href="/resources/webinars" className="text-blue-600 hover:underline">Webinars on Investment Strategies</a></li>
            <li><a href="/resources/articles" className="text-blue-600 hover:underline">Articles on Market Analysis</a></li>
            <li><a href="/resources/tools" className="text-blue-600 hover:underline">Tools for Portfolio Management</a></li>
          </ul>
        </div>
      </div>

      {/* CTA Section */}
      <div className="text-center mb-12">
        <h2 className="text-3xl font-semibold text-white mb-4">Start Making Informed Investment Decisions Today</h2>
        <p className="text-lg text-white mb-6">Leverage the power of AI to make smarter, data-backed decisions about your investments.</p>
      </div>
    </div>
  );
};

export default HomePage;
