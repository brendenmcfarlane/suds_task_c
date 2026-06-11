from src.api_throttler import Throttler, gemini_throttler
from src.agent import SlowGeminiAgent
import time

class TestAgent:
    def __init__(self, throttler) -> None:
        self.throttler = throttler
    def make_call(self):
        self.throttler.make_call()


def main():
    # Test one. throtter works as expected
    # t = Throttler()
    # one = TestAgent(t)
    # two = TestAgent(t)
    # start_time = time.time()
    # print(t.api_calls)
    # for i in range(16):
    #     one.make_call()
    #     print(t.api_calls)
    #     two.make_call()
    #     print(t.api_calls)
    #     print(f"time elapsed: {time.time() - start_time}")
    
    # Test two: integration test with LLM
    start_time = time.time()
    API_KEY = input("Enter API Key: ")
    gemma_one = SlowGeminiAgent(prompt = "what movie should i watch", api_key=API_KEY)
    gemma_two = SlowGeminiAgent(prompt = "where is france", api_key=API_KEY)
    j = 1
    for i in range(16):
        print(gemma_one.call())
        print(f"call No.{j};time elapsed: {time.time() - start_time}")
        j += 1
        print(gemma_two.call())
        print(f"call No.{j};time elapsed: {time.time() - start_time}")
        j += 1

if __name__ == "__main__": main()