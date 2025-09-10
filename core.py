# type: ignore
import json
import re
import asyncio
import requests
from openai import OpenAI
from config import Config
from utils import setup_logging

logger = setup_logging()


class SmartReply():
    def __init__(self):
        self.model_name = Config.MODEL_NAME
        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKEN
        self.cache = {}
        self.model = OpenAI(api_key=Config.OPENAI_API_KEY)

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
                self.model.responses.create,
                model=self.model_name,
                input=prompt,
                # reasoning={"summary": "concise"}
            )
            logger.info("Successfully generated smart reply")
            # Extract first message text
            if response.output and response.output[0].content:
                reply_text = response.output[0].content[0].text.strip()

                # Remove markdown fences if present
                reply_text = re.sub(r"^```(?:json)?", "", reply_text)
                reply_text = re.sub(r"```$", "", reply_text).strip()
                return json.loads(reply_text)

            return {}
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise e
