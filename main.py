import ollama

from config import *

from memory import *
messages=load_memory()
while True:
    user=input("You: ")
    if user.lower().strip() in ["exit","quit"]:
        print("Exiting the chat. Goodbye!")
        break
    messages.append(
        {"role":"user",
         "content":user
         } )
    response=ollama.chat(
        model=MODEL,
        messages=messages[len(messages)-MAX_MESSAGES:]  # only send the last MAX_MESSAGES messages to the model
    )
    answer=response["message"]["content"]
    messages.append(
        {"role":"assistant",
         "content":answer
         } )
    save_memory(messages)
    print("Maestro: ",answer)