import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Welcome from './components/Welcome';
import UserInfo from './components/UserInfo';
import HomePage from './components/HomePage';
import ProfilePage from './components/Profile';
import AboutUs from './components/AboutUs';

// PrivateRoute component ensures the user is logged in before accessing a route
const PrivateRoute = ({ element }) => {
  const token = localStorage.getItem('token');
  if (!token) {
    // If no token, redirect to the Welcome (Login/Signup) page
    return <Navigate to="/" />;
  }
  return element;
};

// AuthenticatedRoute component ensures the user has a profile before proceeding
const AuthenticatedRoute = ({ element }) => {
  const token = localStorage.getItem('token');
  const userProfile = localStorage.getItem('userProfile');
  
  if (!token) {
    // If no token, redirect to the Welcome (Login/Signup) page
    return <Navigate to="/" />;
  }

  // If there's no profile but user is not at /userinfo, redirect to /userinfo
  if (!userProfile && window.location.pathname !== '/userinfo') {
    return <Navigate to="/userinfo" />;
  }
  
  return element;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Route */}
        <Route path="/" element={<Welcome />} />
        
        {/* Protected Route - Requires authentication */}
        <Route
          path="/userinfo"
          element={
            <PrivateRoute element={<UserInfo />} />
          }
        />
        
        {/* Protected Routes - Requires authentication and profile completion */}
        <Route
          path="/homepage"
          element={
            <AuthenticatedRoute element={<HomePage />} />
          }
        />
        
        <Route
          path="/profile"
          element={
            <AuthenticatedRoute element={<ProfilePage />} />
          }
        />
        
        <Route
          path="/about"
          element={
            <AuthenticatedRoute element={<AboutUs />} />
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
