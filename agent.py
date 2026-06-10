from typing import Optional
from google import genai


class Agent:
    def __init__(self, name="Agent Smith", prompt=""):
        self._name = name
        self._prompt = prompt

    def get_name(self):
        return self._name
    
    def get_prompt(self):
        return self._prompt
    
    def call(self, context=""):
        #TODO: implment API LLM call here
        return (f"{self._name} was prompted with '{self._prompt}'. \nContext: {context}")
    
class GeminiAgent(Agent):
    def __init__(self, name="Gemini Agent", prompt="", api_key = None):
        super().__init__(name, prompt)
        self._client: Optional[genai.Client] = None
        if api_key is not None:
            self.set_api_key(api_key)
        self._model = "gemini-3.1-flash-lite"

    def call(self, context=""):
        if self._client is None:
            raise RuntimeError("API client not configured. Call set_api_key first.")

        input_text = self._prompt + " " + context
        response = self._client.models.generate_content(
            model=self._model,
            contents=input_text
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