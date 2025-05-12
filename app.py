from flask import Flask, request, jsonify, render_template
import uuid
import os
from dotenv import load_dotenv
from groq import Groq  # Assuming groq.com provides a Python client
import json
import random
import db
import sqlite3
from db import DB_FILE

load_dotenv("py.env")

app = Flask(__name__)

db.initialize_database()

@app.route('/')
def index():
    return render_template('index.html')

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
client2 = Groq(
    api_key=os.environ.get("GROQ_API_KEY_CHAT"),
)

intents = [
    "greeting",
    "job_inquiry",
    "networking",
    "appreciation",
    "follow_up",
    "introduction",
    "request_recommendation",
    "schedule_meeting",
    "farewell",
    "small_talk"
]

greeting_responses = [
    "Hi there! 👋",
    "Hello! How can I assist you today?",
    "Hey! What's up?",
    "Hi! Hope you're having a great day.",
    "Hello! What brings you here?",
    "Hey there! How can I help?",
    "Hi! Nice to meet you.",
    "Greetings! How may I assist you?",
    "Hey! Need any help?",
    "Hello! I'm here if you need anything."
]

job_inquiry_responses = [
    "Sure! What kind of job are you looking for?",
    "I can help you explore job opportunities. Tell me more.",
    "Are you open to full-time, part-time, or freelance roles?",
    "Let's get you connected with some openings.",
    "I’d be happy to assist with your job search!"
]

schedule_meeting_responses = [
    "Sure! When would you like to schedule the meeting?",
    "Please provide a few time slots that work for you.",
    "I’ll send a calendar invite shortly.",
    "Can you confirm the agenda and participants?",
    "Let’s set up a time that works best for both of us."
]

appreciation_responses = [
    "You're very welcome!",
    "Glad I could help 😊",
    "Thank you for the kind words!",
    "Anytime! Let me know if you need anything else.",
    "Appreciate it!"
]

follow_up_responses = [
    "Just checking in — did you get a chance to review my last message?",
    "Following up on our previous conversation.",
    "Let me know if you need any more details.",
    "I’m here if you need anything further!",
    "Hope everything’s going well — looking forward to your reply."
]

introduction_responses = [
    "Nice to meet you! Tell me a bit about yourself.",
    "Great to connect! What do you do?",
    "Pleasure meeting you!",
    "Looking forward to learning more about your work.",
    "Thanks for the intro! Let’s connect further."
]

request_recommendation_responses = [
    "Happy to recommend! Can you share more details about the role?",
    "Of course — what would you like me to focus on in the recommendation?",
    "I'd be glad to help. Send me your resume or profile link.",
    "Sure! I just need a bit of context on the opportunity.",
    "I’d be honored to recommend you."
]

farewell_responses = [
    "Goodbye! Have a great day!",
    "Take care! Talk to you soon.",
    "Bye for now!",
    "Catch you later!",
    "Signing off — feel free to reach out anytime."
]

small_talk_responses = [
    "Haha, that’s interesting!",
    "Oh really? Tell me more!",
    "I totally get that.",
    "Lol, you made my day!",
    "Just the usual — how about you?"
]

template_responses = {
    "greeting": greeting_responses,
    "job_inquiry": job_inquiry_responses,
    "schedule_meeting": schedule_meeting_responses,
    "appreciation": appreciation_responses,
    "follow_up": follow_up_responses,
    "introduction": introduction_responses,
    "request_recommendation": request_recommendation_responses,
    "farewell": farewell_responses,
    "small_talk": small_talk_responses
}

def classify_intent(message):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You will be given a text message. Classify the intent of the message into one of the following categories: "
                    "greeting, job_inquiry, networking, appreciation, follow_up, introduction, request_recommendation, schedule_meeting, farewell, small_talk. "
                    "In addition, determine whether the message can be replied to using a predefined template, without needing unique user-specific input. "
                    "If it can, mark \"template_reply\" as \"yes\". If the message requires a personalized or context-specific response, mark it as \"no\". "
                    "Respond ONLY with a JSON object in this format: "
                    "{\"category\": \"greeting\", \"template_reply\": \"yes\"}. "
                    "Do not include any explanation or extra text."
                )
            },
            {
                "role": "user",
                "content": "The message is: " + message,
            }
        ],
        model="gemma2-9b-it",
    )
    return extract_category_and_template_flag(chat_completion.choices[0].message.content.strip().lower())

def extract_category_and_template_flag(intent_response):
    try:
        resp = json.loads(intent_response)
        category = resp.get("category")
        template_flag = resp.get("template_reply")
        return category, template_flag
    except json.JSONDecodeError:
        print("JSON parse error:", intent_response)
        return None, None



