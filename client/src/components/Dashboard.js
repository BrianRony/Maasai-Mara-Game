import React from 'react';

const ActionButton = ({ icon, label, onClick, color }) => (
  <button
    onClick={onClick}
    className={`
      flex flex-col items-center justify-center p-4 rounded-xl shadow-lg border-2 border-transparent
      transition-all duration-300 transform hover:scale-105 hover:border-yellow-400
      bg-gray-800 hover:bg-gray-700
      ${color || 'text-gray-200'}
    `}
  >
    <div className="text-4xl mb-2">{icon}</div>
    <span className="font-bold text-sm tracking-wide uppercase">{label}</span>
  </button>
);

const Dashboard = ({ onAction, stats }) => {
  const { health } = stats;

  return (
    <div className="w-full">
      {/* Narrative Context */}
      <div className="bg-black/30 p-4 rounded-lg mb-6 border-l-4 border-yellow-500">
        <p className="text-gray-300 italic text-lg">
          "The African sun beats down. The savannah stretches endlessly before you. 
          Your vehicle hums quietly. What is your next move?"
        </p>
      </div>

      {/* Action Grid */}
      <div className="grid grid-cols-2 gap-4">
        <ActionButton 
          icon="🦁" 
          label="Scout Wildlife" 
          onClick={() => onAction('OBSERVE')} 
          color="text-yellow-400"
        />
        <ActionButton 
          icon="🎒" 
          label="Scavenge" 
          onClick={() => onAction('FIND')} 
          color="text-blue-400"
        />
        <ActionButton 
          icon="🌥️" 
          label="Check Weather" 
          onClick={() => onAction('WEATHER')} 
          color="text-gray-300"
        />
        <ActionButton 
          icon="📸" 
          label="Take Photo" 
          onClick={() => onAction('PHOTO')} 
          color="text-purple-400"
        />
        <ActionButton 
          icon="💊" 
          label="Use Item" 
          onClick={() => onAction('USE')} 
          color="text-green-400"
        />
        <ActionButton 
          icon="🤝" 
          label="Visit Village" 
          onClick={() => onAction('INTERACT')} 
          color="text-orange-400"
        />
      </div>

      {/* Emergency / End Game */}
      <div className="mt-8 pt-6 border-t border-gray-700 flex justify-between items-center">
        {health < 30 && (
          <div className="text-red-500 font-bold animate-pulse">
            ⚠️ HEALTH CRITICAL - HEAL SOON
          </div>
        )}
        <button
          onClick={() => onAction('COMPLETE')}
          className="ml-auto text-xs text-red-400 hover:text-red-300 underline"
        >
          End Expedition
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
