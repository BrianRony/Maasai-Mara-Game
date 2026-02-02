import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import config from '../config';

function CompleteSafari({ playerId, onComplete }) {
  const [result, setResult] = useState('');
  const navigate = useNavigate();

  const completeSafari = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/complete-safari`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ player_id: playerId })
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data.message);
        // Show result, no auto-navigation
      } else {
        setResult('Error completing safari: ' + response.statusText);
      }
    } catch (error) {
      console.error('Error completing safari:', error);
      setResult('Error completing safari: ' + error.message);
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg text-center">
      <h2 className="text-2xl font-bold text-yellow-500 mb-4">End of the Road</h2>
      <p className="text-gray-300 mb-4">Your journey comes to a close...</p>

      <button 
        onClick={completeSafari}
        className="bg-yellow-500 hover:bg-yellow-600 text-black font-bold py-2 px-4 rounded-md transition duration-300 transform hover:scale-105"
      >
        Complete Safari
      </button>
      
      {result && (
        <div className="mt-6 p-4 bg-gray-700 rounded-md border border-yellow-600">
          <p className="text-yellow-400 whitespace-pre-wrap font-mono text-sm">{result}</p>
          
          <button 
            onClick={() => navigate('/')}
            className="mt-6 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-full transition duration-300 shadow-lg animate-bounce"
          >
            Start New Adventure ↺
          </button>
        </div>
      )}
    </div>
  );
}

export default CompleteSafari;
