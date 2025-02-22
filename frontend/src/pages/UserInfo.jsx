import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const UserInfo = () => {
    const [name, setName] = useState("");
    const [riskTolerance, setRiskTolerance] = useState(5);
    const [investmentStyle, setInvestmentStyle] = useState("short-term");
    const [incomeRange, setIncomeRange] = useState("2-5 LPA");
    const [investmentGoal, setInvestmentGoal] = useState("financial-growth");
    const [investmentExperience, setInvestmentExperience] = useState("beginner");

    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log({ name, riskTolerance, investmentStyle, incomeRange, investmentGoal, investmentExperience });
        alert("Profile information saved!");
        navigate('/home'); // Navigate to HomePage after submission
    };

    return (
        <div className="relative flex flex-col items-center justify-center min-h-screen bg-black text-white overflow-hidden">
            {/* Motion Background */}
            <div className="absolute inset-0">
                {/* Animated Waves */}
                <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-black via-gray-900 to-black animate-wave motion-reduce:animate-none opacity-70"></div>

                {/* Floating Glowing Particles */}
                <div className="absolute w-full h-full overflow-hidden">
                    {[...Array(25)].map((_, i) => (
                        <div
                            key={i}
                            className="absolute w-2 h-2 bg-orange-500 rounded-full opacity-80 animate-float"
                            style={{
                                top: `${Math.random() * 100}%`,
                                left: `${Math.random() * 100}%`,
                                animationDelay: `${Math.random() * 3}s`,
                                animationDuration: `${3 + Math.random() * 4}s`,
                            }}
                        ></div>
                    ))}
                </div>
            </div>

            <div className="relative z-10 w-full max-w-md px-6">
                <h2 className="text-4xl sm:text-5xl font-extrabold text-orange-500 mb-8 text-center animate-fadeIn">
                    Let’s Get Started 🚀
                </h2>

                <form
                    onSubmit={handleSubmit}
                    className="bg-gray-900 p-8 rounded-2xl shadow-lg backdrop-blur-md bg-opacity-80 transition-all duration-300 hover:shadow-orange-500/50"
                >
                    {/* Full Name */}
                    <div className="mb-6">
                        <label className="block text-lg font-semibold mb-2 text-orange-400">
                            Full Name
                        </label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className="w-full p-3 rounded-lg border border-gray-700 bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-orange-500 placeholder-gray-400 transition-transform transform hover:scale-105"
                            required
                        />
                    </div>

                    {/* Risk Tolerance */}
                    <div className="mb-6">
                        <label className="block text-lg font-semibold mb-2 text-orange-400">
                            Risk Tolerance
                        </label>
                        <input
                            type="range"
                            min="1"
                            max="10"
                            value={riskTolerance}
                            onChange={(e) => setRiskTolerance(e.target.value)}
                            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer transition-all hover:scale-105"
                        />
                        <div className="flex justify-between text-sm mt-1">
                            <span>Low Risk</span>
                            <span className="text-orange-400 font-bold">Value: {riskTolerance}</span>
                            <span>High Risk</span>
                        </div>
                    </div>

                    {/* Investment Style */}
                    <div className="mb-6">
                        <label className="block text-lg font-semibold mb-2 text-orange-400">
                            Investment Style
                        </label>
                        <select
                            value={investmentStyle}
                            onChange={(e) => setInvestmentStyle(e.target.value)}
                            className="w-full p-3 rounded-lg border border-gray-700 bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-orange-500 hover:scale-105 transition"
                        >
                            <option value="short-term">Short Term</option>
                            <option value="medium-term">Medium Term</option>
                            <option value="long-term">Long Term</option>
                        </select>
                    </div>

                    {/* Income Range (Adjusted for INR) */}
                    <div className="mb-6">
                        <label className="block text-lg font-semibold mb-2 text-orange-400">
                            Income Range (INR)
                        </label>
                        <select
                            value={incomeRange}
                            onChange={(e) => setIncomeRange(e.target.value)}
                            className="w-full p-3 rounded-lg border border-gray-700 bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-orange-500 hover:scale-105 transition"
                        >
                            <option value="Less than 2 LPA">Less than ₹2 LPA</option>
                            <option value="2-5 LPA">₹2 - ₹5 LPA</option>
                            <option value="5-10 LPA">₹5 - ₹10 LPA</option>
                            <option value="10-20 LPA">₹10 - ₹20 LPA</option>
                            <option value="More than 20 LPA">More than ₹20 LPA</option>
                        </select>
                    </div>

                    {/* Investment Goal */}
                    <div className="mb-6">
                        <label className="block text-lg font-semibold mb-2 text-orange-400">
                            Investment Goal
                        </label>
                        <select
                            value={investmentGoal}
                            onChange={(e) => setInvestmentGoal(e.target.value)}
                            className="w-full p-3 rounded-lg border border-gray-700 bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-orange-500 hover:scale-105 transition"
                        >
                            <option value="financial-growth">Financial Growth</option>
                            <option value="education">Education</option>
                            <option value="retirement">Retirement</option>
                            <option value="real-estate">Real Estate</option>
                        </select>
                    </div>

                    {/* Investment Experience */}
                    <div className="mb-6">
                        <label className="block text-lg font-semibold mb-2 text-orange-400">
                            Investment Experience
                        </label>
                        <select
                            value={investmentExperience}
                            onChange={(e) => setInvestmentExperience(e.target.value)}
                            className="w-full p-3 rounded-lg border border-gray-700 bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-orange-500 hover:scale-105 transition"
                        >
                            <option value="beginner">Beginner</option>
                            <option value="intermediate">Intermediate</option>
                            <option value="advanced">Advanced</option>
                        </select>
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        className="w-full bg-orange-500 hover:bg-orange-600 font-bold p-3 text-black rounded-lg font-semibold transition duration-300 shadow-md transform hover:scale-110"
                    >
                        Start Your Investment Journey 💸
                    </button>
                </form>
            </div>
        </div>
    );
};

export default UserInfo;
