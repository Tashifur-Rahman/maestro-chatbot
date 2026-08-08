import ollama
from config import MODEL, MAX_MESSAGES

def generate_response(messages):
    response=ollama.chat(
        model=MODEL,
        messages=messages,
        stream=True
    )
    full_response=""
    for chunk in response:
        token=chunk["message"]["content"]
        print(token,end="",flush=True) #print the token without a newline and flush the output buffer
        full_response+=token

    print()  # Print a newline after the response is complete
    return full_response