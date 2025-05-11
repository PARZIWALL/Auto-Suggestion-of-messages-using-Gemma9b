Here's a sample README for your project:

---

# Chat API with Intent Handling and Message Suggestions

This project provides a Flask-based chat API where users can interact with a chatbot, send messages, receive responses, and get suggestions based on their previous messages. The chat history is stored in a SQLite database, and each message can have a suggestion that will be shown to the user.

## Features

* **Start a Chat**: Initiates a chat session with a unique user ID.
* **Send Messages**: Users can send messages, and the chatbot will respond based on the intent of the message.
* **Get Chat History**: Fetches the chat history between two users.
* **Message Suggestions**: When viewing chat history, users can receive message suggestions based on the last message in the conversation.

## Requirements

* Python 3.x
* Flask
* SQLite

### Install dependencies

1. Create a virtual environment (if you don't have one):

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   * For Windows:

     ```bash
     .\venv\Scripts\activate
     ```
   * For macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

3. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### `requirements.txt` example:

```
Flask==2.1.1
sqlite3==3.36.0
```

## Setup

1. **Initialize the Database:**

   The SQLite database is used to store chat history. The database will be automatically initialized when the server is started.

2. **Run the Flask App:**

   Start the Flask development server by running:

   ```bash
   python app.py
   ```

   By default, the server will run on `http://127.0.0.1:5000/`.

## API Endpoints

### 1. `/start_chat` (POST)

* **Description**: Starts a new chat session and returns a unique `user_id` for that session.
* **Request**: `POST` with no body.
* **Response**:

  ```json
  {
    "user_id": "unique-user-id"
  }
  ```

### 2. `/send_message` (POST)

* **Description**: Sends a message from the user to the chatbot. The chatbot will process the message and generate a response.
* **Request**:

  ```json
  {
    "user_id": "unique-user-id",
    "message": "Hello, how are you?"
  }
  ```
* **Response**:

  ```json
  {
    "response": "I'm doing well, thanks for asking!"
  }
  ```

### 3. `/get_chat_history` (GET)

* **Description**: Fetches the last 20 messages between a sender and receiver.
* **Request**:

  ```bash
  GET /get_chat_history?user_id=unique-user-id&other_user_id=other-user-id
  ```
* **Response**:

  ```json
  {
    "chat_history": [
      {
        "sender": "unique-user-id",
        "receiver": "other-user-id",
        "message": "Hello, how are you?",
        "timestamp": "2025-05-11 19:25:00"
      },
      {
        "sender": "other-user-id",
        "receiver": "unique-user-id",
        "message": "I'm doing well, thanks for asking!",
        "timestamp": "2025-05-11 19:26:00"
      },
      ...
    ],
    "latest_suggestion": "You could ask, 'How's the weather today?'"
  }
  ```

### 4. `/insert_message` (DB operation)

* **Description**: Inserts messages into the database (for use with backend operations).
* **Request**: Handled within the app during message sending.

## Database Structure

The database stores chat messages in the `chat_history` table. The schema is:

```sql
CREATE TABLE chat_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender TEXT NOT NULL,
  receiver TEXT NOT NULL,
  message TEXT NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## How Suggestions Work

When fetching chat history, the system will analyze the latest message in the conversation to suggest possible follow-up actions or responses. If the latest message includes certain keywords, a suggestion will be provided to the user.

Example:

* **Latest Message**: "Hello, how are you?"
* **Suggestion**: "You could ask, 'How's the weather today?'"

This suggestion will appear under the `latest_suggestion` key in the response.

## File Structure

```bash
.
├── app.py               # Main Flask application
├── db.py                # Database operations (CRUD functions)
├── requirements.txt     # Required Python libraries
└── chat_history.db      # SQLite database file (automatically created)
```

## Contributing

If you'd like to contribute, feel free to fork this repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This README covers the project setup, API usage, and structure. You can expand or modify this based on specific requirements or features.