def generate_text(context,message):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                   "You are a helpful assistant. Given a user's message, respond briefly and naturally, like in a real-time chat. "
                    "Keep it concise, friendly, and context-aware. Use no more than a few sentences. the context of the chat will be given to you. "
                    "Do NOT add explanations or metadata — only reply to the message. only reply to the message. "
                    "context: {context} "
                    
                )
            },
            {
                "role": "user",
                "content": message,
            }
        ],
        model="gemma2-9b-it",
    )
    print(chat_completion.choices[0].message.content.strip())
    return chat_completion.choices[0].message.content.strip()
def generate_template_response(intent):
    response = template_responses.get(intent, ["I'm here to help!"])
    return random.choice(response)

def generate_llm_response(message):
    chat_completion = client2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You're a helpful assistant. Given a user's message, respond briefly and naturally, like in a real-time chat. "
                    "Keep it concise, friendly, and context-aware. Use no more than a few sentences. "
                    "Do NOT add explanations or metadata — only reply to the message."
                )
            },
            {
                "role": "user",
                "content": message,
            }
        ],
        model="gemma2-9b-it",
    )
    return chat_completion.choices[0].message.content.strip()

chat_sessions = {}

@app.route('/start_chat', methods=['POST'])
def start_chat():
    user_id = str(uuid.uuid4())
    chat_sessions[user_id] = []
    return jsonify({"user_id": user_id})

import sqlite3

def sender_exists(sender_id):
    connection = sqlite3.connect(db.DB_FILE)
    cursor = connection.cursor()
    cursor.execute('SELECT 1 FROM chats WHERE sender = ? OR receiver = ? LIMIT 1', (sender_id, sender_id))
    exists = cursor.fetchone() is not None
    connection.close()
    return exists

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender_id = data.get("user_id")
    receiver_id = data.get("receiver_id")
    message = data.get("message")
    
    

    if not sender_id or not receiver_id or not message:
        return jsonify({"error": "Missing sender_id, receiver_id, or message"}), 400

    if not sender_exists(sender_id):
        return jsonify({"error": "Invalid sender ID"}), 400
    
    if "@autogenerate" in message:
            message = autogenerate(message, sender_id, receiver_id)
            print(message)

    intent, method = classify_intent(message)

    if intent is None or method is None:
        return jsonify({"error": "Unable to classify intent or method"}), 400

    if method.lower() == "yes":
        suggestion = generate_template_response(intent)
    else:
        suggestion = generate_llm_response(message)

    message_entry = {
        "sender": sender_id,
        "receiver": receiver_id,
        "message": message,
        "suggestion": suggestion
    }

    # Store message in database (chat_messages)
    db.insert_message(sender=sender_id, receiver=receiver_id, message=message)

    # Store suggestion in database (suggestions)
    db.insert_suggestion(user_id=sender_id, other_user_id=receiver_id, suggestion=suggestion)

    return jsonify({"suggestion": suggestion})

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    user_id = request.args.get("user_id")
    other_user_id = request.args.get("other_user_id")

    if not user_id or not other_user_id:
        return jsonify({"error": "Missing user_id or other_user_id"}), 400

    # Fetch conversation (only messages)
    conversation = db.fetch_conversation(user_id, other_user_id)

    if not conversation:
        return jsonify({"error": "No conversation found"}), 400

    chat_history = []
    for sender, receiver, message, timestamp in conversation:
        chat_history.append({
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "timestamp": timestamp
        })

    # Fetch the latest suggestion independently
    latest_suggestion = db.fetch_latest_suggestion(user_id, other_user_id)

    # Final response
    return jsonify({
        "chat_history": chat_history,
        "latest_suggestion": latest_suggestion['suggestion'] if latest_suggestion else None
    })

@app.route('/get_latest_suggestion', methods=['GET'])
def get_latest_suggestion():
    user_id = request.args.get("user_id")
    other_user_id = request.args.get("other_user_id")

    if not user_id or not other_user_id:
        return jsonify({"error": "Missing user_id or other_user_id"}), 400

    latest_suggestion = db.fetch_latest_suggestion(user_id, other_user_id)

    if not latest_suggestion:
        return jsonify({"error": "No suggestion found"}), 404

    return jsonify({"latest_suggestion": latest_suggestion['suggestion']})




def autogenerate(message, user_id, other_user_id):
    

    context = db.fetch(user_id, other_user_id)
    if(context is None):
        return jsonify({"error": "No context found"}), 200
    generated_text= generate_text(message=message, context=context)

    if generated_text is None :
        return jsonify({"error": "Unable to classify intent or method"}), 400

    

    return generated_text
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
   
