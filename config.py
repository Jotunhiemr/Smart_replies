# type: ignore
import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", " ")
    MODEL_NAME: str = "gpt-4o-mini-2024-07-18"
    TEMPERATURE: float = 0.7
    MAX_TOKEN: int = 200

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    TOKEN: str = os.getenv("TOKEN", " ")
    BASE_URL: str = os.getenv(
        "BASE_URL",
        "https://nameless-cliffs-02505-061fd2550135.herokuapp.com",
        )


config = Config()
