import json
import os

from config import FILE_NAME
def load_memory():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                messages = json.load(f)
        except json.JSONDecodeError:  # if json file is empty or corrupted, start with an empty list
            messages = []
    else:
        messages = []
    return messages
def save_memory(messages):
    with open(FILE_NAME, "w") as f:
        json.dump(messages, f, indent=4)

def clear_memory():
    messages = []
    save_memory(messages)
    print("Chat History Cleared.")

def show_history(messages):
    print("\033[1;36m========== Chat History ==========\033[0m")
    for msg in messages:
        if msg["role"] == "user":
            print(f"\033[32mYou      : {msg['content']}\033[0m")
        else:
            print(f"\033[33mMaestro  : {msg['content']}\033[0m")

