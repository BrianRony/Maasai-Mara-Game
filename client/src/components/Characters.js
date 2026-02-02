import React, { useState, useEffect } from 'react';
import SafariLayout from "./SafariLayout";

import config from '../config';

function Characters() {
  const [characters, setCharacters] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${config.API_BASE_URL}/api/characters`)
      .then(r => r.json())
      .then(data => {
        setCharacters(data);
        setLoading(false);
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <SafariLayout title="Classes" subtitle="Choose your path">
      {loading ? (
        <p className="text-gray-400 animate-pulse text-center">Loading classes...</p>
      ) : (
        <div className="grid gap-6 md:grid-cols-1">
          {characters.map(char => (
            <div key={char.id} className="bg-gray-700/50 border border-gray-600 rounded-lg p-6 hover:border-yellow-500 transition-colors">
              <h3 className="text-xl font-bold text-yellow-400 mb-2">{char.character_type}</h3>
              <p className="text-gray-300 text-sm">{char.description}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                <span className="px-2 py-1 bg-gray-800 text-xs text-gray-400 rounded">Starting Item: ???</span>
              </div>
            </div>
          ))}
        </div>
      )}
      
      <div className="mt-8 text-center">
        <a href="/" className="text-yellow-500 hover:text-yellow-400 underline text-sm">
          ← Back to Home
        </a>
      </div>
    </SafariLayout>
  );
}

export default Characters;
