import gzip
import requests
import io
import csv
from collections import Counter
from multiprocessing import Pool

# Only pull in bigrams with these POS patterns
PATTERNS = {('ADJ', 'NOUN'), ('NOUN', 'NOUN')}

MIN_TOTAL_COUNT = 100  # Cutoff for the SUM of all years
OUTPUT_FILE = "aggregated_ngrams.csv"

# Ensure your WordNet-derived set is lowercased
ALLOWABLE_WORDS = {word.lower() for word in ['central', 'snow', 'bank']}

# Go through each allowable word to find which books to read
TARGET_LETTERS = set()
for word in ALLOWABLE_WORDS:
    TARGET_LETTERS.add(word[0:2])
    
print(TARGET_LETTERS)

def process_url(url):
    print(f"Processing: {url}")
    # Key: (w1, w2, t1, t2) -> Value: Total Count
    counts = Counter()
    
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with gzip.open(r.raw, mode='rt', encoding='utf-8') as f:
                for line in f:
                    parts = line.split('\t')
                    if len(parts) < 3: continue
                    
                    ngram = parts[0]
                    match_count = int(parts[2])
                    
                    tokens = ngram.split(' ')
                    if len(tokens) != 2: continue

                    try:
                        w1_raw, t1 = tokens[0].rsplit('_', 1)
                        w2_raw, t2 = tokens[1].rsplit('_', 1)
                        # Normalize to lowercase for WordNet compatibility
                        w1, w2 = w1_raw.lower(), w2_raw.lower()
                    except ValueError:
                        continue

                    if (t1, t2) in PATTERNS:
                        if w1 in ALLOWABLE_WORDS and w2 in ALLOWABLE_WORDS:
                            # Aggregate the count for this bigram across all years
                            counts[(w1, w2, t1, t2)] += match_count
                            
    except Exception as e:
        print(f"Error on {url}: {e}")
    
    return counts

if __name__ == '__main__':
    base_url = "http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-{}.gz"
    urls = [base_url.format(l) for l in TARGET_LETTERS]

    with Pool(processes=4) as pool:
        results_list = pool.map(process_url, urls)

    # Combine counters from all processes
    final_counts = Counter()
    for c in results_list:
        final_counts.update(c)

    # Save to CSV, applying the MIN_TOTAL_COUNT filter
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Word1', 'Word2', 'Tag1', 'Tag2', 'Total_Count'])
        
        for (w1, w2, t1, t2), total in final_counts.items():
            if total >= MIN_TOTAL_COUNT:
                writer.writerow([w1, w2, t1, t2, total])

    print(f"Done! Created {OUTPUT_FILE}")
