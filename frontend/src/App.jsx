import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Welcome from './components/Welcome';
import UserInfo from './components/UserInfo';
import HomePage from './components/HomePage';
import ProfilePage from './components/Profile';
import AboutUs from './components/AboutUs';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Route path="/" element={<Welcome />} />;
  }
  return children;
};

const AuthenticatedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  const userProfile = localStorage.getItem('userProfile');
  
  if (!token) {
    return <Route path="/" element={<Welcome />} />;
  }
  
  if (!userProfile && window.location.pathname !== '/userinfo') {
    return <Route path="/userinfo" element={<UserInfo />} />;
  }
  
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Route */}
        <Route path="/" exact element={<Welcome />} />
        
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
          path="/homepage"
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
