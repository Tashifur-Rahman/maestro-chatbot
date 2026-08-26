import ollama
from llm import generate_response
from memory import *
from config import *
from prompts import SYSTEM_PROMPT

#create a new session
current_session_id = create_session("New Chat")
messages = load_memory(current_session_id)

while True:
    user=input("You: ")
    if user.lower().strip() in ["exit","quit"]:
        print("Exiting...")
        break
    if user.lower().strip() == "/clear":
        clear_memory(current_session_id)
        messages=[]
        print("Chat history cleared.")
        continue
    if user.lower().strip() =="/history":
        show_history(messages)
        continue
    # New session creation command
    if user.lower().startswith("/new "):
        title=user[5:].strip()
        if not title:
            print("Please provide a title for the new session. Usage: /new <title>")
            continue
        current_session_id=create_session(title)
        messages=[]
        print(f"New session '{title}' created.")
        continue
    # List all sessions command
    if user.lower().strip()=="/sessions":
        sessions=get_sessions()
        print("\n========== Sessions ==========")
        for session in sessions:
            print(f"{session['_id']}  →  {session['title']}")
        continue

    # switch to a different session command
    if user.lower().startswith("/switch "):
        session_id=user[8:].strip()
        messages=load_memory(session_id)
        current_session_id=session_id
        print(f"Switched to session {session_id}.")
        continue

    messages.append(
        {"role":"user",
         "content":user
         }
    )
    save_memory(current_session_id,"user",user) #add the user message to the database
    answer=generate_response(messages[-MAX_MESSAGES:]) #get the last MAX_MESSAGES messages for context
    messages.append(
        {"role":"assistant",
         "content":answer
         }
    )
    save_memory(current_session_id,"assistant",answer)
    print("Maestro:",answer)
