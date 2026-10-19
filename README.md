# 🍬 Sweet Odyssey — Match-3 Puzzle Game

Sweet Odyssey is a full-stack, browser-based Match-3 puzzle game inspired by classic candy-matching mechanics, featuring an original visual identity, interactive level progression, animated gameplay, and persistent player data.

The project was developed to demonstrate modern frontend development, 2D game programming, backend API integration, database management, and automated software testing.

## 🎮 Key Features

- **20 Playable Levels:** Progressively challenging puzzle levels with different objectives.
- **Match-3 Game Engine:** Candy swapping, match detection, cascading combinations, gravity, and scoring.
- **Special Candies:** Line-clearing and color-clearing mechanics.
- **Interactive Level Map:** Unlock new levels, earn stars, and replay completed challenges.
- **Player Progression:** Persistent scores, unlocked levels, and completion records.
- **Power-Ups:** Special gameplay abilities and extra moves.
- **Responsive UI:** Designed for desktop and mobile browsers.
- **Animations and Effects:** Candy interactions, visual transitions, and victory celebrations.
- **Python Backend:** API-based player progress management.
- **Easy Local Setup:** Launch the game using `app.py` or the included Windows startup script.

## 🛠 Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite |
| Game Engine | Phaser 3 |
| Backend | Python, FastAPI |
| Data Validation | Pydantic |
| Database | SQLite (local), optional PostgreSQL support |
| Frontend Testing | Vitest |
| Backend Testing | Pytest |
| End-to-End Testing | Playwright |

## 🏗 Architecture

The application separates interactive gameplay from server-side data persistence.

- **Frontend:** User interface, level selection, animations, and game rendering.
- **Game Logic:** Match detection, moves, scoring, cascades, and level objectives.
- **Backend:** REST API endpoints, player records, game result validation, and progression management.
- **Database:** Persistent player progress and completed level results.

## 🚀 Getting Started

### Requirements

- Python 3.11 or newer
- A modern web browser
- Internet access for the initial dependency installation

### Run on Windows

Extract the ZIP archive and double-click:

`OYUNU_BASLAT.bat`

Alternatively, run the following command from the project folder:

```bash
python app.py
```

The startup script installs the required Python dependencies and opens the game in your browser.

The packaged frontend is ready to use without requiring Node.js or Docker.

## 🧪 Testing

The project includes automated tests for game mechanics, backend functionality, and browser interactions.

Validation performed during development:

- 119 Python tests passed
- 94 TypeScript tests passed
- 7 browser scenarios passed

Test coverage includes match detection, player moves, level completion, progression persistence, and essential UI interactions.

## 🎯 Project Goals

Sweet Odyssey was created as a software engineering portfolio project to demonstrate:

- Full-stack web application development
- Interactive 2D game design
- Game state management and algorithmic problem-solving
- RESTful API architecture
- Persistent data storage
- Responsive user experience
- Automated testing and quality assurance
- Modular and maintainable software architecture

## 📌 Project Status

Playable local project with 20 configured levels, persistent progression, and an integrated Python backend.

## 📄 License

No open-source license has been selected yet.
