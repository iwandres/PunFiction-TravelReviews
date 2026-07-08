import json

# Define the categories mapping
category_mapping = {
    # Ancient Ruins & Archaeological Sites
    "Colosseum": "Ancient Ruins & Archaeological Sites",
    "Pyramids of Giza": "Ancient Ruins & Archaeological Sites",
    "Petra": "Ancient Ruins & Archaeological Sites",
    "Chichen Itza": "Ancient Ruins & Archaeological Sites",
    "Angkor Wat": "Ancient Ruins & Archaeological Sites",
    "Machu Picchu": "Ancient Ruins & Archaeological Sites",
    "Pantheon": "Ancient Ruins & Archaeological Sites",
    "Roman Forum": "Ancient Ruins & Archaeological Sites",
    "Stonehenge": "Ancient Ruins & Archaeological Sites",

    # Natural Wonders & Landscapes
    "Grand Canyon": "Natural Wonders & Landscapes",
    "Great Barrier Reef": "Natural Wonders & Landscapes",
    "Yellowstone National Park": "Natural Wonders & Landscapes",
    "Loch Ness": "Natural Wonders & Landscapes",
    "Black Forest": "Natural Wonders & Landscapes",
    "Matterhorn": "Natural Wonders & Landscapes",
    "Cliffs of Moher": "Natural Wonders & Landscapes",
    "Giant's Causeway": "Natural Wonders & Landscapes",

    # Historic Towers, Monuments & Statues
    "Eiffel Tower": "Historic Towers, Monuments & Statues",
    "Taj Mahal": "Historic Towers, Monuments & Statues",
    "Christ the Redeemer": "Historic Towers, Monuments & Statues",
    "Big Ben": "Historic Towers, Monuments & Statues",
    "Leaning Tower of Pisa": "Historic Towers, Monuments & Statues",
    "Atomium": "Historic Towers, Monuments & Statues",

    # Modern Skyscrapers & Architecture
    "Empire State Building": "Modern Skyscrapers & Architecture",
    "Burj Khalifa": "Modern Skyscrapers & Architecture",
    "Space Needle": "Modern Skyscrapers & Architecture",

    # Bridges, Canals & Historic Engineering
    "Great Wall of China": "Bridges, Canals & Historic Engineering",
    "Golden Gate Bridge": "Bridges, Canals & Historic Engineering",
    "Panama Canal": "Bridges, Canals & Historic Engineering",
    "Tower Bridge": "Bridges, Canals & Historic Engineering",
    "Grand Canal": "Bridges, Canals & Historic Engineering",

    # Castles, Fortresses & Cathedrals
    "Tower of London": "Castles, Fortresses & Cathedrals",
    "Edinburgh Castle": "Castles, Fortresses & Cathedrals",
    "Mont Saint-Michel": "Castles, Fortresses & Cathedrals",
    "Sagrada Fam\u00edlia": "Castles, Fortresses & Cathedrals",
    "St. Peter's Basilica": "Castles, Fortresses & Cathedrals",
    "Notre-Dame Cathedral": "Castles, Fortresses & Cathedrals",

    # Famous Streets, Squares & Towns
    "Times Square": "Famous Streets, Squares & Towns",
    "Spanish Steps": "Famous Streets, Squares & Towns",
    "La Rambla": "Famous Streets, Squares & Towns",
    "Santorini": "Famous Streets, Squares & Towns"
}

with open('backend/travelreviews_daily_games.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

# Bucket the challenges
buckets = {}
for g in games:
    orig = g['boss_original_title']
    cat = category_mapping.get(orig, "Other/Unmapped")
    if cat not in buckets:
        buckets[cat] = []
    buckets[cat].append(g)

# Print summary
print("### Category Distribution")
for cat, items in sorted(buckets.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n#### {cat} ({len(items)} challenges)")
    unique_landmarks = sorted(list(set(item['boss_original_title'] for item in items)))
    print("Featured Landmarks: " + ", ".join(unique_landmarks))
    for item in items:
        num = item.get('puzzle_number')
        num_str = f"#{num}" if num else "[Queue]"
        print(f"  - {num_str} {item['boss_original_title']} -> **{item['boss_pun_title']}**")
