import json

class Category:
def __init__(self, label: str, words: list, source_type: str = "unknown"):
self.label = label.upper().strip()

clean_words = [str(w).strip().upper() for w in words]

if len(set(clean_words)) < 4:
raise ValueError(f"Category '{self.label}' must have 4 unique words. Check for duplicates.")

self.words = clean_words[:4]
self.source_type = source_type

def is_robust(self) -> bool:
valid_length = all(len(w) > 0 for w in self.words)
unique_check = len(set(self.words)) == 4
return valid_length and unique_check

def to_dict(self):
return {
"label": self.label,
"words": self.words,
"metadata": {"source": self.source_type}
}

def __repr__(self):
return f"Category({self.label}: {', '.join(self.words)})"

