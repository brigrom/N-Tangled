/**
 * N-Tangled Frontend Logic
 * Connected to Python GameSession
 */

let gameState = {
    words: [],          // Words currently on the grid
    selected: [],       // Currently clicked tiles (max 4)
    solvedCategories: [], // Names of categories already found
    lives: 4
};

// DOM Elements
const gridElement = document.getElementById('game-grid');
const livesElement = document.getElementById('lives-count');
const messageElement = document.getElementById('game-message');

/**
 * 1. INITIALIZE GAME
 * Asks the Python server for the starting 16 words.
 */
async function initGame() {
    try {
        const response = await fetch('/get_game');
        const data = await response.json();
        
        // data.grid comes from your Python GameSession._shuffle_logic()
        // We map strings to objects so we can track selection state
        gameState.words = data.grid.map(word => ({
            text: word,
            selected: false
        }));
        
        gameState.lives = data.lives;
        renderGrid();
    } catch (error) {
        console.error("Error connecting to Python backend:", error);
        messageElement.innerText = "Server connection failed.";
    }
}

/**
 * 2. RENDER THE UI
 * Clears the grid and redraws banners + tiles.
 */
function renderGrid() {
    if (!gridElement) return;
    gridElement.innerHTML = '';

    // A. Draw Solved Banners (Full width)
    gameState.solvedCategories.forEach(category => {
        const banner = document.createElement('div');
        banner.className = 'solved-category-banner';
        // We set the color in the CSS or dynamically here
        banner.innerText = category.label;
        banner.style.backgroundColor = getCategoryColor(category.label);
        gridElement.appendChild(banner);
    });

    // B. Draw Active Tiles
    gameState.words.forEach(wordObj => {
        const tile = document.createElement('div');
        tile.className = 'tile';
        if (gameState.selected.includes(wordObj)) {
            tile.classList.add('selected');
        }
        tile.innerText = wordObj.text;
        tile.onclick = () => toggleTile(wordObj);
        gridElement.appendChild(tile);
    });

    // C. Update Lives
    livesElement.innerText = `Mistakes remaining: ${"● ".repeat(gameState.lives)}`;
}

/**
 * 3. SELECTION LOGIC
 */
function toggleTile(wordObj) {
    const index = gameState.selected.indexOf(wordObj);
    if (index > -1) {
        gameState.selected.splice(index, 1);
    } else if (gameState.selected.length < 4) {
        gameState.selected.push(wordObj);
    }
    renderGrid();
}

/**
 * 4. SUBMIT TO PYTHON ENGINE
 * Sends the 4 selected words to Python for validation.
 */
async function submitGuess() {
    if (gameState.selected.length !== 4) {
        showMessage("Select 4 words!");
        return;
    }

    const selectedTexts = gameState.selected.map(w => w.text);

    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selected: selectedTexts })
        });

        const result = await response.json(); // The Output from your Task 6 logic

        if (result.status === "correct") {
            // Remove solved words from the JS grid
            gameState.words = gameState.words.filter(w => !selectedTexts.includes(w.text));
            // Add the category label to solved list
            gameState.solvedCategories.push({ label: result.category });
            gameState.selected = [];
            showMessage("Correct!");
        } else {
            gameState.lives = result.remaining_lives;
            showMessage(result.message); // Displays "One away!" or "Try again."
        }

        renderGrid();

        if (gameState.lives <= 0) {
            showMessage("Game Over!");
        }
    } catch (error) {
        console.error("Submit error:", error);
    }
}

/**
 * UTILITIES
 */
function showMessage(msg) {
    messageElement.innerText = msg;
    messageElement.style.opacity = "1";
    setTimeout(() => { messageElement.style.opacity = "0.8"; }, 2000);
}

function getCategoryColor(label) {
    const colors = {
        "Silver ____": "#f9df6d",
        "Types of Oil": "#a0c35a",
        "Dog Breeds": "#b0c4ef",
        "Furniture": "#ba81c5"
    };
    return colors[label] || "#ccc";
}

function shuffleBoard() {
    gameState.words.sort(() => Math.random() - 0.5);
    renderGrid();
}

function deselectAll() {
    gameState.selected = [];
    renderGrid();
}

// Kick off the game
initGame();