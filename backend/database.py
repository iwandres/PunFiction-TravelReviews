import os
from datetime import datetime, timedelta, timezone
import uuid
from pymongo import MongoClient

# Use the MONGO_URI from the environment, defaulting to localhost for local testing if missing
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)

db = client["movie_puzzle_db"]
production_pool = db["boss_puzzle_sets"]
staging_pool = db["raw_combinator_pool"]
telemetry_pool = db["PunFiction"]

def get_next_boss_puzzle():
    """Fetches a pristine, approved puzzle from staging."""
    query = {
        "status": "approved",
        "is_consumed": False,
        "family_locked": False
    }
    boss_doc = staging_pool.find_one(query)
    return boss_doc

def lock_consumed_data(boss_doc):
    """Updates the staging database to prevent macro-duplication."""
    # 1. Mark this specific pun as successfully consumed
    staging_pool.update_one(
        {"_id": boss_doc["_id"]},
        {"$set": {"is_consumed": True}}
    )
    
    # 2. Lock the entire family of unused permutations from that base movie
    lock_result = staging_pool.update_many(
        {
            "base_title": boss_doc["base_title"],
            "is_consumed": False 
        },
        {"$set": {"family_locked": True}}
    )
    print(f"Locked {lock_result.modified_count} sister-puns for '{boss_doc['base_title']}'.")

def get_global_blacklist():
    """Fetches every original movie ever used in past puzzles."""
    past_games = production_pool.find({}, {"puzzles.original_movie": 1})
    global_blacklist = []
    for game in past_games:
        for puzzle in game.get("puzzles", []):
            global_blacklist.append(puzzle["original_movie"])
            
    return list(set(global_blacklist))

def assemble_and_store(boss_doc, mini_puzzles_array, temp_boss_id=None, poster_url=None):
    """Packages the data and inserts it into the production database."""
    # Schedule the game for tomorrow at 2:00 AM Pacific Time (9:00 AM UTC). 
    publish_date = datetime.now(timezone.utc).replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
    
    boss_id = temp_boss_id if temp_boss_id else f"boss_{uuid.uuid4().hex[:8]}"
    
    final_document = {
        "boss_id": boss_id,
        "boss_original_title": boss_doc["base_title"],
        "boss_pun_title": boss_doc["pun_title_generated"],
        "boss_pitch": boss_doc["llm_pitch"],
        "difficulty_tier": 1, 
        "puzzles": mini_puzzles_array,
        "published_date": publish_date,
        "created_at": datetime.now(timezone.utc)
    }
    
    if poster_url:
        final_document["boss_poster_url"] = poster_url
        
    result = production_pool.insert_one(final_document)
    print(f"Production Document Created: {result.inserted_id}")
    return result.inserted_id

def flag_puzzle_format_error(original_doc_id):
    """Flags a puzzle in staging that failed NLP validation."""
    staging_pool.update_one(
        {"_id": original_doc_id},
        {"$set": {"status": "requires_custom_format"}}
    )

def record_telemetry_event(puzzle_number, event_type, hints_used=0, attempts=1):
    """Records a telemetry event in the MongoDB collection using atomic increments."""
    update_query = {}
    if event_type == 'start':
        update_query = {"$inc": {"start": 1}}
    elif event_type == 'attempt':
        update_query = {"$inc": {"attempts": 1}}
    elif event_type == 'solve':
        hints_used = max(0, min(4, int(hints_used)))
        clamped_attempts = max(1, min(5, int(attempts)))
        update_query = {
            "$inc": {
                f"solve_{hints_used}": 1,
                f"solve_att_{clamped_attempts}": 1
            }
        }
    elif event_type in ['click_profile', 'click_stats', 'click_help']:
        update_query = {"$inc": {event_type: 1}}
        
    if update_query:
        telemetry_pool.update_one(
            {"_id": puzzle_number},
            update_query,
            upsert=True
        )

def get_telemetry_stats(puzzle_number=None):
    """Fetches aggregated telemetry stats from MongoDB."""
    if puzzle_number:
        doc = telemetry_pool.find_one({"_id": puzzle_number})
        if doc:
            return {
                "start": doc.get("start", 0),
                "attempts": doc.get("attempts", 0),
                "solve_0": doc.get("solve_0", 0),
                "solve_1": doc.get("solve_1", 0),
                "solve_2": doc.get("solve_2", 0),
                "solve_3": doc.get("solve_3", 0),
                "solve_4": doc.get("solve_4", 0),
                "solve_att_1": doc.get("solve_att_1", 0),
                "solve_att_2": doc.get("solve_att_2", 0),
                "solve_att_3": doc.get("solve_att_3", 0),
                "solve_att_4": doc.get("solve_att_4", 0),
                "solve_att_5": doc.get("solve_att_5", 0)
            }
        else:
            return {
                "start": 0,
                "attempts": 0,
                "solve_0": 0,
                "solve_1": 0,
                "solve_2": 0,
                "solve_3": 0,
                "solve_4": 0,
                "solve_att_1": 0,
                "solve_att_2": 0,
                "solve_att_3": 0,
                "solve_att_4": 0,
                "solve_att_5": 0
            }
    else:
        # Fetch all stats and build mapped dictionary
        all_docs = telemetry_pool.find({})
        stats_map = {}
        for doc in all_docs:
            p_num = doc["_id"]
            stats_map[p_num] = {
                "start": doc.get("start", 0),
                "attempts": doc.get("attempts", 0),
                "solve_0": doc.get("solve_0", 0),
                "solve_1": doc.get("solve_1", 0),
                "solve_2": doc.get("solve_2", 0),
                "solve_3": doc.get("solve_3", 0),
                "solve_4": doc.get("solve_4", 0),
                "solve_att_1": doc.get("solve_att_1", 0),
                "solve_att_2": doc.get("solve_att_2", 0),
                "solve_att_3": doc.get("solve_att_3", 0),
                "solve_att_4": doc.get("solve_att_4", 0),
                "solve_att_5": doc.get("solve_att_5", 0)
            }
        return stats_map

user_profiles_pool = db["UserProfiles"]

def get_user_profile(profile_id):
    """Fetches a user profile from MongoDB by profile_id."""
    try:
        profile = user_profiles_pool.find_one({"_id": profile_id})
        if profile:
            return {
                "profile_id": profile["_id"],
                "solved_puzzles": profile.get("solved_puzzles", []),
                "solved_hints": profile.get("solved_hints", {}),
                "attempted_puzzles": profile.get("attempted_puzzles", []),
                "max_streak": profile.get("max_streak", 0)
            }
    except Exception as e:
        print(f"Error fetching user profile {profile_id}: {e}")
    return None

def upsert_user_profile(profile_id, solved_puzzles, solved_hints, attempted_puzzles, max_streak):
    """Upserts user profile state to MongoDB."""
    try:
        user_profiles_pool.update_one(
            {"_id": profile_id},
            {
                "$set": {
                    "solved_puzzles": solved_puzzles,
                    "solved_hints": solved_hints,
                    "attempted_puzzles": attempted_puzzles,
                    "max_streak": max_streak,
                    "last_updated": datetime.now(timezone.utc)
                }
            },
            upsert=True
        )
        return True
    except Exception as e:
        print(f"Error upserting user profile {profile_id}: {e}")
        return False
