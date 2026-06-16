from src.graph_mutator import WorkflowGraphMutator, GraphMutator
from src.agent import Agent
from src.workflow_node import WorkflowNode
from google import genai
import time

def export_search_results(list_nodes, path):
    with open(path, "w") as file:
        file.write("[\n" + str(list_nodes[0]))
        for i in range(1, len(list_nodes)):
            file.write("," + str(list_nodes[i]))
        file.write("]")

def main():
    API_KEY = "AIzaSyAFovarXvQGDDR25RrA_NwRa3ADajsc5B4"
    QUESTION = ("James writes a 3-page letter to 2 different friends twice a week." + 
                "How many pages does he write in a year?")
    PLANNER = Agent("Planner", "You are the Planner. Propose a concise plan to solve the task.")
    READER = Agent("Reader", "You are the Reader. Extract key facts for another agent to use to generate the final answer.")
    SOLVER = Agent("Solver", "You are the Solver. Carry out the plan and compute results")
    VERIFIER = Agent("Verifier", "You are the Verifier. Double-check the result and produce the final answer only.")
    QUESTIONAGENT= Agent("QuestionNode", "")
    SINKAGENT = Agent("SinkNode", "")
    agents = [QUESTIONAGENT,PLANNER, READER, SOLVER, VERIFIER, SINKAGENT]
    edges = [("QuestionNode", "Planner"), ("QuestionNode", "Reader"), 
                ("QuestionNode", "Verifier"), ("Planner", "Reader"), 
                ("Planner", "Verifier"), ("Planner", "Solver"), 
                ("Reader", "Solver"), ("Reader", "Verifier"), (
                    "Solver", "Verifier"), ("Verifier", "SinkNode")]
    
    #node removal
    wkflwnd = WorkflowNode({"agents": [QUESTIONAGENT, VERIFIER, SINKAGENT], "edges": [("QuestionNode", "Verifier"), ("Verifier", "SinkNode")]}, 70)
    mut = WorkflowGraphMutator(wkflwnd.get_agents()[:], wkflwnd.get_edges()[:], 70)
    mut.try_remove_agent("QuestionNode")
    mut.try_remove_agent("ArithmeticChecker")
    mut.try_remove_agent("Verifier")
        #simple node removal
    mut.remove_agent("Verifier")


    mut = WorkflowGraphMutator([QUESTIONAGENT,PLANNER, READER, VERIFIER, SINKAGENT], 
                               [("QuestionNode", "Planner"), ("QuestionNode", "Reader"),
                                    ("Planner", "Verifier"), ("Reader", "Verifier"), 
                                    ("Verifier", "SinkNode") ], 70)

    mut.remove_agent("Verifier")
    print(" ")

    mut.try_add_agent("Verifier")
    mut.try_add_agent("Planner")
    mut.add_agent("Verifier")
    i = 0
    mut.pick_mutation()


if __name__ == "__main__": main()