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
    console.log('JWT Token:', token); // Log the JWT token for debugging purposes
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
      risk_tolerance: parseInt(riskTolerance, 10), // Ensure this is an integer
      investment_type: investmentType,
      investment_reason: investmentReason,
      income_range: incomeRange,
      investment_experience: investmentExperience,
      preferred_sectors: preferredSectors, // Send selected preferred sector(s)
    };

    try {
      // Send data to backend API
      const response = await axios.post(
        'http://127.0.0.1:8000/api/api/profile/', 
        userProfileData,
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`, // Attach token in the Authorization header
          },
        }
      );

      if (response.status === 201) {
        console.log('Profile saved successfully');
        // Redirect after successful profile save
        navigate('/home');
      }
    } catch (error) {
      console.error('Error saving profile:', error);
      if (error.response && error.response.status === 401) {
        // Token expired or invalid
        setErrorMessage('Session expired. Please log in again.');
        localStorage.removeItem('jwtToken'); // Remove expired token
        navigate('/'); // Redirect to login page
      } else {
        setErrorMessage('Failed to save profile. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">User Info</h1>

      {errorMessage && (
        <div className="bg-red-500 text-white p-3 mb-4 rounded">
          {errorMessage}
        </div>
      )}

      <form onSubmit={handleSaveProfile}>
        <div className="mb-4">
          <label className="block text-gray-700" htmlFor="name">
            Name:
          </label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-1 p-2 w-full border border-gray-300 rounded"
            required
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700" htmlFor="risk_tolerance">
            Risk Tolerance (1-10):
          </label>
          <input
            type="number"
            id="risk_tolerance"
            min="1"
            max="10"
            value={riskTolerance}
            onChange={(e) => setRiskTolerance(e.target.value)}
            className="mt-1 p-2 w-full border border-gray-300 rounded"
            required
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700" htmlFor="investment_type">
            Investment Type:
          </label>
          <select
            id="investment_type"
            value={investmentType}
            onChange={(e) => setInvestmentType(e.target.value)}
            className="mt-1 p-2 w-full border border-gray-300 rounded"
            required
          >
            <option value="">Select Investment Type</option>
            <option value="short-term">Short-term</option>
            <option value="mid-term">Mid-term</option>
            <option value="long-term">Long-term</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-gray-700" htmlFor="investment_reason">
            Investment Reason:
          </label>
          <select
            id="investment_reason"
            value={investmentReason}
            onChange={(e) => setInvestmentReason(e.target.value)}
            className="mt-1 p-2 w-full border border-gray-300 rounded"
            required
          >
            <option value="">Select Investment Reason</option>
            <option value="wealth growth">Wealth Growth</option>
            <option value="education">Education</option>
            <option value="retirement">Retirement</option>
            <option value="estate">Estate</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-gray-700" htmlFor="income_range">
            Income Range:
          </label>
          <select
            id="income_range"
            value={incomeRange}
            onChange={(e) => setIncomeRange(e.target.value)}
            className="mt-1 p-2 w-full border border-gray-300 rounded"
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

        <div className="mb-4">
          <label className="block text-gray-700" htmlFor="investment_experience">
            Investment Experience:
          </label>
          <select
            id="investment_experience"
            value={investmentExperience}
            onChange={(e) => setInvestmentExperience(e.target.value)}
            className="mt-1 p-2 w-full border border-gray-300 rounded"
            required
          >
            <option value="">Select Investment Experience</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-gray-700" htmlFor="preferred_sectors">
            Preferred Sectors:
          </label>
          <select
            id="preferred_sectors"
            value={preferredSectors}
            onChange={(e) => setPreferredSectors(e.target.value)}
            className="mt-1 p-2 w-full border border-gray-300 rounded"
            required
          >
            <option value="">Select Preferred Sector</option>
            <option value="education">Education</option>
            <option value="realestate">Real Estate</option>
            <option value="wealthgrowth">Wealth Growth</option>
          </select>
        </div>

        <div className="mb-4">
          <button
            type="submit"
            className="bg-blue-500 text-white p-2 w-full rounded"
            disabled={isLoading}
          >
            {isLoading ? 'Saving...' : 'Save Profile'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default UserInfo;
