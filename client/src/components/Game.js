import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import StartSafari from './StartSafari';
import ObserveWildlife from './ObserveWildlife';
import InteractWithLocals from './InteractWithLocals';
import HandleWeatherChange from './HandleWeatherChange';
import TakePhoto from './TakePhoto';
import FindItem from './FindItem';
import UseItem from './UseItem';
import CompleteSafari from './CompleteSafari';
import PlayerStatus from './PlayerStatus';
import SafariLayout from './SafariLayout';

function Game() {
  const { playerId } = useParams();
  const [step, setStep] = useState(0);
  const [playerStats, setPlayerStats] = useState({});

  useEffect(() => {
    fetchPlayerStats();
  }, [playerId]);

  const fetchPlayerStats = async () => {
    try {
      const response = await fetch(`/api/players/${playerId}`);
      const data = await response.json();
      setPlayerStats(data);
    } catch (error) {
      console.error('Error fetching player stats:', error);
    }
  };

  const nextStep = (newStats) => {
    // Merge new stats into existing state
    setPlayerStats(prevStats => ({ ...prevStats, ...newStats }));
    // Advance step
    setStep(prevStep => prevStep + 1);
  };

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

  if (step >= gameSteps.length) {
    // Reset to start if we go past the end (though CompleteSafari handles its own exit)
    return <div>Safari Completed!</div>;
  }

  // Titles for the layout based on current step
  const titles = [
    { title: "Karibu!", subtitle: "Begin your adventure" },
    { title: "The Wild", subtitle: "Observe the animals" },
    { title: "Culture", subtitle: "Meet the people" },
    { title: "Elements", subtitle: "Weather the storm" },
    { title: "Capture", subtitle: "Take a photo" },
    { title: "Scavenge", subtitle: "Find items" },
    { title: "Survival", subtitle: "Use your gear" },
    { title: "Journey's End", subtitle: "See your legacy" }
  ];

  const currentInfo = titles[step] || { title: "Safari", subtitle: "" };

  return (
    <SafariLayout title={currentInfo.title} subtitle={currentInfo.subtitle}>
      {/* The Active Game Step */}
      <div className="mb-8">
        {gameSteps[step]}
      </div>

      {/* Floating Status Bar (Always Visible) */}
      <PlayerStatus stats={playerStats} />
    </SafariLayout>
  );
}

export default Game;
