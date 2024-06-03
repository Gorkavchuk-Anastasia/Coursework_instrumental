import json

DATABASE_FILE = 'database.json'

def load_database():
    try:
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'doctors': [], 'appointments': []}

def save_database(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)
