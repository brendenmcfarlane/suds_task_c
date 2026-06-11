from src.agent import GeminiAgent
from src.workflow_node import WorkflowNode
import json

API_KEY = input("Enter your API key: ")
QUESTION = ("James writes a 3-page letter to 2 different friends twice a week." + 
            "How many pages does he write in a year?")
PLANNER = GeminiAgent("Planner", "You are the Planner. Propose a concise plan to solve the task.", api_key=API_KEY)
READER = GeminiAgent("Reader", "You are the Reader. Extract key facts for another agent to use to generate the final answer.", api_key=API_KEY)
SOLVER = GeminiAgent("Solver", "You are the Solver. Carry out the plan and compute results", api_key=API_KEY)
VERIFIER = GeminiAgent("Verifier", "You are the Verifier. Double-check the result and produce the final answer only.", api_key=API_KEY)




def main():


    agents = [PLANNER, READER, SOLVER, VERIFIER]
    edges = [("QuestionNode", "Planner"), ("QuestionNode", "Reader"), 
                ("QuestionNode", "Verifier"), ("Planner", "Solver"), ("Reader", "Solver"), 
                ("Solver", "Verifier"), ("Verifier", "SinkNode")]
    edges_two = [("QuestionNode", "Planner"), ("QuestionNode", "Reader"),
                    ("Planner", "Solver"), ("Reader", "Solver"), 
                    ("Verifier", "SinkNode")]
    
    root_node = WorkflowNode({"agents": agents, "edges": edges}, "root")
    root_node.construct_mas()
    #root_node.run_inference([QUESTION], ["624"])
    # trajectory_json = root_node._mas.export_trajectory()
    # results_json = root_node._mas.export_results()
    # score = root_node.get_score()
    # with open("trajectory.json", "w") as f:
    #     json.dump(json.loads(trajectory_json), f, indent=4)
    # with open("results.json", "w") as f:
    #     json.dump(json.loads(results_json), f, indent=4)
    # print(f"Final Score: {score}")
    root_node.add_child({"agents": agents, "edges": edges_two}, "child1")
    child_node = root_node.get_children()[0]
    child_node.construct_mas()
    child_node.run_inference([QUESTION], ["624"])
    trajectory_json = child_node._mas.export_trajectory()
    results_json = child_node._mas.export_results()
    score = child_node.get_score()
    with open("trajectory.json", "w") as f:
        json.dump(json.loads(trajectory_json), f, indent=4)
    with open("results.json", "w") as f:
        json.dump(json.loads(results_json), f, indent=4)
    print(f"Final Score: {score}")
if __name__ == "__main__":    main()
