from agent import GeminiAgent
from mas import MAS
import json

API_KEY = input("Enter your API key: ")
QUESTION = ("James writes a 3-page letter to 2 different friends twice a week." + 
            "How many pages does he write in a year?")
PLANNER = GeminiAgent("Planner", "You are the Planner. Propose a concise plan to solve the task.", api_key=API_KEY)
READER = GeminiAgent("Reader", "You are the Reader. Extract key facts for another agent to use to generate the final answer.", api_key=API_KEY)
SOLVER = GeminiAgent("Solver", "You are the Solver. Carry out the plan and compute results", api_key=API_KEY)
VERIFIER = GeminiAgent("Verifier", "You are the Verifier. Double-check the result and produce the final answer only.", api_key=API_KEY)

def evaluate_mas(mas, correct_answer):
    final_answer = mas.get_answer()
    print("Final Answer:", final_answer)
    is_correct = (final_answer.strip() == correct_answer.strip())
    print("Is the answer correct?", is_correct)
    mas.set_correctness(is_correct)
    return is_correct

def export_trajectory(mas):
    transcript = [{"agent": agent_name, "output": output} for agent_name, output in mas.get_transcript()]

    trajectory = { "topology": mas.get_topology(), "question": mas.get_question(),
                   "final_answer": mas.get_answer(), "agent_calls": mas.get_number_of_agents(), 
                   "correct": mas.get_correctness(), "transcript": transcript }

    trajectory_json = json.dumps(trajectory, indent=4)
    return trajectory_json

def export_results(mas):
    results = { "topology": mas.get_topology(), "question": mas.get_question(), 
               "agent_calls": mas.get_number_of_agents(), "correct": mas.get_correctness() }

    results_json = json.dumps(results, indent=4)
    return results_json

def main():


    agents = [PLANNER, READER, SOLVER, VERIFIER]
    edges = [("QuestionNode", "Planner"), ("QuestionNode", "Reader"), 
                ("QuestionNode", "Verifier"), ("Planner", "Solver"), ("Reader", "Solver"), 
                ("Solver", "Verifier"), ("Verifier", "SinkNode")]
    mas = MAS(agents, edges)


    mas.execute(QUESTION)
    evaluate_mas(mas, "624")

    trajectory_json = export_trajectory(mas)
    results_json = export_results(mas)
    with open("trajectory.json", "w") as f:
        json.dump(json.loads(trajectory_json), f, indent=4)
    with open("results.json", "w") as f:
        json.dump(json.loads(results_json), f, indent=4)

if __name__ == "__main__":    main()