# type: ignore
import ollama
import asyncio
import requests
from config import Config


class SmartReply():
    def __init__(self):
        self.model_name = Config.MODEL_NAME
        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKEN
        self.cache = {}

    async def load_history(self):
        # Constants
        BASE_URL = "https://nameless-cliffs-02505-061fd2550135.herokuapp.com"
        ENDPOINT = "/api/messages/ai/68bc7349115f9cc0606631a1/68bc7cdd00f235eff62205dc"

        # Headers
        headers = {
            'Host': BASE_URL.split('/')[-1],
            'Content-Type': 'application/json',
            'User-Agent': 'insomnia/11.1.0',
            'Authorization': f'Bearer {Config.TOKEN}',
            'Accept': '*/*'
        }

        try:
            response = requests.get(BASE_URL + ENDPOINT, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            return response.json()["messages"]

        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None

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
            return response.get("response", "").strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"
