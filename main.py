# type: ignore
import json
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from core import SmartReply


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


@app.get("/generate-reply/{user_id}", response_model=ResponseModel)
async def generate_reply():
    conversation = await smrpl.load_history()
    reply = await smrpl.smart_replies(conversation)
    return {"response": json.loads(reply),
            "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }
