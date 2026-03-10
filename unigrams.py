import gzip
import requests
import re
import csv
import pandas as pd
from tqdm import tqdm

# --- Configuration ---
MIN_THRESHOLD = 5000
RAW_OUTPUT = "google_unigrams_raw.csv"
FINAL_RANKED_FILE = "google_unigrams_final.csv"
TARGET_LETTERS = [chr(i) for i in range(ord('a'), ord('z') + 1)]

# Your provided lowercase list (Example: loaded from a file or Synsets)
# ALLOWED_SET = set(line.strip().lower() for line in open('wordnet_list.txt'))
ALLOWED_SET = {"digital", "economy", "strategy", "network", "algorithm"} 

# Regex Patterns
RE_SPECIAL_CASE = re.compile(r'([A-Z][a-z]+[A-Z]|[A-Z]{2,})')
RE_IS_NOISE = re.compile(r'^[\d\W_]+$')

def process_and_flush(url, writer):
    local_data = {}
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"File: {url[-6:]}", leave=False) as pbar:
            with gzip.open(response.raw, mode='rt', encoding='utf-8') as f:
                for line in f:
                    pbar.update(len(line))
                    parts = line.split('\t')
                    if len(parts) < 3: continue
                    
                    token, year, count = parts[0], int(parts[1]), int(parts[2])
                    
                    if '_' in token:
                        word, tag = token.rsplit('_', 1)
                    else:
                        word, tag = token, 'NONE'

                    # Step 1: Filter out pure noise (numbers/symbols)
                    if not RE_IS_NOISE.match(word):
                        if token not in local_data:
                            # [Total_Count, Min_Year, Max_Year, Unique_Years_Set]
                            local_data[token] = [0, year, year, set()]
                        
                        data = local_data[token]
                        data[0] += count
                        if year < data[1]: data[1] = year
                        if year > data[2]: data[2] = year
                        data[3].add(year)

        # Step 2: Flush survivors to CSV
        for token, stats in local_data.items():
            total_count = stats[0]
            if total_count >= MIN_THRESHOLD:
                if '_' in token:
                    word_clean, tag_clean = token.rsplit('_', 1)
                else:
                    word_clean, tag_clean = token, 'NONE'
                
                # Check against your provided lowercase list
                is_in_wordnet = word_clean.lower() in ALLOWED_SET
                
                writer.writerow([
                    word_clean, 
                    tag_clean, 
                    total_count, 
                    len(stats[3]), # Total Years
                    stats[1],      # Start Year
                    stats[2],      # End Year
                    is_in_wordnet
                ])
        
        local_data.clear()
        
    except Exception as e:
        print(f"\nError on {url}: {e}")

if __name__ == "__main__":
    base_url = "http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-1gram-20120701-{}.gz"

    # PART 1: STREAM & EXTRACT
    print(f"--- Extraction Started (Target: {len(TARGET_LETTERS)} files) ---")
    with open(RAW_OUTPUT, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Word', 'POS', 'Total_Count', 'Total_Years', 'First_Year', 'Last_Year', 'Is_Known'])
        for char in TARGET_LETTERS:
            process_and_flush(base_url.format(char), writer)

    # PART 2: FINAL SORT & RANK
    print("\n--- Finalizing: Sorting by Total_Count ---")
    try:
        df = pd.read_csv(RAW_OUTPUT)
        df.sort_values(by='Total_Count', ascending=False, inplace=True)
        df.to_csv(FINAL_RANKED_FILE, index=False)
        print(f"Done! Created {FINAL_RANKED_FILE}")
    except Exception as e:
        print(f"Sorting failed (file might be too large for RAM): {e}")
        print(f"Unsorted data is available at {RAW_OUTPUT}")
