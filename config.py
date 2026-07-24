import os
from dotenv import load_dotenv
load_dotenv()
MODEL = os.getenv(
    "MODEL",
    "qwen3:8b"
)

FILE_NAME = os.getenv(
    "FILE_NAME",
    "data/chat_history.json"
)

MAX_MESSAGES = int(
    os.getenv(
        "MAX_MESSAGES",
        20
    )
)