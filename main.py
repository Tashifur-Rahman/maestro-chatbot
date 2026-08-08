import ollama
from llm import generate_response
from config import *

from memory import *
from prompts import SYSTEM_PROMPT
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
    answer = generate_response(
    messages[-MAX_MESSAGES:]
    )
    messages.append(
        {"role":"assistant",
         "content":answer
         } )
    save_memory("assistant",answer)
    print("Maestro: ",answer)