// Profile Setup component

import React, { useState } from 'react';

const ProfileSetup = () => {
  const [step, setStep] = useState(0);
  const [preferences, setPreferences] = useState({ riskTolerance: '', investmentGoals: '' });

  const handleChange = (e) => {
    setPreferences({ ...preferences, [e.target.name]: e.target.value });
  };

  const handleNext = () => {
    setStep(step + 1);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Submit preferences to the backend
    console.log(preferences);
    // Redirect to dashboard or another page
    window.location.href = '/dashboard'; // Change this as needed
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold">Profile Setup</h2>
      <form onSubmit={handleSubmit}>
        {step === 0 && (
          <div>
            <select name="riskTolerance" value={preferences.riskTolerance} onChange={handleChange} className="border p-2 mb-2 w-full" required>
              <option value="">Select Risk Tolerance</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
            <button type="button" onClick={handleNext} className="bg-blue-500 text-white p-2">Next</button>
          </div>
        )}
        {step === 1 && (
          <div>
            <input type="text" name="investmentGoals" placeholder="Investment Goals" value={preferences.investmentGoals} onChange={handleChange} className="border p-2 mb-2 w-full" required />
            <button type="submit" className="bg-blue-500 text-white p-2">Submit</button>
          </div>
        )}
      </form>
      <div className="progress-bar">
        <div style={{ width: `${(step + 1) * 50}%` }} className="bg-blue-500 h-2" />
      </div>
    </div>
  );
};

export default ProfileSetup;
