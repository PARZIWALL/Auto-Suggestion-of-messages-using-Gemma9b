import sqlite3

DB_FILE = "chatAndSuggestion_.db"

def initialize_database():
    """
    Initializes the SQLite database and creates necessary tables for chats and suggestions.
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Create table for chat messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create table for suggestions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            other_user_id TEXT NOT NULL,
            suggestion TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()

def insert_message(sender, receiver, message):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO chats (sender, receiver, message)
        VALUES (?, ?, ?)
    ''', (sender, receiver, message))

    connection.commit()
    connection.close()

def insert_suggestion(user_id, other_user_id, suggestion):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO suggestions (user_id, other_user_id, suggestion)
        VALUES (?, ?, ?)
    ''', (user_id, other_user_id, suggestion))

    connection.commit()
    connection.close()

def fetch_conversation(sender, receiver, limit=20):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT sender, receiver, message, timestamp
        FROM chats
        WHERE (sender = ? AND receiver = ?)
           OR (sender = ? AND receiver = ?)
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (sender, receiver, receiver, sender, limit))

    conversation = cursor.fetchall()
    connection.close()

    return conversation[::-1]

def fetch(sender, receiver, limit=20):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute('''SELECT COUNT(*) FROM chats WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)''', (sender, receiver, receiver, sender))
    total_count = cursor.fetchone()[0]
    fetch_limit = min(total_count, limit)
    cursor.execute('''SELECT sender, receiver, message, timestamp FROM chats WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?) ORDER BY timestamp DESC LIMIT ?''', (sender, receiver, receiver, sender, fetch_limit))
    conversation = cursor.fetchall()
    connection.close()
    return conversation[::-1]


def fetch_latest_suggestion(user_id, other_user_id):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT suggestion, timestamp
        FROM suggestions
        WHERE user_id = ? AND other_user_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    ''', (other_user_id,user_id))

    result = cursor.fetchone()
    connection.close()

    if result:
        suggestion, timestamp = result
        return {
            'suggestion': suggestion,
            'timestamp': timestamp
        }
    else:
        return {
            'suggestion': None,
            'timestamp': None
        }



# Initialize the database
if __name__ == "__main__":
    initialize_database()
