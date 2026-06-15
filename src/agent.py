from typing import Optional
from google import genai
from google.genai import types

from src.api_throttler import gemini_throttler
from api_key import API_KEY

class Agent:
    def __init__(self, name="Agent Smith", prompt=""):
        self._name = name
        self._prompt = prompt
    def get_name(self):
        return self._name
    def get_prompt(self):
        return self._prompt
    def call(self, context="") -> str:
        return " "
    def set_api_key(self, api_key):
        return None
    
class GeminiAgent(Agent):
    def __init__(self, name="Gemini Agent", prompt=""):
        super().__init__(name, prompt)
        self._client: Optional[genai.Client] = None
        self.set_api_key(API_KEY)
        self._model = "gemini-3.1-flash-lite"
        self._config = types.GenerateContentConfig(temperature=1.5, max_output_tokens=1024, seed=42)

    def call(self, context="") -> str:
        if self._client is None:
            raise RuntimeError("API client not configured. Call set_api_key first.")
        input_text = self._prompt + " " + context
        response = self._client.models.generate_content(
            model=self._model,
            contents=input_text,
            config=self._config
        )
        if response.text is None:
            return ""
        
        return response.text
    
    def set_api_key(self, api_key):
        self._client = genai.Client(api_key=api_key)

    def set_model(self, model_name):
        self._model = model_name

class SlowGeminiAgent(Agent):
    def __init__(self, name="Gemini Agent", prompt=""):
        super().__init__(name, prompt)
        self._client: Optional[genai.Client] = None
        self.set_api_key(API_KEY)
        self._model = "gemini-3.1-flash-lite"
        self._config = types.GenerateContentConfig(temperature=1.5, max_output_tokens=1024, seed=42)

    def call(self, context=""):
        gemini_throttler.make_call()
        if self._client is None:
            raise RuntimeError("API client not configured. Call set_api_key first.")
        input_text = self._prompt + " " + context
        response = self._client.models.generate_content(
            model=self._model,
            contents=input_text,
            config=self._config
        )
        if response.text is None:
            return ""
        
        return response.text
    
    def set_api_key(self, api_key):
        self._client = genai.Client(api_key=api_key)

    def set_model(self, model_name):
        self._model = model_name


def main():
    agent = GeminiAgent("Test", "What is the meaning of life?")
    api_key = input("Enter your API key: ")
    agent.set_api_key(api_key)
    print(agent.call(""))
    pass
    # agent = Agent("buddy", "What is the meaning of life?")
    # print (agent.get_name())
    # print (agent.get_prompt())
    # print (agent.call())

if __name__ == "__main__":    main()