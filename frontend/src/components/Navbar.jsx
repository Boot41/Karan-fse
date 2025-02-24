// Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-blue-600 p-4 text-white">
      <ul className="flex space-x-6">
        <li>
          <Link to="/home" className="hover:text-blue-200">
            Home
          </Link>
        </li>
        <li>
          <Link to="/profile" className="hover:text-blue-200">
            Profile
          </Link>
        </li>
        <li>
          <Link to="/about" className="hover:text-blue-200">
            About Us
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;