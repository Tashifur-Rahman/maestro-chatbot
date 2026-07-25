import ollama

from config import *

from memory import *
create_database()
messages=load_memory()
while True:
    user=input("You: ")
    if user.lower().strip() in ["exit","quit"]:
        print("Exiting the chat. Goodbye!")
        break
    if user.lower().strip() == "clear":
        clear_memory()
        messages=[]
        print("Chat History Cleared.")
        continue
    if user.lower().strip() == "history":
        show_history(messages)
        continue
    messages.append(
        {"role":"user",
         "content":user
         } )
    save_memory("user",user)
    response=ollama.chat(
        model=MODEL,
        messages=messages[len(messages)-MAX_MESSAGES:]  # only send the last MAX_MESSAGES messages to the model
    )
    answer=response["message"]["content"]
    messages.append(
        {"role":"assistant",
         "content":answer
         } )
    save_memory("assistant",answer)
    print("Maestro: ",answer)