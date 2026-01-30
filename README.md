### Maasai Mara Safari Adventure Game

## Project Overview

The Maasai Mara Safari Adventure Game is a Flask-based backend with a React-based frontend adventure game. Players can choose different character types, explore the Maasai Mara region, engage in various quests, and encounter wildlife. The game allows saving, loading, and resetting progress with randomized events for each session.

## Table of Contents
1. Project Dependencies
2. Installation and Setup
3. Server-Side Explanation
4. Client-Side Explanation
5. Connecting the Server and Client
6. Running the Application
7. Migrations
8. Pivot Points


1. Project Dependencies
# Backend Dependencies (Python):
Flask
Flask-SQLAlchemy
Flask-Migrate
Flask-RESTful
Flask-CORS
SQLAlchemy-serializer
Flask-Cache
Flask-Caching


## Frontend Dependencies (JavaScript):
React
React Router DOM
Axios (if needed for making HTTP requests)
Tailwind CSS (for styling)


Ensure all dependencies are installed:

pipenv install  # For backend
npm install  # For frontend

2. Installation and Setup
## Backend (Flask):
- Clone the repository:

git clone https://github.com/your-repo/maasai-mara-adventure.git
cd maasai-mara-adventure/server

- Create and activate a virtual environment:
pipenv shell

- Install dependencies:
pipenv install

- Database setup:
Initialize the database:
flask db init

Generate migrations:
flask db migrate

Apply migrations:
flask db upgrade


## Frontend (React):
- Navigate to the client folder:
cd ../client

- Install the dependencies:
npm install

-Set up Tailwind CSS (already configured in index.css):
npm install -D tailwindcss
npx tailwindcss init


3. Server-Side Explanation
The backend is built using Flask with Flask-RESTful for creating APIs. The game logic is encapsulated in services like GameService and MaasaiMaraEventsLogic, which manage random events, player interactions, and the overall gameplay.

## Core Resources:
- PlayerResource: Handles player creation, updates, and fetching.
- CharacterResource: Manages available characters.
- MapResource: Manages maps and locations.
- QuestResource: Handles quests and their progression.
- GameResource: Manages game states (save, load, reset).
- SafariEventResource: Manages various game events, including wildlife observations, interactions with locals, and weather changes.


## Key Endpoints:
GET /api/players/<player_id>: Fetch player details.
POST /api/game/<player_id>: Save game state.
POST /api/start-safari: Start a new safari adventure.
POST /api/observe-wildlife: Observe wildlife and update player stats.


4. Client-Side Explanation
The frontend is a React app with React Router for routing and Tailwind CSS for styling. The user interface allows players to choose characters, navigate the map, and interact with the environment through various game events such as observing wildlife and handling weather changes.

## Key Components:
- App.js: Main app component that includes routing and navigation.
- NavBar.js: A simple navigation bar with links to various pages.
- Game.js: Core gameplay component that renders different game events like observing wildlife or interacting with locals.
- CompleteSafari.js: Handles the completion of a safari session.
- ErrorPage.js: Displays custom error messages when something goes wrong.

## Key Routes:
- /characterSelect: Select a character to start the game.
- /about: Information about the game and its mission.
- /game/:playerId: The main gameplay route where the player progresses through various events.


5. Connecting the Server and Client
- CORS Setup: The Flask backend has CORS enabled, allowing the frontend to securely communicate with it.
from flask_cors import CORS
CORS(app)


- API Calls from Frontend: Use fetch or axios to make API calls to the backend. For example:

const response = await fetch(`/api/observe-wildlife/${playerId}`);
const data = await response.json();


- Proxy Setup: To handle API requests during development, add a proxy to your package.json file in the client directory:
"proxy": "http://localhost:5555"


6. Running the Application
# Backend:
Start the Flask server:
flask run

# Frontend:
Start the React app:

npm start

Both the server and client should now be running locally. You can access the frontend on http://localhost:3000 and the backend on http://localhost:5555.

7. Migrations
To handle database changes, Flask-Migrate is used.

- Create new migrations:
flask db migrate

- Apply migrations:
flask db upgrade

- Reset migrations: If you need to reset everything:
flask db downgrade


8. Pivot Points

- Game Logic: Core game logic is handled by the MaasaiMaraEventsLogic class in the backend. Random events, inventory management, and player progression are managed here.
- Random Events: Wildlife encounters, weather changes, and interactions with locals are all randomized, adding an element of unpredictability to each game session.
- Game State Management: Players can save, load, and reset their game states, making the game flexible and allowing progression across sessions.
# Maasai-Mara-Game
