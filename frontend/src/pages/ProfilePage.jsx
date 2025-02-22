import { useEffect, useState } from "react";
import axios from "axios";

const ProfilePage = () => {
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem("access_token"); // JWT token from login
        const res = await axios.get("http://127.0.0.1:8000/api/profile/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUserInfo(res.data[0]); // API returns a list, so we use the first item
      } catch (err) {
        console.error("Error fetching profile", err);
      }
    };

    fetchProfile();
  }, []);

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-black text-white overflow-hidden p-4">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-r from-black via-gray-900 to-black opacity-80 animate-gradientMove"></div>

      {/* Navbar */}
      <nav className="absolute top-0 left-0 w-full flex flex-wrap justify-between items-center p-4 bg-gray-900 bg-opacity-80 shadow-lg backdrop-blur-md">
        <div className="text-xl sm:text-2xl font-extrabold text-orange-400 tracking-wide">
          AI Investment Advisor
        </div>
        <button 
          onClick={() => window.history.back()}  
          className="px-4 sm:px-5 py-2 text-white bg-orange-500 hover:bg-orange-600 rounded-xl shadow-lg transition-all duration-300 transform hover:scale-105">
          ⬅ Back
        </button>
      </nav>

      {/* Profile Card */}
      <div className="relative bg-gray-900 bg-opacity-60 p-6 sm:p-8 rounded-2xl shadow-2xl max-w-xs sm:max-w-lg w-full text-center border border-orange-500 backdrop-blur-md animate-fade-in mt-16 sm:mt-20">
        <h1 className="text-3xl sm:text-4xl font-extrabold text-orange-500 mb-6">Your Profile</h1>

        {userInfo ? (
          <div className="text-sm sm:text-lg space-y-3 sm:space-y-4">
            <p><strong className="text-orange-400">Name:</strong> {userInfo.name}</p>
            <p><strong className="text-orange-400">Email:</strong> {userInfo.email}</p>
            <p><strong className="text-orange-400">Investment Experience:</strong> {userInfo.investment_experience}</p>
            <p><strong className="text-orange-400">Investment Goal:</strong> {userInfo.investment_goal}</p>
            <p><strong className="text-orange-400">Income Range:</strong> {userInfo.income_range}</p>
            <p><strong className="text-orange-400">Risk Tolerance:</strong> {userInfo.risk_tolerance}</p>
          </div>
        ) : (
          <p className="text-sm sm:text-lg text-gray-300">No profile data found. Please fill in your details on the User Info page.</p>
        )}
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

          @keyframes fade-in {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
          }
          .animate-fade-in {
            animation: fade-in 0.5s ease-in-out;
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

export default ProfilePage;
