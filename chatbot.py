

import ollama
import json
import os
FILE_NAME="chat_history.json"
MAX_MESSAGES=20
if os.path.exists(FILE_NAME):
    try:
        with open(FILE_NAME,"r") as f:
            messages=json.load(f)
    except json.JSONDecodeError: #if json file is empty or corrupted, start with an empty list
        messages=[]
else:
    messages=[]
while True:
    user=input("User: ")
    #Exit cmd
    if user.lower() in ["exit","quit"]:
        break
    if user.lower().strip() == "/history":

        print("\033[1;36m========== Chat History ==========\033[0m")

        for msg in messages:

            if msg["role"] == "user":
                print(f"\033[32mYou      : {msg['content']}\033[0m")

            else:
                print(f"\033[33mMaestro  : {msg['content']}\033[0m")

        continue
        #clear chat history cmd
    if user.lower() == "/clear":
        messages=[]
        with open(FILE_NAME,"w") as f:
            json.dump(messages,f,indent=4)
        print("Chat History Cleared.")
        continue 

    messages.append(
        {
            "role": "user",
         "content": user
        } )
    # Limit memory size

    if len(messages) > MAX_MESSAGES:
        messages = messages[len(messages) - MAX_MESSAGES:]
    #send messages to the model and get the response
    response=ollama.chat(
        model="qwen3:8b",
        messages=messages
    )
    answer=response["message"]["content"]
    messages.append(
        {
            "role":"assistant",
            "content":answer
        })
    print("Maestro:",answer)

    with open(FILE_NAME,"w") as f:
        json.dump(messages,f,indent=4)