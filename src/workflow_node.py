from src.mas import MAS
import json

class WorkflowNode:
    def __init__(self, topology, node_id, parent=None):
        #{
         #   "agents": ["agent1", "agent2"],
          #  "edges": [("node1", "node2"), ... , ("node2", "node3")]}
        self._topology = topology
        self._node_id = node_id
        self._parent = parent
        self._children = []
        self._mas = None
        self._results = {"successes": [], "failures": [], "score": None}
    def __str__(self):
        if self._parent is None:
            parent = 0
        else:
            parent = str(self._parent.get_node_id())
        mas_representation = {"node_id": str(self._node_id),
                              "topology": self._topology["edges"], 
                              "score":self._results["score"], 
                              "parent_id": parent}
        return json.dumps(mas_representation, indent=4)
    def __repr__(self):
        return self._node_id
    def add_child(self, topology, node_id):
        child_node = WorkflowNode(topology, node_id, parent=self)
        self._children.append(child_node)

    def get_children(self):
        return self._children
    
    def get_parent(self):
        return self._parent
    
    def set_parent(self, parent_node):
        self._parent = parent_node

    def get_node_id(self):
        return self._node_id
    
    def get_agents(self):
        return self._topology["agents"]
    
    def get_edges(self):
        return self._topology["edges"]
    
    def get_accuracy(self):
        return len(self._results["successes"]) / (len(self._results["successes"]) + len(self._results["failures"]))

    def get_num_calls(self): 
        return self._mas.get_number_of_agents()
    
    def get_score(self):
        return self._results["score"]
    
    def run_inference(self, questions: list[str], answers: list[str]):
        #create mas given topology and execute with each question, store results in self._results
        if not isinstance(self._mas, MAS):
            raise Exception("MAS not constructed yet.")
        for question, answer in zip(questions, answers):
            self._mas.reset_mas()
            self._mas.execute(question)
            final_answer = self._mas.get_answer()
            is_correct = (final_answer.strip() == answer.strip())
            if is_correct:
                self._results["successes"].append((question, answer, final_answer))
            else:
                self._results["failures"].append((question, answer, final_answer))
        self._results["score"] = len(self._results["successes"]) / (len(self._results["successes"]) + len(self._results["failures"])) - (0.02 * self._mas.get_number_of_agents()) # small penalty for more calls, to encourage simpler solutions

    def construct_mas(self):
        #need to add q and sink node in here
        agents = [agent for agent in self._topology["agents"]]
        edges = [edge for edge in self._topology["edges"]]
        self._mas = MAS(agents, edges)  
        