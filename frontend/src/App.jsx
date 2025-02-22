import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Welcome from './pages/Welcome';
import UserInfo from './pages/UserInfo';
import HomePage from './pages/HomePage';
import ProfilePage from './pages/ProfilePage';
import AboutUs from './pages/AboutUs';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/" replace />;
  }
  return children;
};

const AuthenticatedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  const userProfile = localStorage.getItem('userProfile');
  
  if (!token) {
    return <Navigate to="/" replace />;
  }
  
  if (!userProfile && window.location.pathname !== '/userinfo') {
    return <Navigate to="/userinfo" replace />;
  }
  
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Route */}
        <Route path="/" element={<Welcome />} />
        
        {/* Protected Route - Only needs authentication */}
        <Route
          path="/userinfo"
          element={
            <PrivateRoute>
              <UserInfo />
            </PrivateRoute>
          }
        />
        
        {/* Protected Routes - Need both authentication and profile completion */}
        <Route
          path="/home"
          element={
            <AuthenticatedRoute>
              <HomePage />
            </AuthenticatedRoute>
          }
        />
        
        <Route
          path="/profile"
          element={
            <AuthenticatedRoute>
              <ProfilePage />
            </AuthenticatedRoute>
          }
        />
        
        <Route
          path="/about"
          element={
            <AuthenticatedRoute>
              <AboutUs />
            </AuthenticatedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
