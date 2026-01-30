import React, { useState } from 'react';

const characterTypes = ['Adventurer', 'Hunter', 'Warden']; // Example character types

function ChangeCharacterType({ playerId, onChange }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = async (type) => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`/api/players/${playerId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ character_type: type }),
      });

      if (response.ok) {
        onChange(type); // Pass the selected type to the parent component
      } else {
        setError("Failed to update character type");
      }
    } catch (error) {
      setError(`Error updating character type: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-700 p-6 rounded-lg shadow-lg">
      <h3 className="text-2xl font-bold text-yellow-400 mb-4">Select New Character Type:</h3>
      <div className="flex flex-wrap justify-center gap-4">
        {characterTypes.map((type) => (
          <button
            key={type}
            onClick={() => handleChange(type)}
            className={`bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-md transition duration-300 ${loading ? 'cursor-not-allowed opacity-50' : ''}`}
            disabled={loading}
          >
            {type}
          </button>
        ))}
      </div>
      {error && <p className="mt-4 text-red-400">{error}</p>}
    </div>
  );
}

export default ChangeCharacterType;
