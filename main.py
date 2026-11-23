
from llm import generate_response

from memory import *
from config import *
from prompts import SYSTEM_PROMPT
from rag import get_context


# Create a new session
current_session_id = create_session("New Chat")

messages = load_memory(current_session_id)


while True:

    user = input("\nYou: ")

    command = user.lower().strip()

    # Exit
    if command in ["exit", "quit"]:

        print("Exiting Maestro. Goodbye!")
        break


    # Clear current session history
    if command == "/clear":

        clear_memory(current_session_id)

        messages = []

        print("Chat history cleared.")

        continue


    # Show current session history
    if command == "/history":

        show_history(messages)

        continue


    # Create a new session
    if command.startswith("/new "):

        title = user[5:].strip()

        if not title:

            print("Please provide a session title.")

            continue

        current_session_id = create_session(title)

        messages = []

        print(f"New session '{title}' created.")

        continue


    # List all sessions
    if command == "/sessions":

        sessions = get_sessions()

        print("\n========== Sessions ==========")

        for session in sessions:

            print(f"{session['_id']} -> {session['title']}")

        continue


    # Switch sessions
    if command.startswith("/switch "):

        session_id = user[8:].strip()

        messages = load_memory(session_id)

        current_session_id = session_id

        print(f"Switched to session {session_id}.")

        continue


    # Check whether this is a document question
    use_rag = command.startswith("/ask ")

    if use_rag:

        question = user[5:].strip()

        if not question:

            print("Usage: /ask your question")

            continue

    else:

        question = user.strip()


    # Add user message to conversation
    messages.append({
        "role": "user",
        "content": question
    })

    save_memory(
        current_session_id,
        "user",
        question
    )


    # Retrieve document context only for /ask
    context = None

    if use_rag:

        print("\nSearching your documents...")

        context = get_context(question)

        if context:

            print("Relevant information retrieved.")

        else:

            answer = "I couldn't find relevant information about this question in your uploaded documents."

            print("\nMaestro:", answer)

            messages.append({
                "role": "assistant",
                "content": answer
            })

            save_memory(
                current_session_id,
                "assistant",
                answer
            )

            continue


    # Generate answer using Qwen
    answer = generate_response(
        messages[-MAX_MESSAGES:],
        context
    )


    # Add assistant response to conversation
    messages.append({
        "role": "assistant",
        "content": answer
    })

    save_memory(
        current_session_id,
        "assistant",
        answer
    )
