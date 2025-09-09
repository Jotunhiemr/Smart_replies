# type: ignore
import ollama
import asyncio
import requests
from config import Config
from utils import setup_logging

logger = setup_logging()


class SmartReply():
    def __init__(self):
        self.model_name = Config.MODEL_NAME
        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKEN
        self.cache = {}

    async def load_history(self, user_id_1: str, user_id_2: str) -> list:
        # Constants

        ENDPOINT = f"/api/messages/ai/{user_id_1}/{user_id_2}"

        # Headers
        headers = {
            'Host': Config.BASE_URL.split('/')[-1],
            'Content-Type': 'application/json',
            'User-Agent': 'insomnia/11.1.0',
            'Authorization': f'Bearer {Config.TOKEN}',
            'Accept': '*/*'
        }

        try:
            response = requests.get(Config.BASE_URL + ENDPOINT,
                                    headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logger.info("Successfully loaded conversation history")
            return response.json()["messages"][-5:]  # Return last 5 messages

        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request: {e}")
            raise e

    async def smart_replies(self, conversation: list) -> str:
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
                options={
                    "temperature": self.temperature,
                },
            )
            logger.info("Successfully generated smart reply")
            return response.get("response", "").strip()
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise e
