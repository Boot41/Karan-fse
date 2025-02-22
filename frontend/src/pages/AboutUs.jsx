import { useNavigate } from "react-router-dom";

const AboutUs = () => {
  const navigate = useNavigate();

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-black text-white overflow-hidden p-4 sm:p-6">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-r from-black via-gray-900 to-black opacity-80 animate-gradientMove"></div>

      {/* Header */}
      <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-orange-500 mb-6 sm:mb-8 animate-fade-in tracking-wide text-center">
        About Us
      </h1>

      {/* Card containing paragraph + address + contact */}
      <div className="bg-gray-800 bg-opacity-70 p-5 sm:p-8 rounded-2xl shadow-lg max-w-xs sm:max-w-xl lg:max-w-2xl w-full text-center backdrop-blur-md animate-float">
        <p className="text-base sm:text-lg md:text-xl text-gray-300 mb-4 sm:mb-6 leading-relaxed">
          Welcome to <span className="text-orange-400 font-bold">AI Investment Advisor</span>, 
          where technology meets smart investing. Our platform leverages AI to provide 
          <span className="text-orange-400 font-bold"> data-driven investment insights </span> 
          to help you make informed financial decisions.
        </p>
        <p className="text-sm sm:text-lg md:text-xl mb-3 sm:mb-4">
          <strong>📍 Address:</strong> 19, 4th Main, 23rd Cross Rd, Rajiv Gandhi Nagar, Sector 7, HSR Layout, Bengaluru, Karnataka 560068
        </p>
        <p className="text-sm sm:text-lg md:text-xl">
          <strong>📞 Contact:</strong> 9672618163
        </p>
      </div>

      {/* Back Button */}
      <button
        onClick={() => navigate(-1)}
        className="mt-6 px-6 sm:px-8 py-2 sm:py-3 text-lg sm:text-xl text-white bg-orange-500 hover:bg-orange-600 rounded-2xl shadow-lg transition-all duration-300 transform hover:scale-105"
      >
        ⬅️ Back
      </button>

      {/* Floating Animation & Background Effect */}
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

          @keyframes fade-in {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
          }
          .animate-fade-in {
            animation: fade-in 0.5s ease-in-out;
          }
        `}
      </style>
    </div>
  );
};

export default AboutUs;
