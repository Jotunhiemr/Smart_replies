# type: ignore
import ollama
import asyncio
from config import Config


class SmartReply():
    def __init__(self):
        self.model_name = Config.MODEL_NAME
        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKEN
        self.cache = {}

    async def load_history(self, user_id):
        pass

    async def smart_replies(self, conversation):
        prompt = f"""
            The following is a conversation between two speaker:
            ----------------------
            {conversation}
            ----------------------
            Kindly generate the best, most appropriate next
            message/response
            in the conversation.
            consider the user's style of speech, chain of thought and the
            context of the conversation.

            Only provide the next message/response without any additional
            commentary or explanation.
            Provide output in JSON format
            """
        try:
            response = await asyncio.to_thread(
                ollama.generate,
                model=self.model_name,
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response.get("response", "").strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"
