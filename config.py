import os
from dotenv import load_dotenv
load_dotenv()
MODEL = os.getenv(
    "MODEL",
    "qwen3:8b"
)

MONGO_URL = os.getenv(
    "MONGO_URL")
DATABASE_NAME = os.getenv(
    "DATABASE_NAME")

MAX_MESSAGES = int(
    os.getenv(
        "MAX_MESSAGES",
        20
    )
)
DATABASE=os.getenv(
    "DATABASE",
    "data/maestro.db"
)