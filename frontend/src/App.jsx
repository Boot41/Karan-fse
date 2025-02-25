// App.jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Welcome from './components/Welcome';
import UserInfo from './components/UserInfo';
import HomePage from './components/HomePage';
import ProfilePage from './components/Profile';
import AboutUs from './components/AboutUs';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard'; // Import the Dashboard component
import ErrorBoundary from './components/ErrorBoundary';

const PrivateRoute = ({ element }) => {
  const token = localStorage.getItem('jwtToken');
  if (!token) {
    return <Navigate to="/" />;
  }
  return element;
};

const AuthenticatedRoute = ({ element }) => {
  const token = localStorage.getItem('jwtToken');
  const userProfile = localStorage.getItem('userProfile');

  if (!token) {
    return <Navigate to="/" />;
  }

  if (!userProfile && window.location.pathname !== '/userinfo') {
    return <Navigate to="/userinfo" />;
  }

  return element;
};

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('jwtToken'));

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  useEffect(() => {
    const token = localStorage.getItem('jwtToken');
    setIsLoggedIn(!!token);
  }, []);

  return (
    <Router>
      <ErrorBoundary>
        <Routes>
          <Route path="/" element={<Welcome onLogin={handleLogin} />} />
          <Route path="/userinfo" element={<PrivateRoute element={<UserInfo />} />} />
          <Route
            path="/home"
            element={
              <AuthenticatedRoute
                element={
                  <>
                    <Navbar />
                    <HomePage />
                  </>
                }
              />
            }
          />
          <Route
            path="/dashboard" // Add the dashboard route
            element={
              <AuthenticatedRoute
                element={
                  <>
                    <Navbar />
                    <Dashboard />
                  </>
                }
              />
            }
          />
          <Route
            path="/about"
            element={
              <AuthenticatedRoute
                element={
                  <>
                    <Navbar />
                    <AboutUs />
                  </>
                }
              />
            }
          />
          <Route
            path="/profile"
            element={
              <AuthenticatedRoute
                element={
                  <>
                    <Navbar />
                    <ProfilePage />
                  </>
                }
              />
            }
          />
        </Routes>
      </ErrorBoundary>
    </Router>
  );
}

export default App;