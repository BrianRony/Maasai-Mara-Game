import React from 'react';
import { useNavigate } from 'react-router-dom';

const WelcomePage = () => {
    const navigate = useNavigate();

    const navigateToCharacters = () => {
        navigate('/characterSelect');
    };

    return (
        <div className="flex items-center justify-center h-screen bg-gray-900">
            <div className="text-center p-10 bg-blue-800 border border-blue-500 rounded-lg shadow-lg max-w-lg mx-4 md:mx-auto">
                <h1 className="text-5xl font-bold text-yellow-300 mb-6">Welcome to MAASAI MARA QUEST</h1>
                <p className="text-xl text-yellow-200 mb-4">Embark on an epic adventure in the Maasai Mara!</p>
                <p className="text-lg text-yellow-100 mb-6">Start by exploring our <a href="/characterSelect" className="text-yellow-400 font-bold hover:underline">Character Selection</a> page to choose your hero.</p>
                <button
                    onClick={navigateToCharacters}
                    className="bg-yellow-500 hover:bg-yellow-600 text-black font-bold py-3 px-6 rounded-lg transition duration-300 focus:outline-none"
                    aria-label="Get Started"
                >
                    Get Started
                </button>
                <p className="text-yellow-200 mt-6">Ready to dive into the adventure? Click the button above to get started!</p>
            </div>
        </div>
    );
};

export default WelcomePage;
