import React, { useState, useEffect } from 'react';

const Profile = () => {
  const [userProfile, setUserProfile] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    try {
      const profileData = localStorage.getItem('userProfile');
      if (profileData) {
        setUserProfile(JSON.parse(profileData));  // Safely parse the JSON
      }
    } catch (err) {
      setError('Something went wrong while loading your profile. Please try again.');
      console.error('Error parsing JSON from localStorage:', err);
    }
  }, []);

  if (error) {
    return <div>{error}</div>;
  }

  if (!userProfile) {
    return <div>Loading...</div>;
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-12">
      <h2 className="text-2xl font-semibold mb-4">Your Profile</h2>
      
      <p><strong>Name:</strong> {userProfile.name}</p>
      <p><strong>Investment Experience:</strong> {userProfile.investment_experience}</p>
      <p><strong>Income Range:</strong> {userProfile.income_range}</p>
      <p><strong>Risk Tolerance:</strong> {userProfile.risk_tolerance}</p>
      <p><strong>Investment Type:</strong> {userProfile.investment_type}</p>
      <p><strong>Investment Reason:</strong> {userProfile.investment_reason}</p>
      <p><strong>Preferred Sectors:</strong> {userProfile.preferred_sectors}</p>
    </div>
  );
};

export default Profile;
