import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Welcome = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!email || password.length < 8) {
            setErrorMessage("Invalid email or password");
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/api/token/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("access_token", data.access);
                localStorage.setItem("refresh_token", data.refresh);
                navigate("/user-info"); // Redirect to User Info page
            } else {
                setErrorMessage(data.error || "Invalid credentials. Please try again.");
            }
        } catch (error) {
            console.error("Login error:", error);
            setErrorMessage("Something went wrong. Please try again later.");
        }
    };

    return (
        <div className="relative flex flex-col items-center justify-center min-h-screen bg-black text-white overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-black via-gray-900 to-black opacity-80 animate-pulse"></div>

            <h1 className="text-orange-500 text-5xl sm:text-6xl font-extrabold mb-8 text-center animate-fadeIn">
                Welcome to <br /> 
                AI-Driven Investment Platform of 
                <span className="text-blue-500"> Think41</span>
            </h1>

            <div className="relative bg-gray-900 p-8 rounded-2xl shadow-lg w-96 backdrop-blur-md bg-opacity-80 transition-all duration-300 hover:shadow-orange-500/50 animate-fadeIn">
                {errorMessage && (
                    <div className="bg-red-500 text-white p-3 mb-4 rounded-md text-center">
                        {errorMessage}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="flex flex-col">
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                        className="mb-4 p-3 rounded-lg border border-gray-700 bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-orange-500 placeholder-gray-400 transition"
                        required
                    />
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password (min 8 characters)"
                        className="mb-4 p-3 rounded-lg border border-gray-700 bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-orange-500 placeholder-gray-400 transition"
                        minLength={8}
                        required
                    />
                    <button 
                        type="submit"
                        className="bg-orange-500 hover:bg-orange-600 text-white p-3 rounded-lg font-semibold transition duration-300 shadow-md transform hover:scale-105">
                        Sign In
                    </button>
                </form>

                <div className="mt-6 flex flex-col items-center space-y-2">
                    <button 
                        type="button" 
                        className="text-orange-400 hover:text-orange-500 transition duration-300 text-lg relative group transform hover:scale-105">
                        Sign Up
                        <span className="absolute left-0 bottom-0 w-0 h-[2px] bg-orange-500 transition-all duration-300 group-hover:w-full"></span>
                    </button>
                    <button 
                        type="button" 
                        className="text-orange-400 hover:text-orange-500 transition duration-300 text-lg relative group transform hover:scale-105">
                        Forgot Password?
                        <span className="absolute left-0 bottom-0 w-0 h-[2px] bg-orange-500 transition-all duration-300 group-hover:w-full"></span>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Welcome;
