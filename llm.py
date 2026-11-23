
import ollama

from config import MODEL
from prompts import SYSTEM_PROMPT


def generate_response(messages, context=None):

    # Start with Maestro's system instructions
    system_content = SYSTEM_PROMPT

    # Add retrieved document context if available
    if context:

        system_content += """

The following information was retrieved
from the user's uploaded documents.

Use it when answering questions about those documents.

---------------- DOCUMENT CONTEXT ----------------

"""
        system_content += context

        system_content += """

---------------- END OF DOCUMENT CONTEXT ----------------

If the answer is not present in the retrieved context,
clearly tell the user instead of making up an answer.
"""

    # Prepare complete conversation
    chat_messages = [
        {
            "role": "system",
            "content": system_content
        }
    ]

    chat_messages.extend(messages)

    # Generate streaming response
    response = ollama.chat(
        model=MODEL,
        messages=chat_messages,
        stream=True
    )

    full_response = ""

    print("Maestro: ", end="", flush=True)

    for chunk in response:

        token = chunk["message"]["content"]

        print(token, end="", flush=True)

        full_response += token

    print()

    return full_response
