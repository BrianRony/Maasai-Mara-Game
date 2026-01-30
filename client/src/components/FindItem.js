import React, { useState } from 'react';

function FindItem({ playerId, onComplete }) {
  const [result, setResult] = useState('');

  const findItem = async () => {
    try {
      const response = await fetch('/api/find-item', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ player_id: playerId })
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data.message);
        
        // Progression
        setTimeout(() => {
          if (onComplete) onComplete(data.updated_stats || {});
        }, 2000);
      } else {
        setResult('Error finding item: ' + response.statusText);
      }
    } catch (error) {
      console.error('Error finding item:', error);
      setResult('Error finding item: ' + error.message);
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg text-center">
      <h2 className="text-2xl font-bold text-yellow-500 mb-4">Scavenge</h2>
      <p className="text-gray-300 mb-4">You search the surroundings...</p>

      <button 
        onClick={findItem}
        className="bg-yellow-500 hover:bg-yellow-600 text-black font-bold py-2 px-4 rounded-md transition duration-300"
      >
        Find Item
      </button>
      
      {result && (
        <div className="mt-4 p-4 bg-gray-700 rounded-md">
          <p className="text-yellow-400">{result}</p>
        </div>
      )}
    </div>
  );
}

export default FindItem;
