import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const UserInfo = () => {
    const [riskTolerance, setRiskTolerance] = useState(5);
    const [investmentStyle, setInvestmentStyle] = useState('Moderate');
    const [experienceLevel, setExperienceLevel] = useState('Beginner');
    const navigate = useNavigate();

    const handleSave = async () => {
        const userData = { riskTolerance, investmentStyle, experienceLevel };
        await axios.post('/api/user-profile', userData);
        navigate('/homepage');
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
            <h1 className="text-3xl font-bold mb-4">User Investment Preferences</h1>
            <label>Risk Tolerance (1-10):</label>
            <input type="number" value={riskTolerance} onChange={(e) => setRiskTolerance(e.target.value)} className="mb-4 p-2 border rounded" min="1" max="10" />
            <label>Investment Style:</label>
            <select value={investmentStyle} onChange={(e) => setInvestmentStyle(e.target.value)} className="mb-4 p-2 border rounded">
                <option value="Conservative">Conservative</option>
                <option value="Moderate">Moderate</option>
                <option value="Aggressive">Aggressive</option>
            </select>
            <label>Experience Level:</label>
            <select value={experienceLevel} onChange={(e) => setExperienceLevel(e.target.value)} className="mb-4 p-2 border rounded">
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
            </select>
            <button onClick={handleSave} className="px-4 py-2 bg-blue-500 text-white rounded">Save & Continue</button>
        </div>
    );
};

export default UserInfo;
