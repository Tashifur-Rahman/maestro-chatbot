import os
from dotenv import load_dotenv
load_dotenv()
MODEL = os.getenv(
    "MODEL",
    "qwen3:8b"
)



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