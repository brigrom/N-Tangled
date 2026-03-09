import itertools
import math
import json
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class HeritageDeepDistraction:
    def __init__(self, synset_data, vector_model):
        """
        synset_data: Luke/Justin's list of dictionaries.
        vector_model: A dict of {WORD: [v1, v2, ...]} from Task 1/2.
        """
        self.data = synset_data
        # Convert all vectors to numpy arrays for high-speed math
        self.vector_model = {k.upper(): np.array(v).reshape(1, -1) for k, v in vector_model.items()}
        self.word_stats = {}

    def _get_category_centroid(self, word_list):
        """Calculates the 'Average Meaning' (prototype) of a whole category."""
        vecs = [self.vector_model[w.upper()] for w in word_list if w.upper() in self.vector_model]
        if not vecs:
            return None
        return np.mean(vecs, axis=0)

    def calculate_distraction_index(self):
        """
        Calculates distraction scores based on:
        1. CROSS-POLLINATION: Similarity to other category vibes.
        2. LITERAL OVERLAP: Being in multiple groups.
        3. LEMMA TRAPS: Plural/Singular confusion.
        """
        # Step 1: Map out all category 'centroids'
        category_vibes = {}
        for group in self.data:
            centroid = self._get_category_centroid(group["group_words"])
            if centroid is not None:
                category_vibes[group["synset_id"]] = centroid

        # Step 2: Analyze every word in the system
        all_unique_words = set()
        for group in self.data:
            all_unique_words.update([w.upper() for w in group["group_words"]])

        for word in all_unique_words:
            if word not in self.vector_model:
                continue
            
            word_vec = self.vector_model[word]
            base_score = 0.0
            reasons = []

            # --- CRITERIA A: SEMANTIC SHADOWING ---
            # Does this word's meaning 'bleed' into other categories?
            
            for syn_id, vibe_vec in category_vibes.items():
                # Skip if the word actually belongs to this category
                if any(word == w.upper() for g in self.data if g["synset_id"] == syn_id for w in g["group_words"]):
                    continue
                
                sim = cosine_similarity(word_vec, vibe_vec)[0][0]
                if sim > 0.65: # High accuracy threshold
                    bonus = sim * 18
                    base_score += bonus
                    reasons.append(f"Shadows '{syn_id}' category (+{round(bonus, 1)})")

            # --- CRITERIA B: LITERAL OVERLAP ---
            
            occurrences = sum(1 for g in self.data if any(word == w.upper() for w in g["group_words"]))
            if occurrences > 1:
                base_score += (occurrences * 20)
                reasons.append(f"In {occurrences} different lists (+{occurrences * 20})")

            # --- CRITERIA C: PLURAL/SINGULAR TRAPS ---
            if word.endswith('S') and word[:-1] in all_unique_words:
                base_score += 12
                reasons.append("Plural trap (Singular exists)")
            elif f"{word}S" in all_unique_words:
                base_score += 12
                reasons.append("Singular trap (Plural exists)")

            self.word_stats[word] = {
                "distraction_score": round(base_score, 2),
                "reasons": reasons
            }

    def export_rankings(self, filename="word_difficulty.json"):
        """Saves to Desktop to avoid 'Read-only file system' errors."""
        # Finds your Mac's Desktop path automatically
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        final_path = os.path.join(desktop_path, filename)
        
        ranked_list = sorted(self.word_stats.items(), key=lambda x: x[1]['distraction_score'], reverse=True)
        export_data = {item[0]: item[1] for item in ranked_list}
        
        try:
            with open(final_path, 'w') as f:
                json.dump(export_data, f, indent=4)
            print(f"\n[SUCCESS] File saved to: {final_path}")
            
            # --- LEADERBOARD PRINT ---
            print("\n" + "="*50)
            print(f"{'TOP 5 MOST DISTRACTING WORDS':^50}")
            print("="*50)
            for i, (word, stats) in enumerate(ranked_list[:5], 1):
                print(f"{i}. {word:<12} Score: {stats['distraction_score']:<6}")
                for r in stats['reasons']:
                    print(f"   - {r}")
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"ERROR saving file: {e}")

# --- EXECUTION ---
if __name__ == "__main__":
    # 1. INPUT: Luke/Justin's Data Format
    luke_justin_data = [
        {"synset_id": "presidents", "group_words": ["BUSH", "GRANT", "LINCOLN", "TRUMP"]},
        {"synset_id": "cars", "group_words": ["FORD", "DODGE", "CHEVY", "TESLA"]},
        {"synset_id": "silver_items", "group_words": ["LINING", "SPOON", "BULLET", "MINE"]}
    ]

    # 2. INPUT: Task 1/2 Vector Model (Mocked for testing)
    mock_vecs = {
        "LINCOLN": [0.8, 0.8, 0.1], # Cross between Politics and Cars
        "BUSH":    [0.1, 0.9, 0.0], # Pure Politics
        "FORD":    [0.9, 0.1, 0.0], # Pure Car
        "SPOON":   [0.0, 0.0, 0.9],
        "SPOONS":  [0.0, 0.0, 0.9],
        "MINE":    [0.5, 0.0, 0.5], # Cross between Self and Explosives
        "BULLET":  [0.2, 0.0, 0.7]
    }

    # 3. RUN ENGINE
    engine = HeritageDeepDistraction(luke_justin_data, mock_vecs)
    engine.calculate_distraction_index()
    engine.export_rankings()