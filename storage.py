import json
import os

DB_FILE = "db.json"

def load_db():
    # Reads local JSON data store safely, returning structured maps.
    if not os.path.exists(DB_FILE):
        return {"users": {}, "projects": {}, "bugs": {}, "gamification": {}, "bug_counter": 0}
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"users": {}, "projects": {}, "bugs": {}, "gamification": {}, "bug_counter": 0}

def save_db(data):
    # Commits absolute delta updates safely back to your db.json structural layout.
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)