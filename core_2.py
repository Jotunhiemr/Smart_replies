import ollama
import asyncio
import aiohttp
from config import Config
from functools import lru_cache
from typing import List, Dict, Optional


class SmartReply:
    def __init__(self):
        self.model_name = Config.MODEL_NAME
        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKEN
        self.cache = {}
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def setup(self):
        """Initialize the aiohttp session"""
        self.session = aiohttp.ClientSession()
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
            
    @lru_cache(maxsize=32)
    def _get_headers(self) -> Dict:
        """Cached header generation"""
        return {
            'Host': "nameless-cliffs-02505-061fd2550135.herokuapp.com",
            'Content-Type': 'application/json',
            'User-Agent': 'insomnia/11.1.0',
            'Authorization': f'Bearer {Config.TOKEN}',
            'Accept': '*/*'
        }
    
    async def load_history(self) -> Optional[List]:
        """Load conversation history with caching"""
        cache_key = "conversation_history"
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        try:
            async with self.session.get(
                "https://nameless-cliffs-02505-061fd2550135.herokuapp.com"
                "/api/messages/ai/68bc7349115f9cc0606631a1/68bc7cdd00f235eff62205dc",
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                data = await response.json()
                self.cache[cache_key] = data["messages"]
                return data["messages"]
        except aiohttp.ClientError as e:
            print(f"Error loading history: {e}")
            return None
            
    async def smart_replies(self, conversation: List[str]) -> str:
        """Generate smart replies with optimized parameters"""
        # Cache conversation prompt
        prompt_cache_key = "prompt_" + str(hash("".join(conversation)))
        if prompt_cache_key in self.cache:
            prompt = self.cache[prompt_cache_key]
        else:
            prompt = f"""
            The following is a conversation between two speakers:
            ----------------------
            {''.join(conversation)}
            ----------------------
            Kindly generate the best, most appropriate next
            message/response
            in the conversation.
            Consider the user's style of speech, chain of thought and the
            context of the conversation.
            Only provide the next message/response without any additional
            commentary or explanation.
            Provide output in JSON format
            """
            self.cache[prompt_cache_key] = prompt
            
        try:
            response = await asyncio.to_thread(
                ollama.generate,
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "stream": False  # Disable streaming for better performance
                }
            )
            return response.get("response", "").strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"