import React from "react";
import App from "./App";
import ErrorPage from './components/ErrorPage';
import Characters from './components/Characters';
import About from './components/About';
import Player from './components/Player';
import Game from './components/Game';
import Leaderboard from './components/Leaderboard';

const routes = [
  {
    path: '/',
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: 'characterSelect',
        element: <Characters />,
      },
      {
        path: 'about',
        element: <About />,
      },
      {
        path: 'player',
        element: <Player />,
      },
      {
        path: 'leaderboard',
        element: <Leaderboard />,
      },
      {
        path: 'game/:playerId',
        element: <Game />,
      }
    ]
  }
];

export default routes;
