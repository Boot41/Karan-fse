import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
    const navigate = useNavigate();

    const handleViewPortfolio = () => {
        navigate('/profile');
    };

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold">Dashboard</h1>
            <div className="my-4">
                <h2 className="text-xl">Investment Suggestions</h2>
                {/* AI-generated suggestions will be displayed here */}
            </div>
            <button onClick={handleViewPortfolio} className="px-4 py-2 bg-blue-500 text-white rounded">View Full Portfolio</button>
        </div>
    );
};

export default HomePage;
