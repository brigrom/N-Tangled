# N-Tangled
Build a word game to entertain the American Heritage faculty and students

## N-Gram portion
**Task 1:** Identify word colocations using Google Ngram or local datasets.

**Responsibilities:** 
* Write scripts to pull and filter Ngram data.
* Identify high-frequency bigrams
* * Suffix (e.g., "silver" -> "lining," "spoons," "bullet", "mine")
* * Prefix (e.g., "oil" -> "baby", "olive", "motor", "avocado")
* Create a JSON where a single word anchors one or more sets of four distinct words.
* * {"prefix": {"silver":[["lining," "spoons," "bullet", "mine"], [...]], "hot": {...}},
* *  "suffix": {"oil":[["baby," "olive," "motor", "avocado"], [...]], "hot": {...}} }

**Deliverable:** 
A JSON file of words sharing a common bigram prefix and a separate dictionary of words sharing a common bigram suffix.

**Hints:**
https://storage.googleapis.com/books/ngrams/books/datasetsv3.html
https://datamuse.com/

## WordNet portion
**Task 2:** Identify polysemous words (words with many meanings or "synsets").

**Responsibilities:** 
* Find words with high "sense counts" (e.g., "crane" as a bird vs. "crane" as machinery).
* Filter for nouns and verbs to ensure the words are interchangeable in a grid, in other words match the part of speech.
* Map synonyms to help find category members.

**Deliverable:** A JSON file of distinct semantic paths for a given ambiguous term.

**Hints:**
Use WordNet

## Create four word sets
**Task 3:** The "Connectors." They build the actual sets of four.

**Responsibilities:** 
* Consume data from Tasks 1 and 2 to create "Valid Sets".
* Ensure each set has a "Category Name" (e.g., "Parts of a Shoe" or "___ Cake").
* * While manual effort is tempting, generate code to automatically do this.
* Create a logic check to ensure that within a single set of four, the connection is robust.
* * You can have a human in the loop here

**Deliverable:** A Category class that stores a label and at least one set of four string items.

## Distraction Logic
**Task 4:** Find words that could belong to two categories in order to troll our users.

**Responsibilities:** 
* Analyze the output of Task 3 and look for "Cross-Pollination."
* If Team 3 has a "Fruit" category and a "Tech Companies" category, this team suggests "Apple" to confuse the player.
* Calculate "Distraction Scores" for a 16-word grid.

**Deliverable:** A script that swaps one word from a category with a semantically ambiguous word from the database.

## Game Engine
**Task 5:** Set up all the game logic.

**Responsibilities:** 
* Handle the selection logic (the "Check" button).
* Track the "lives" (four mistakes and you're out).
* Implement the shuffle logic and ensure the 16 words are randomized across the 4x4 grid.

**Deliverable:** A GameSession class that manages the is_correct() logic and state transitions.

## DevOps and UI
**Task 6:** Manage the GitHub repo and the user's view.

**Responsibilities:** 
* Set up testing.
* Build a simple CLI (Command Line Interface) or a web app so people can actually play.
* Manage the README.md and the requirements.txt.
  
**Deliverable:** The main entry point of the program (main.py) and the visual board layout.

|Sample|Table|For|Game|
| ------ | ----- | ------- | ----- |
|SPOON| BABY | HAIKU | FIREFLY|
| BULLET | SONNET | STAR TREK| OLIVE|
|SPACE 1999|ODE|MOTOR|MINE|
| DOLLAR | RED DWARF | AVOCADO | LIMERICK |
