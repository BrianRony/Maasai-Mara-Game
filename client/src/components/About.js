
import React from 'react';

function About() {
  return (
    <div className="about-page bg-gray-900 p-8 min-h-screen">
      <div className="max-w-4xl mx-auto bg-gray-800 text-gray-100 p-8 rounded-lg shadow-lg">
        <h1 className="text-5xl font-bold text-center text-yellow-300 mb-6">About Maasai Mara Adventure</h1>
        <p className="text-xl text-gray-300 mb-6">
          Welcome to <span className="font-semibold text-yellow-400">Maasai Mara Adventure</span>, an immersive role-playing game set in the stunning Maasai Mara of Kenya. Choose your path from three unique characters—Adventurer, Hunter, or Warden—each with distinct abilities that influence your journey through perilous quests and diverse landscapes.
        </p>
        <p className="text-xl text-gray-300 mb-8">
          Experience the thrill of exploration, engage in tactical challenges, and immerse yourself in the rich cultural and natural environment of the Maasai Mara. Your choices shape your adventure, whether you’re negotiating with local tribes, combating wildlife threats, or protecting the land from intruders.
        </p>
        
        <h2 className="text-4xl font-semibold text-yellow-300 mb-4">Our Mission</h2>
        <p className="text-xl text-gray-300 mb-6">
          Our mission is to transport you to the heart of the Maasai Mara, providing an experience that is not only visually stunning but also deeply engaging. We strive to blend the beauty of this unique landscape with the excitement of gameplay, ensuring every moment is packed with adventure.
        </p>
        <p className="text-xl text-gray-300">
          Enjoy your journey through the Maasai Mara, and may your adventures be as boundless as the savannahs themselves!
        </p>
      </div>
    </div>
  );
}

export default About;
