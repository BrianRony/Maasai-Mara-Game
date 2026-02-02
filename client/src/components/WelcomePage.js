import React from "react";
import { Link } from "react-router-dom";
import SafariLayout from "./SafariLayout";

function WelcomePage() {
  return (
    <SafariLayout title="Maasai Mara" subtitle="The Ultimate Safari Adventure">
      <div className="text-center space-y-8">
        <p className="text-xl text-gray-300 italic">
          "Step into the wild. Survive the elements. Discover the legend."
        </p>

        <div className="flex flex-col space-y-4 max-w-md mx-auto">
          <Link to="/player">
            <button className="w-full bg-yellow-500 hover:bg-yellow-400 text-black font-bold py-4 px-8 rounded-xl shadow-lg transform transition hover:scale-105 text-lg">
              Start New Game 🦁
            </button>
          </Link>
          
          <Link to="/characterSelect">
             <button className="w-full bg-gray-700 hover:bg-gray-600 text-gray-200 font-semibold py-3 px-8 rounded-xl shadow-md transition">
               View Characters 👥
             </button>
          </Link>

          <Link to="/about">
             <button className="w-full bg-gray-800 hover:bg-gray-700 text-gray-400 font-medium py-3 px-8 rounded-xl border border-gray-700 transition">
               About the Game ℹ️
             </button>
          </Link>
        </div>
      </div>
    </SafariLayout>
  );
}

export default WelcomePage;
