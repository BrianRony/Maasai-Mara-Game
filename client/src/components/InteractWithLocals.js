import React, { useState } from 'react';

function InteractWithLocals({ playerId, onComplete }) {
  const [result, setResult] = useState('');

  const interactWithLocals = async () => {
    try {
      const response = await fetch('/api/interact-with-locals', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ player_id: playerId })
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data.message);
        // Wait 2 seconds so user can read the message, then move to next step
        setTimeout(() => {
          if (onComplete) onComplete(data.updated_stats || {});
        }, 6000);
      } else {
        setResult('Error interacting with locals: ' + response.statusText);
      }
    } catch (error) {
      console.error('Error interacting with locals:', error);
      setResult('Error interacting with locals: ' + error.message);
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg text-center">
      <h2 className="text-2xl font-bold text-yellow-500 mb-4">Meet the Maasai</h2>
      <p className="text-gray-300 mb-4">You encounter a local community. What will you learn?</p>
      
      <button 
        onClick={interactWithLocals}
        className="bg-yellow-500 hover:bg-yellow-600 text-black font-bold py-2 px-4 rounded-md transition duration-300"
      >
        Interact with Locals
      </button>
      
      {result && (
        <div className="mt-4 p-4 bg-gray-700 rounded-md">
          <p className="text-yellow-400">{result}</p>
        </div>
      )}
    </div>
  );
}

export default InteractWithLocals;
