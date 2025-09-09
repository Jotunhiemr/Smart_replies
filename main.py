# type: ignore
import json
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from core import SmartReply
from utils import setup_logging

logger = setup_logging()

app = FastAPI(title="Smart Reply API",
              version="1.0.0",
              description="Generating appropriate smart replies .")


class ResponseModel(BaseModel):
    response: dict
    timestamp: str


smrpl = SmartReply()


@app.get("/")
def read_root():
    return "Welcome to the Smart Reply API!"


@app.get("/generate-reply/{user_id_1}/{user_id_2}",
         response_model=ResponseModel)
async def generate_reply(user_id_1: str, user_id_2: str) -> dict:
    try:
        conversation = await smrpl.load_history(user_id_1, user_id_2)
        logger.info("Loaded conversation history")
        reply = await smrpl.smart_replies(conversation)
        logger.info(f"Generated reply: {reply}")
        return {"response": json.loads(reply),
                "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                }
    except Exception as e:
        logger.error(f"Error generating reply: {e}")
        return {"response": {"error": "Failed to generate reply"},
                "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                }
