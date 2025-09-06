# type: ignore
from fastapi import FastAPI
from core import SmartReply


app = FastAPI(title="Smart Reply API",
              version="1.0.0",
              description="Generating appropriate smart replies .")
smrpl = SmartReply()


@app.get("/")
def read_root():
    return "Welcome to the Smart Reply API!"


@app.get("/generate-reply/{user_id}")
def generate_reply(user_id: str):
    conversation = smrpl.load_history(user_id)
    reply = smrpl.smart_replies(conversation)
    return {"response": reply}
