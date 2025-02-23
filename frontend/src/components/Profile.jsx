import React from 'react';
import { useNavigate } from 'react-router-dom';

const Profile = () => {
    const navigate = useNavigate();

    const handleAddInvestment = () => {
        // Logic to add a new stock
    };

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold">User Portfolio</h1>
            {/* Portfolio details will be displayed here */}
            <button onClick={handleAddInvestment} className="px-4 py-2 bg-blue-500 text-white rounded">Add Investment</button>
            <button onClick={() => navigate('/homepage')} className="px-4 py-2 bg-gray-500 text-white rounded">Back to Dashboard</button>
        </div>
    );
};

export default Profile;
