from src.graph_mutator import WorkflowGraphMutator, GraphMutator
from src.agent import GeminiAgent
from src.workflow_node import WorkflowNode
from google import genai
import time


def main():
    API_KEY = input("Enter API Key:")
    QUESTION = ("James writes a 3-page letter to 2 different friends twice a week." + 
                "How many pages does he write in a year?")
    PLANNER = GeminiAgent("Planner", "You are the Planner. Propose a concise plan to solve the task.", api_key=API_KEY)
    READER = GeminiAgent("Reader", "You are the Reader. Extract key facts for another agent to use to generate the final answer.", api_key=API_KEY)
    SOLVER = GeminiAgent("Solver", "You are the Solver. Carry out the plan and compute results", api_key=API_KEY)
    VERIFIER = GeminiAgent("Verifier", "You are the Verifier. Double-check the result and produce the final answer only.", api_key=API_KEY)



    agents = [PLANNER, READER, SOLVER, VERIFIER]
    edges = [("QuestionNode", "Planner"), ("QuestionNode", "Reader"), 
                ("QuestionNode", "Verifier"), ("Planner", "Solver"), ("Reader", "Solver"), 
                ("Solver", "Verifier"), ("Verifier", "SinkNode")]
    edges_two = [("QuestionNode", "Planner"), ("QuestionNode", "Reader"),
                    ("Planner", "Solver"), ("Reader", "Solver"), 
                    ("Verifier", "SinkNode")]
    seed = 77
    root_node = WorkflowNode({"agents": agents, "edges": edges}, seed)
    curr = root_node
    scores = []
    root_node.construct_mas()
    root_node.run_inference([QUESTION], ["624"])
    score = root_node.get_accuracy() - 0.02 * root_node.get_num_calls()
    print((score, {"agents": agents, "edges": edges}))
    scores.append((score, root_node))
    seed += 1
    for _ in range(1):
        mut1 = WorkflowGraphMutator(curr.get_agents()[:], curr.get_edges()[:], seed)
        mut2 = WorkflowGraphMutator(curr.get_agents()[:], curr.get_edges()[:], seed + 1)
        mut1.pick_mutation()
        mut2.pick_mutation()
        topo1, topo2 = mut1.get_topology(), mut2.get_topology()

        curr.add_child(topo1, node_id=seed)
        curr.add_child(topo2, node_id=seed+1)
        seed += 2
        kids = curr.get_children()
        child1, child2 = kids[-2], kids[-1]
        child1.construct_mas()
        child2.construct_mas()
        child1.run_inference([QUESTION], ["624"])
        child2.run_inference([QUESTION], ["624"])
        score1 = child1.get_accuracy() - 0.02 * child1.get_num_calls()
        score2 = child2.get_accuracy() - 0.02 * child2.get_num_calls()
        scores.append((score1, child1, mut1.get_topology()))
        scores.append((score2, child2, mut2.get_topology()))
        print((score1, child1))
        print((score2, child2))
        if (score <= score1 or score <= score2):
            score = max(score1, score2)
            curr = child1 if score1 > score2 else child2
        print(f"Best: {(score, curr)}")
        time.sleep(60)
    
    scores.sort()
    print(scores)




    # # score = root_node.get_score()
    # # with open("trajectory.json", "w") as f:
    # #     json.dump(json.loads(trajectory_json), f, indent=4)
    # # with open("results.json", "w") as f:
    # #     json.dump(json.loads(results_json), f, indent=4)
    # # print(f"Final Score: {score}")
    # root_node.add_child({"agents": agents, "edges": edges_two}, "child1")
    # child_node = root_node.get_children()[0]
    # child_node.construct_mas()
    # child_node.run_inference([QUESTION], ["624"])
    # trajectory_json = child_node._mas.export_trajectory()
    # results_json = child_node._mas.export_results()
    # score = child_node.get_score()
    # with open("trajectory.json", "w") as f:
    #     json.dump(json.loads(trajectory_json), f, indent=4)
    # with open("results.json", "w") as f:
    #     json.dump(json.loads(results_json), f, indent=4)
    # print(f"Final Score: {score}")



if __name__ == "__main__": main()