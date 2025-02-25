import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const UserInfo = () => {
  const navigate = useNavigate();

  // State to hold form data
  const [name, setName] = useState('');
  const [riskTolerance, setRiskTolerance] = useState(5);
  const [investmentType, setInvestmentType] = useState('');
  const [investmentReason, setInvestmentReason] = useState('');
  const [incomeRange, setIncomeRange] = useState('');
  const [investmentExperience, setInvestmentExperience] = useState('');
  const [preferredSectors, setPreferredSectors] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Check if user is logged in and handle token expiration
  useEffect(() => {
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      navigate('/'); // Redirect to Welcome page if not logged in
    }
  }, [navigate]);

  // Handle form submission
  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage('');

    const token = localStorage.getItem('jwtToken');
    if (!token) {
      setErrorMessage('You must be logged in to save your profile.');
      setIsLoading(false);
      return;
    }

    const userProfileData = {
      name,
      risk_tolerance: parseInt(riskTolerance, 10),
      investment_type: investmentType,
      investment_reason: investmentReason,
      income_range: incomeRange,
      investment_experience: investmentExperience,
      preferred_sectors: preferredSectors,
    };

    try {
      // Send the data to the backend
      const response = await axios.put(
        'http://127.0.0.1:8000/api/profile/save/', 
        userProfileData,
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      if (response.status === 200) {
        // Save profile data to localStorage
        localStorage.setItem('userProfile', JSON.stringify(userProfileData)); // Save as JSON string
        navigate('/home');
      }
    } catch (error) {
      console.error('Error saving profile:', error);
      if (error.response) {
        setErrorMessage(error.response.data.detail || 'Failed to save profile. Please try again.');
      } else if (error.request) {
        setErrorMessage('Server did not respond');
      } else {
        setErrorMessage('Something went wrong. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-50 py-10">
      <div className="w-full max-w-lg bg-white shadow-lg rounded-lg p-6">
        <h1 className="text-3xl font-semibold text-center text-gray-800 mb-6">User Information</h1>

        {errorMessage && (
          <div className="bg-red-500 text-white p-3 rounded mb-4">
            {errorMessage}
          </div>
        )}

        <form onSubmit={handleSaveProfile}>
          <div className="space-y-4">
            {/* Name */}
            <div>
              <label htmlFor="name" className="block text-gray-700">Name</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="mt-1 p-2 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Risk Tolerance */}
            <div>
              <label htmlFor="risk_tolerance" className="block text-gray-700">Risk Tolerance (1-10)</label>
              <input
                type="number"
                id="risk_tolerance"
                min="1"
                max="10"
                value={riskTolerance}
                onChange={(e) => setRiskTolerance(e.target.value)}
                className="mt-1 p-2 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Investment Type */}
            <div>
              <label htmlFor="investment_type" className="block text-gray-700">Investment Type</label>
              <select
                id="investment_type"
                value={investmentType}
                onChange={(e) => setInvestmentType(e.target.value)}
                className="mt-1 p-2 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select Investment Type</option>
                <option value="short-term">Short-term</option>
                <option value="mid-term">Mid-term</option>
                <option value="long-term">Long-term</option>
              </select>
            </div>

            {/* Investment Reason */}
            <div>
              <label htmlFor="investment_reason" className="block text-gray-700">Investment Reason</label>
              <select
                id="investment_reason"
                value={investmentReason}
                onChange={(e) => setInvestmentReason(e.target.value)}
                className="mt-1 p-2 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select Investment Reason</option>
                <option value="wealth growth">Wealth Growth</option>
                <option value="education">Education</option>
                <option value="retirement">Retirement</option>
                <option value="estate">Estate</option>
              </select>
            </div>

            {/* Income Range */}
            <div>
              <label htmlFor="income_range" className="block text-gray-700">Income Range</label>
              <select
                id="income_range"
                value={incomeRange}
                onChange={(e) => setIncomeRange(e.target.value)}
                className="mt-1 p-2 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select Income Range</option>
                <option value="under 2 LPA">Under 2 LPA</option>
                <option value="2 LPA - 5 LPA">2 LPA - 5 LPA</option>
                <option value="5 LPA - 10 LPA">5 LPA - 10 LPA</option>
                <option value="10 LPA - 15 LPA">10 LPA - 15 LPA</option>
                <option value="15 LPA - 20 LPA">15 LPA - 20 LPA</option>
                <option value="20 LPA+">20 LPA+</option>
              </select>
            </div>

            {/* Investment Experience */}
            <div>
              <label htmlFor="investment_experience" className="block text-gray-700">Investment Experience</label>
              <select
                id="investment_experience"
                value={investmentExperience}
                onChange={(e) => setInvestmentExperience(e.target.value)}
                className="mt-1 p-2 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select Investment Experience</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            {/* Preferred Sectors */}
            <div>
              <label htmlFor="preferred_sectors" className="block text-gray-700">Preferred Sectors</label>
              <select
                id="preferred_sectors"
                value={preferredSectors}
                onChange={(e) => setPreferredSectors(e.target.value)}
                className="mt-1 p-2 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select Preferred Sector</option>
                <option value="technology">Technology</option>
                <option value="healthcare">Healthcare</option>
                <option value="finance">Finance</option>
                <option value="real estate">Real Estate</option>
                <option value="energy">Energy</option>
                <option value="consumer goods">Consumer Goods</option>
              </select>
            </div>

            {/* Save Profile Button */}
            <div className="mt-6">
              <button
                type="submit"
                className="w-full py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                disabled={isLoading}
              >
                {isLoading ? 'Saving...' : 'Save Profile'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserInfo;
