# type: ignore
import ollama
from config import Config


class SmartReply():
    def __init__(self):
        self.model_name = Config.MODEL_NAME
        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKEN

    def load_history(self, user_id):
        pass

    def smart_replies(self, conversation):
        conversation = self.load_history(user_id=None)
        try:
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
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                )
            print("Generated smart reply.")
            return response['response']
        except Exception as e:
            return str(e)
