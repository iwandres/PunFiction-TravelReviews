import json

# Define the category to theme mapping
landmark_theme_mapping = {
    # Ancient Ruins & Archaeological Sites
    "Colosseum": "ancient_ruins",
    "Pyramids of Giza": "ancient_ruins",
    "Petra": "ancient_ruins",
    "Chichen Itza": "ancient_ruins",
    "Angkor Wat": "ancient_ruins",
    "Machu Picchu": "ancient_ruins",
    "Pantheon": "ancient_ruins",
    "Roman Forum": "ancient_ruins",
    "Stonehenge": "ancient_ruins",

    # Natural Wonders & Landscapes
    "Grand Canyon": "natural_wonders",
    "Great Barrier Reef": "natural_wonders",
    "Yellowstone National Park": "natural_wonders",
    "Loch Ness": "natural_wonders",
    "Black Forest": "natural_wonders",
    "Matterhorn": "natural_wonders",
    "Cliffs of Moher": "natural_wonders",
    "Giant's Causeway": "natural_wonders",

    # Historic Towers, Monuments & Statues
    "Eiffel Tower": "historic_monuments",
    "Taj Mahal": "historic_monuments",
    "Christ the Redeemer": "historic_monuments",
    "Big Ben": "historic_monuments",
    "Leaning Tower of Pisa": "historic_monuments",
    "Atomium": "historic_monuments",

    # Castles, Fortresses & Cathedrals
    "Tower of London": "castles_cathedrals",
    "Edinburgh Castle": "castles_cathedrals",
    "Mont Saint-Michel": "castles_cathedrals",
    "Sagrada Família": "castles_cathedrals",
    "St. Peter's Basilica": "castles_cathedrals",
    "Notre-Dame Cathedral": "castles_cathedrals",
    "Alcatraz Island": "castles_cathedrals",

    # Bridges, Canals & Historic Engineering
    "Great Wall of China": "bridges_canals",
    "Golden Gate Bridge": "bridges_canals",
    "Panama Canal": "bridges_canals",
    "Tower Bridge": "bridges_canals",
    "Grand Canal": "bridges_canals",

    # Famous Streets, Squares & Towns
    "Times Square": "streets_squares",
    "Spanish Steps": "streets_squares",
    "La Rambla": "streets_squares",
    "Santorini": "streets_squares",

    # Modern Skyscrapers & Tall Structures
    "Burj Khalifa": "modern_skyscrapers",
    "Empire State Building": "modern_skyscrapers",
    "Space Needle": "modern_skyscrapers"
}

file_path = 'backend/travelreviews_daily_games.json'

with open(file_path, 'r', encoding='utf-8') as f:
    games = json.load(f)

print(f"Loaded {len(games)} challenges.")

updated_count = 0
for g in games:
    orig = g['boss_original_title']
    theme = landmark_theme_mapping.get(orig)
    if theme:
        g['page_theme'] = theme
        updated_count += 1
    else:
        print(f"WARNING: Landmark '{orig}' was not mapped to a theme!")

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(games, f, indent=2, ensure_ascii=False)

print(f"Successfully updated {updated_count} challenges in {file_path}.")
