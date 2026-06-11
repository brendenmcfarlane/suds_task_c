from agent import GeminiAgent
from mas import MAS
API_KEY = input("Enter your API key: ")
# make sure full MAS setup is working


def main():
    question = ("James writes a 3-page letter to 2 different friends twice a week." + 
                "How many pages does he write in a year?")
    planner = GeminiAgent("Planner", "You are the Planner. Propose a concise plan to solve the task.", api_key=API_KEY)
    reader = GeminiAgent("Reader", "You are the Reader. Extract key facts for another agent to use to generate the final answer.", api_key=API_KEY)
    solver = GeminiAgent("Solver", "You are the Solver. Carry out the plan and compute results", api_key=API_KEY)
    verifier = GeminiAgent("Verifier", "You are the Verifier. Double-check the result and produce the final answer only.", api_key=API_KEY)


    agents = [planner, reader, solver, verifier]
    edges = [("QuestionNode", "Planner"), ("QuestionNode", "Reader"), 
                ("QuestionNode", "Verifier"), ("Planner", "Solver"), ("Reader", "Solver"), 
                ("Solver", "Verifier"), ("Verifier", "SinkNode")]
    mas = MAS(agents, edges)
    answer = mas.execute(question)
    print(mas._nodes["Solver"].get_incoming())
    print("Answer:", answer)

if __name__ == "__main__":    main()
