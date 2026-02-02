import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import SafariLayout from './SafariLayout';
import PlayerStatus from './PlayerStatus';

// Action Components
import StartSafari from './StartSafari';
import ObserveWildlife from './ObserveWildlife';
import InteractWithLocals from './InteractWithLocals';
import HandleWeatherChange from './HandleWeatherChange';
import TakePhoto from './TakePhoto';
import FindItem from './FindItem';
import UseItem from './UseItem';
import CompleteSafari from './CompleteSafari';

import config from '../config';

function Game() {
  const { playerId } = useParams();
  const [step, setStep] = useState(0);
  const [playerStats, setPlayerStats] = useState({});

  useEffect(() => {
    fetchPlayerStats();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playerId]);

  const fetchPlayerStats = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/players/${playerId}`);
      const data = await response.json();
      setPlayerStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const nextStep = (newStats) => {
    if (newStats) {
        setPlayerStats(prev => ({ ...prev, ...newStats }));
    }
    setStep(prev => prev + 1);
  };

  // The Linear Journey
  const gameSteps = [
    <StartSafari playerId={playerId} onComplete={nextStep} stats={playerStats} />,
    <ObserveWildlife playerId={playerId} onComplete={nextStep} stats={playerStats} />,
    <InteractWithLocals playerId={playerId} onComplete={nextStep} stats={playerStats} />,
    <HandleWeatherChange playerId={playerId} onComplete={nextStep} stats={playerStats} />,
    <TakePhoto playerId={playerId} onComplete={nextStep} stats={playerStats} />,
    <FindItem playerId={playerId} onComplete={nextStep} stats={playerStats} />,
    <UseItem playerId={playerId} onComplete={nextStep} stats={playerStats} />,
    <CompleteSafari playerId={playerId} onComplete={nextStep} stats={playerStats} />
  ];

  // Title logic for the Header
  const titles = [
    { title: "Karibu!", subtitle: "Begin your adventure" },
    { title: "The Wild", subtitle: "Observe the animals" },
    { title: "Culture", subtitle: "Meet the people" },
    { title: "Elements", subtitle: "Weather the storm" },
    { title: "Capture", subtitle: "Take a photo" },
    { title: "Scavenge", subtitle: "Find items" },
    { title: "Survival", subtitle: "Use your gear" },
    { title: "Legacy", subtitle: "End of the road" }
  ];

  const isGameOver = playerStats?.health <= 0 && step > 0;
  const currentInfo = titles[step] || { title: "Maasai Mara", subtitle: "" };

  return (
    <SafariLayout title={isGameOver ? "GAME OVER" : currentInfo.title} subtitle={isGameOver ? "The Wild Has Claimed You" : currentInfo.subtitle}>
      {/* Game Content */}
      <div className="mb-8 min-h-[300px] flex flex-col justify-center">
        {isGameOver ? (
          <div className="text-center animate-pulse">
            <div className="text-6xl mb-4">💀</div>
            <h2 className="text-3xl text-red-600 font-bold mb-4">YOUR JOURNEY ENDS HERE</h2>
            <p className="text-gray-400 mb-8">You have succumbed to the dangers of the Mara.</p>
            <button 
              onClick={() => window.location.href = '/'}
              className="bg-red-700 hover:bg-red-600 text-white font-bold py-3 px-8 rounded-full shadow-lg"
            >
              Try Again
            </button>
          </div>
        ) : (
          step < gameSteps.length ? gameSteps[step] : <div>Safari Completed!</div>
        )}
      </div>

      {/* Persistent Status Bar */}
      <PlayerStatus stats={playerStats} />
    </SafariLayout>
  );
}

export default Game;
