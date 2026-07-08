import json
import os
import re

CLUES_FILE = 'backend/travelreviews_clues.json'
POSTCARDS_FILE = 'backend/travelreviews_postcards.json'
DAILY_GAMES_FILE = 'backend/travelreviews_daily_games.json'

clues = json.load(open(CLUES_FILE))
postcards = json.load(open(POSTCARDS_FILE))
try:
    puzzles = json.load(open(DAILY_GAMES_FILE))
except Exception:
    puzzles = []

approved_postcards = [p for p in postcards if p.get('status') == 'approved']
existing_puzzle_ids = {pz['puzzle_id'] for pz in puzzles}

clues_dict = {c['id']: c for c in clues}

new_puzzles_added = 0
for item in approved_postcards:
    if item['clue_id'] in existing_puzzle_ids:
        continue
        
    matchingClue = clues_dict.get(item['clue_id'])
    num = str(len(puzzles) + 1).zfill(3)
    
    rawTitle = item['pun_name']
    ansPattern = re.sub(r'[a-zA-Z]', '_', rawTitle)
    
    words = rawTitle.split(' ')
    first_letter_words = []
    for w in words:
        if len(w) > 0:
            first_letter_words.append(w[0] + re.sub(r'[a-zA-Z]', '_', w[1:]))
        else:
            first_letter_words.append('')
    firstLetterPattern = ' '.join(first_letter_words)
    
    puzzle_entry = {
        "puzzle_number": num,
        "puzzle_id": item['clue_id'],
        "boss_id": 'boss_' + item['clue_id'],
        "boss_original_title": item['original_name'],
        "boss_pun_title": item['pun_name'],
        "answer": ansPattern,
        "boss_hint2": firstLetterPattern,
        "reviewer_name": matchingClue['reviewer_name'] if matchingClue else "Anonymous",
        "review_title": matchingClue['review_title'] if matchingClue else "Terrible!",
        "clue1": matchingClue['clue1'] if matchingClue else "",
        "clue2": matchingClue['clue2'] if matchingClue else "",
        "clue3": matchingClue['clue3'] if matchingClue else "",
        "boss_pitch": item['owner_response'],
        "boss_poster_url": item['image_path'],
        "difficulty_tier": 1,
        "status": "approved",
        "puzzles": []
    }
    puzzles.append(puzzle_entry)
    new_puzzles_added += 1
    print(f"Compiled puzzle {num}: {item['pun_name']}")
    
if new_puzzles_added > 0:
    with open(DAILY_GAMES_FILE, 'w', encoding='utf-8') as f:
        json.dump(puzzles, f, indent=2)
    print(f"Saved {new_puzzles_added} new puzzles to {DAILY_GAMES_FILE}")
else:
    print("No new puzzles to compile.")
