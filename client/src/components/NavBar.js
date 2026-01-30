import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import '../index.css';

function NavBar() {
  const navigate = useNavigate();  // Use React Router's useNavigate hook

  function goHome() {
    navigate("/");  // Navigate to home without full page reload
  }

  return (
    <nav className="bg-gray-800 text-white shadow-md py-4">
      <div className="container mx-auto flex items-center justify-between px-4">
        <p className="text-2xl font-bold cursor-pointer" onClick={goHome}>MAASAI MARA QUEST</p>
        <ul className="flex space-x-6">
          <li>
            <NavLink
              to="/characterSelect"
              className={({ isActive }) => 
                isActive ? "bg-gray-700 text-white px-4 py-2 rounded transition duration-300" : 
                "text-white hover:bg-gray-700 px-4 py-2 rounded transition duration-300"
              }
            >
              Characters
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/about"
              className={({ isActive }) => 
                isActive ? "bg-gray-700 text-white px-4 py-2 rounded transition duration-300" : 
                "text-white hover:bg-gray-700 px-4 py-2 rounded transition duration-300"
              }
            >
              About
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default NavBar;
