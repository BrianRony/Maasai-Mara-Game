import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';

function NavBar() {
  const navigate = useNavigate();

  function goHome() {
    navigate("/");
  }

  const linkClass = ({ isActive }) =>
    `px-4 py-2 rounded-lg font-medium transition-all duration-300 transform ${
      isActive 
        ? "bg-yellow-600 text-white shadow-lg scale-105" 
        : "text-gray-300 hover:text-yellow-400 hover:bg-gray-800"
    }`;

  return (
    <nav className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50 backdrop-blur-md bg-opacity-90">
      <div className="container mx-auto flex items-center justify-between px-6 py-4">
        
        {/* Logo / Brand */}
        <div 
          onClick={goHome} 
          className="flex items-center space-x-2 cursor-pointer group"
        >
          <span className="text-3xl filter drop-shadow-lg group-hover:scale-110 transition-transform duration-300">🦁</span>
          <span className="text-2xl font-bold tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-yellow-600 group-hover:from-yellow-300 group-hover:to-yellow-500">
            MAASAI MARA
          </span>
        </div>

        {/* Navigation Links */}
        <ul className="flex space-x-2 md:space-x-6">
          <li>
            <NavLink to="/characterSelect" className={linkClass}>
              Classes
            </NavLink>
          </li>
          <li>
            <NavLink to="/leaderboard" className={linkClass}>
              Leaderboard
            </NavLink>
          </li>
          <li>
            <NavLink to="/about" className={linkClass}>
              About
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default NavBar;
