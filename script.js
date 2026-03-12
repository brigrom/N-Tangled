/**
 * N-Tangled Frontend Logic - Static Version (No Python needed!)
 */

// 1. DATA FROM APP.PY (Moved here)
const puzzleData = [
    {"label": "Silver ____", "words": ["Lining", "Spoons", "Bullet", "Mine"]},
    {"label": "Types of Oil", "words": ["Baby", "Olive", "Motor", "Avocado"]},
    {"label": "Dog Breeds", "words": ["Pug", "Boxer", "Lab", "Poodle"]},
    {"label": "Furniture", "words": ["Chair", "Table", "Bed", "Sofa"]}
];

let gameState = {
    words: [],           // Words currently on the grid
    selected: [],        // Currently clicked tiles (max 4)
    solvedCategories: [], // Objects {label: "Name"}
    lives: 4,
    gameOver: false
};

// DOM Elements
const gridElement = document.getElementById('game-grid');
const livesElement = document.getElementById('lives-count');
const messageElement = document.getElementById('game-message');

/**
 * 2. INITIALIZE GAME
 * Replaces the old Python fetch with local shuffle logic
 */
function initGame() {
    let allWords = [];
    puzzleData.forEach(cat => allWords.push(...cat.words));
    
    // Shuffle the words
    allWords.sort(() => Math.random() - 0.5);

    gameState.words = allWords.map(word => ({
        text: word,
        selected: false
    }));
    
    gameState.lives = 4;
    gameState.solvedCategories = [];
    gameState.selected = [];
    gameState.gameOver = false;
    
    renderGrid();
}

/**
 * 3. RENDER THE UI
 */
function renderGrid() {
    if (!gridElement) return;
    gridElement.innerHTML = '';

    // A. Draw Solved Banners
    gameState.solvedCategories.forEach(category => {
        const banner = document.createElement('div');
        banner.className = 'solved-category-banner';
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
 * 4. SELECTION LOGIC
 */
function toggleTile(wordObj) {
    if (gameState.gameOver) return;

    const index = gameState.selected.indexOf(wordObj);
    if (index > -1) {
        gameState.selected.splice(index, 1);
    } else if (gameState.selected.length < 4) {
        gameState.selected.push(wordObj);
    }
    renderGrid();
}

/**
 * 5. SUBMIT LOGIC (Now Local JS)
 * This replaces the "async function submitGuess()" that used fetch
 */
function submitGuess() {
    if (gameState.gameOver) return;
    
    if (gameState.selected.length !== 4) {
        showMessage("Select 4 words!");
        return;
    }

    const selectedTexts = gameState.selected.map(w => w.text);
    let foundMatch = null;

    // Check if selection matches any category
    for (let cat of puzzleData) {
        const matches = selectedTexts.filter(word => cat.words.includes(word));
        if (matches.length === 4) {
            foundMatch = cat;
            break;
        }
    }

    if (foundMatch) {
        // Correct!
        gameState.words = gameState.words.filter(w => !selectedTexts.includes(w.text));
        gameState.solvedCategories.push({ label: foundMatch.label });
        gameState.selected = [];
        showMessage("Correct!");
        
        if (gameState.solvedCategories.length === 4) {
            gameState.gameOver = true;
            showMessage("Perfect! You solved it!");
        }
    } else {
        // Incorrect - check for "One Away"
        gameState.lives -= 1;
        
        let isOneAway = false;
        for (let cat of puzzleData) {
            const matches = selectedTexts.filter(word => cat.words.includes(word));
            if (matches.length === 3) {
                isOneAway = true;
                break;
            }
        }

        showMessage(isOneAway ? "One away!" : "Try again.");
        gameState.selected = []; // Optional: Clear selection on wrong answer
        
        if (gameState.lives <= 0) {
            gameState.gameOver = true;
            showMessage("Game Over!");
        }
    }

    renderGrid();
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
    if (gameState.gameOver) return;
    gameState.words.sort(() => Math.random() - 0.5);
    renderGrid();
}

function deselectAll() {
    if (gameState.gameOver) return;
    gameState.selected = [];
    renderGrid();
}

// Start the game
initGame();
