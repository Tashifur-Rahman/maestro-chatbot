from pymongo import MongoClient
from bson import ObjectId

from config import MONGO_URL, DATABASE_NAME, MONGO_URL


# Connect to MongoDB
client = MongoClient(MONGO_URL)

db = client[DATABASE_NAME]

conversations = db["conversations"]


def create_session(title):
    conversation = {
        "title": title,
        "messages": []
    }

    result = conversations.insert_one(conversation)

    return str(result.inserted_id)


def load_memory(session_id):
    conversation = conversations.find_one(
        {"_id": ObjectId(session_id)}
    )

    if conversation:
        return conversation["messages"]

    return []


def save_memory(session_id, role, content):
    conversations.update_one(
        {"_id": ObjectId(session_id)},
        {
            "$push": {
                "messages": {
                    "role": role,
                    "content": content
                }
            }
        }
    )


def clear_memory(session_id):
    conversations.update_one(
        {"_id": ObjectId(session_id)},
        {
            "$set": {
                "messages": []
            }
        }
    )


def show_history(messages):

    print("\n========== Chat History ==========")

    for msg in messages:

        if msg["role"] == "user":
            print(
                f"\033[32mYou      : {msg['content']}\033[0m"
            )

        else:
            print(
                f"\033[33mMaestro  : {msg['content']}\033[0m"
            )