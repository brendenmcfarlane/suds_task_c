from src.workflow_node import WorkflowNode
from src.agent import SlowGeminiAgent
from src.graph_mutator import WorkflowGraphMutator

# TODO: search.py executes accurately with SlowGeminiAgent
# TODO: finished search writes results to JSON
# [
#     {     
#         "node_id": int,
#         "topology": {
#             "agents": [str],
#             "edges": [(str,str)]
#         },
#         "score": int,
#         "parent_id": int
#     }
# ]
def export_search_results(list_nodes, path):
    with open(path, "w") as file:
        file.write("[\n" + str(list_nodes[0]))
        for i in range(1, len(list_nodes)):
            file.write("," + str(list_nodes[i]))
        file.write("]")
    


def main():
    API_KEY = input("Enter API Key:")
    QUESTION = ("James writes a 3-page letter to 2 different friends twice a week." + 
                "How many pages does he write in a year?")
    PLANNER = SlowGeminiAgent("Planner", "You are the Planner. Propose a concise plan to solve the task.", api_key=API_KEY)
    READER = SlowGeminiAgent("Reader", "You are the Reader. Extract key facts for another agent to use to generate the final answer.", api_key=API_KEY)
    SOLVER = SlowGeminiAgent("Solver", "You are the Solver. Carry out the plan and compute results", api_key=API_KEY)
    VERIFIER = SlowGeminiAgent("Verifier", "You are the Verifier. Double-check the result and produce the final answer only.", api_key=API_KEY)


    seed = 77
    agents = [PLANNER, READER, SOLVER, VERIFIER]
    edges = [("QuestionNode", "Planner"), ("QuestionNode", "Reader"), 
                ("QuestionNode", "Verifier"), ("Planner", "Solver"), ("Reader", "Solver"), 
                ("Solver", "Verifier"), ("Verifier", "SinkNode")]
    root_node = WorkflowNode({"agents": agents, "edges": edges}, seed)
    root_node.construct_mas()
    root_node.run_inference([QUESTION], ["624"])
    # print(root_node)

    mutator = WorkflowGraphMutator(agents, edges, seed=78)
    mutator.pick_mutation()
    root_node.add_child(mutator.get_topology(), 78)
    child_node = root_node.get_children()[0]
    child_node.construct_mas()
    child_node.run_inference([QUESTION], ["624"])
    # print(child_node)
    
    nodes = [root_node, child_node]
    path = "./outputs/d8_trajectory.json"
    # export_search_results(nodes, path)

    



if __name__ == "__main__": main()