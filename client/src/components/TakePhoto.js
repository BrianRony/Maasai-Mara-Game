import React, { useState } from 'react';

const TakePhoto = ({ playerId, onComplete }) => {
  const [result, setResult] = useState('');

  const takePhoto = async () => {
    try {
      const response = await fetch('/api/take-photo', {
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
        }, 6000);
      } else {
        setResult('Error taking photo: ' + response.statusText);
      }
    } catch (error) {
      console.error('Error taking photo:', error);
      setResult(`Error taking photo: ${error.message}`);
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg text-center">
      <h2 className="text-2xl font-bold text-yellow-500 mb-4">Capture the Moment</h2>
      <p className="text-gray-300 mb-4">You spot something interesting...</p>

      <button
        onClick={takePhoto}
        className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-md transition duration-300"
      >
        Take Photo
      </button>
      {result && (
        <div className="mt-4 p-4 bg-gray-700 rounded-md">
          <p className="text-yellow-400">{result}</p>
        </div>
      )}
    </div>
  );
};

export default TakePhoto;
