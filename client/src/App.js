import React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import NavBar from './components/NavBar';
import WelcomePage from './components/WelcomePage';

function App() {
  const location = useLocation(); 

  return (
    <>
      <header>
        <NavBar />
      </header>
      <main>
        {location.pathname === '/' && <WelcomePage />}
        <Outlet />  {/* Renders nested child routes */}
      </main>
    </>
  );
}

export default App;