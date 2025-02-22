import { useNavigate } from "react-router-dom";
import { useState } from "react";

const HomePage = () => {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    if (query.trim()) {
      navigate(`/search?query=${encodeURIComponent(query)}`);
    }
  };

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-black text-white overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-r from-black via-gray-900 to-black opacity-80 animate-gradientMove"></div>

      {/* Navbar */}
      <nav className="absolute top-0 left-0 w-full flex flex-wrap justify-between items-center p-4 bg-gray-900 bg-opacity-80 shadow-lg backdrop-blur-md">
        <div className="text-xl sm:text-2xl font-extrabold text-orange-400 tracking-wide">
          AI Investment Advisor
        </div>
        <div className="flex space-x-3 sm:space-x-4 mt-2 sm:mt-0">
          <button 
            onClick={() => navigate("/profile")}  
            className="px-4 sm:px-5 py-2 text-white bg-orange-500 hover:bg-orange-600 rounded-xl shadow-lg transition-all duration-300 transform hover:scale-105">
            Profile
          </button>
          <button 
            onClick={() => navigate("/about")}  
            className="px-4 sm:px-5 py-2 text-white bg-orange-500 hover:bg-orange-600 rounded-xl shadow-lg transition-all duration-300 transform hover:scale-105">
            About Us
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <h1 className="text-4xl sm:text-5xl md:text-7xl font-extrabold mb-6 mt-20 sm:mt-16 animate-fade-in tracking-wide text-center">
        Welcome to <span className="text-orange-500">AI Investment Advisor</span>
      </h1>
      <p className="text-base sm:text-lg md:text-xl text-gray-300 mb-6 sm:mb-8 text-center max-w-xs sm:max-w-md md:max-w-2xl animate-slide-up">
        Get smart investment insights powered by AI. Personalize your portfolio and make informed financial decisions.
      </p>

      {/* Search Box - Responsive */}
      <div className="relative w-11/12 sm:w-full max-w-lg animate-float">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full p-3 sm:p-4 pl-10 sm:pl-12 pr-14 sm:pr-16 text-white bg-gray-900 bg-opacity-60 border-2 border-orange-500 rounded-xl shadow-xl focus:outline-none focus:ring-4 focus:ring-orange-500 hover:border-orange-400 transition-all duration-300 backdrop-blur-md placeholder-gray-400 text-sm sm:text-base"
          placeholder="💡 Ask AI: Should I invest in Tesla?"
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        />
        <button
          onClick={handleSearch}
          className="absolute right-3 sm:right-4 top-1/2 transform -translate-y-1/2 bg-orange-500 hover:bg-orange-600 text-white px-2 sm:px-3 py-1 sm:py-2 rounded-lg shadow-lg transition-all duration-300 transform hover:scale-110"
        >
          🔍
        </button>
      </div>

      {/* Floating Animation Effect */}
      <style>
        {`
          @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-5px); }
            100% { transform: translateY(0px); }
          }
          .animate-float {
            animation: float 3s ease-in-out infinite;
          }

          @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
          }
          .animate-gradientMove {
            background-size: 200% 200%;
            animation: gradientMove 8s ease infinite;
          }
        `}
      </style>
    </div>
  );
};

export default HomePage;
