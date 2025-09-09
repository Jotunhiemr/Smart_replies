# type : ignore
import os
from dotenv import load_dotenv


load_dotenv()


class Config:

    MODEL_NAME = "qwen2.5"
    TEMPERATURE = 0.7
    MAX_TOKEN = 200
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    TOKEN = os.getenv("TOKEN", " ")
    URL = os.getenv(
        "https://nameless-cliffs-02505-061fd2550135.herokuapp.com/"
        "api/messages/ai",
        ""
    )


config = Config()
