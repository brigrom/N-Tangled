from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# --- Paste your GameSession class here ---
class GameSession:

    def __init__(self, puzzle_data):
        self.categories = puzzle_data # Expected: [{"label": "Name", "words": [...]}, ...]
        self.all_words = []
        for cat in self.categories:
            self.all_words.extend(cat['words'])
        
        self.lives = 4
        self.found_categories = []
        self.grid = self._shuffle_logic()
        self.game_over = False

    def _shuffle_logic(self):
        shuffled = list(self.all_words)
        random.shuffle(shuffled)
        return shuffled
    
    def get_status(self):
        """
        Returns the current state of the game for the UI to render.
        """
        return {
            "grid": self.grid,
            "lives": self.lives,
            "found": self.found_categories,
            "game_over": self.game_over
        }

    def check_selection(self, selected_words):
        """
        Validates the user's 4-word selection.
        Returns a dictionary formatted for Task 6 output.
        """
        if self.game_over:
            return {"status": "error", "message": "Game already over."}

        # 1. Check if selection matches any category
        for cat in self.categories:
            # Check how many selected words belong to this category
            matches = set(selected_words).intersection(set(cat['words']))
            match_count = len(matches)

            if match_count == 4:
                self.found_categories.append(cat)
                # Remove solved words from the active grid
                self.grid = [w for w in self.grid if w not in cat['words']]
                if len(self.found_categories) == 4:
                    self.game_over = True
                return {
                    "status": "correct", 
                    "category": cat['label'], 
                    "remaining_lives": self.lives
                }

        # 2. If no perfect match, check for "Near Miss"
        self.lives -= 1
        if self.lives <= 0: self.game_over = True
        
        # Check if any category had 3/4 words
        is_one_away = any(len(set(selected_words).intersection(set(cat['words']))) == 3 
                          for cat in self.categories)

        if is_one_away:
            return {"status": "incorrect", "message": "One away!", "remaining_lives": self.lives}
        
        return {"status": "incorrect", "message": "Try again.", "remaining_lives": self.lives}
    
    

# Mock puzzle data from Task 4
puzzle_data = [
    {"label": "Silver ____", "words": ["Lining", "Spoons", "Bullet", "Mine"]},
    {"label": "Types of Oil", "words": ["Baby", "Olive", "Motor", "Avocado"]},
    {"label": "Dog Breeds", "words": ["Pug", "Boxer", "Lab", "Poodle"]},
    {"label": "Furniture", "words": ["Chair", "Table", "Bed", "Sofa"]}
]

game = GameSession(puzzle_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_game', methods=['GET'])
def get_game():
    # This sends the shuffled 16 words to the JavaScript
    return jsonify(game.get_status())

@app.route('/submit', methods=['POST'])
def submit():
    selected = request.json.get('selected')
    # This calls the check_selection method we wrote earlier
    result = game.check_selection(selected)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

