# N-Tangled
Build a word game to entertain the American Heritage faculty and students

## N-Gram portion - Mike and Jonah
**Task 1:** Identify word colocations using Google Ngram or local datasets.

**Responsibilities:** 
* Write scripts to pull and filter Ngram data.
* Identify high-frequency bigrams
    * Suffix (e.g., "silver" -> "lining," "spoons," "bullet", "mine")
    * Prefix (e.g., "oil" -> "baby", "olive", "motor", "avocado")
* Create a JSON where a single word anchors one **or more** sets of four **or more distinct words.
    * {"prefix": {"silver":[["lining," "spoons," "bullet", "mine"], [...]], "hot": {...}},
    *  "suffix": {"oil":[["baby," "olive," "motor", "avocado", "crude"], [...]], "hot": {...}} }
        * Order the terms by the frequency of the bigram

**Deliverable:**  
A JSON file of words sharing a common bigram prefix and of words sharing a common bigram suffix.

**Hints:**
https://storage.googleapis.com/books/ngrams/books/datasetsv3.html
https://datamuse.com/

## WordNet portion - Emilee and Gianna
**Task 2:** Identify synonymous words (words with the same meaning or "synset").

**Responsibilities:** 
* Get a list of all words in wordnet (or all synsets and skip next step)
* For each word, get all of its synsets
* Create a dictionary of every synset that has at least four lemmas

**Deliverable:**  
A JSON file composed of a dictionary of synsets, each synset having a list of synonymous words.

**Hints:**  
d = {}   
for syns in wn.synsets(your_word):   
&nbsp;&nbsp;&nbsp;&nbsp;if len(syns.lemma_names()) >= 4:   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;d[syns.name()] = syns.lemma_names()  

## Polysemous words portion - Luke and Jett
**Task 2.5:** Identify polysemous words (words with many meanings or "synsets").

**Responsibilities:** 
* Find words with high "sense counts" (e.g., "crane" as a bird vs. "crane" as machinery).

**Deliverable:**   
A JSON file composed of a dictionary of ambiguous terms, and the synsets belonging to them

## WordNet portion - Patrick and Siyuan
**Task 2.75:** Build lists of categories

**Responsibilities:** 
* Find lists on various topics

**Deliverable:**   
A JSON file composed of a dictionary of topics, and the members belonging to them

## Create four word sets - Jett and Luke
**Task 3:** The "Connectors." They build the actual sets of four.

**Responsibilities:** 
* Consume data from Tasks 1 and 2 to create "Valid Sets".
* Ensure each set has a "Category Name" (e.g., "Words that mean small" or "___ Cake" or "Silver ____").
    * While manual effort is tempting, generate code to automatically do this.
* Maintain frequency order from Task 1

**Deliverable:**  
A Category class that stores a label and at least one set of four string items.

## Distraction Logic - Jordan and Carson
**Task 4:** Find words that could belong to two categories in order to troll our users.

**Responsibilities:** 
* Analyze the output of Task 3 and look for ways to increase the difficulty of the words in a set
* Do this by finding terms in two or more sets and ranking the relatedness of the categories
    * Relatedness
        * Explore word embedding
            * Word2Vec
            * GloVe
* Calculate "Distraction Scores" for a 16-word grid.

**Deliverable:**   
A JSON file of four categories and four words in each category, sorted by easy to hard   
[{"Car Brands":['Ford', 'Dodge', 'Lincoln', 'Ram'], "Presidentsl":['Bush', 'Grant', 'Trump', 'Trump'] ....

## Game Engine - Siyuan and Patrick
**Task 5:** Set up all the game logic.

**Responsibilities:** 
* Handle the selection logic (the "Check" button).
* Track the "lives" (four mistakes and you're out).
* Implement the shuffle logic and ensure the 16 words are randomized across the 4x4 grid.

**Deliverable:**   
A GameSession class that manages the is_correct() logic and state transitions.   
Build a simple CLI (Command Line Interface) for testing

## DevOps and UI - Preston and Finn
**Task 6:** Manage the GitHub repo and the user's view.

**Responsibilities:** 
* Build a web app so people can actually play.
* Manage the README.md and the requirements.txt.
  
**Deliverable:**   
The main entry point of the program (main.py) and the visual board layout.

|Sample|Table|For|Game|
| ------ | ----- | ------- | ----- |
|SPOON| BABY | HAIKU | FIREFLY|
| BULLET | SONNET | STAR TREK| OLIVE|
|SPACE 1999|ODE|MOTOR|MINE|
| DOLLAR | RED DWARF | AVOCADO | LIMERICK |
