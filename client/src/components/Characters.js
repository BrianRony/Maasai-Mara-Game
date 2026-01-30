import React from 'react';
import { useNavigate } from 'react-router-dom';

function Characters() {
  const navigate = useNavigate();

  const characters = [
    {
      name: 'Adventurer',
      description: 'A brave hero ready for any challenge.',
      img: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTINyVzG_kSZ02MgkM8GLLtI7PbU5EJ4MWyOg&s',
      qualities: 'Strength, Courage, Adaptability'
    },
    {
      name: 'Hunter',
      description: 'A skilled tracker and fighter.',
      img: 'https://cdn3.vectorstock.com/i/1000x1000/91/37/hunter-retro-vintage-deer-hunting-t-shirt-design-vector-48369137.jpg',
      qualities: 'Agility, Precision, Stealth'
    },
    {
      name: 'Warden',
      description: 'A guardian with a strong sense of duty.',
      img: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYXWXzWZ9OHwnC1131Twwy1TnsBCb0jEOT5w&s',
      qualities: 'Defense, Strategy, Leadership'
    }
  ];

  return (
    <div className="bg-gray-900 min-h-screen flex flex-col items-center p-6">
      <h1 className="text-5xl text-yellow-400 font-bold mb-12">Choose Your Character</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
        {characters.map((character, index) => (
          <div key={index} className="bg-gray-800 p-8 rounded-lg shadow-lg text-center hover:shadow-xl transition-shadow duration-300">
            <img 
              src={character.img} 
              alt={character.name} 
              className="mb-6 mx-auto w-40 h-40 object-cover rounded-full border-4 border-yellow-400"
              style={{ imageRendering: 'auto' }} // Use auto for better quality
            />
            <h2 className="text-2xl text-white font-bold mb-3">{character.name}</h2>
            <p className="text-gray-300 mb-4">{character.description}</p>
            <p className="text-yellow-400 font-medium">Unique Qualities:</p>
            <p className="text-gray-400">{character.qualities}</p>
          </div>
        ))}
      </div>
      <button 
        className="mt-12 bg-yellow-500 hover:bg-yellow-600 text-black font-bold py-3 px-6 rounded-lg transition duration-300"
        onClick={() => navigate('/player')}
      > 
        Register & Choose Your Character
      </button>
    </div>
  );
}

export default Characters;
