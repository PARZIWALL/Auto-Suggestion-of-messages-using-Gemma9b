import sqlite3

# Database file name
DB_FILE = "chat_history.db"

def initialize_database():
    """
    Initializes the SQLite database and creates the necessary table for chat history.
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Create table for chat history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT NOT NULL,
        receiver TEXT NOT NULL,
        message TEXT NOT NULL,
        suggestion TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )

    ''')

    connection.commit()
    connection.close()

def insert_message(sender, receiver, message, suggestion=None):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO chat_history (sender, receiver, message, suggestion)
        VALUES (?, ?, ?, ?)
    ''', (sender, receiver, message, suggestion))

    connection.commit()
    connection.close()

def fetch_conversation(sender, receiver, limit=20):
    """
    Fetches the last `limit` messages between a sender and a receiver.
    Messages are returned in chronological order (oldest to newest).
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT sender, receiver, message, timestamp
        FROM chat_history
        WHERE (sender = ? AND receiver = ?)
           OR (sender = ? AND receiver = ?)
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (sender, receiver, receiver, sender, limit))

    conversation = cursor.fetchall()
    connection.close()

    # Reverse to return in ascending (oldest to newest) order
    return conversation[::-1]

# Initialize the database when the script is run
if __name__ == "__main__":
    initialize_database()