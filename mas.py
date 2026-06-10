from agent import Agent
from node import AgentNode, QuestionNode, SinkNode

class MAS:
    def __init__(self, List_of_agents, List_of_edges):
        self._nodes = {}
        self._transcript = []
        self._answer = ""
        for agent in List_of_agents:
            self._nodes[agent.get_name()] = AgentNode(agent)
        self._nodes["SinkNode"] = SinkNode()
        self._nodes["QuestionNode"] = QuestionNode()

        for edge in List_of_edges:
            self.add_edge(edge[0], edge[1])

    def add_edge(self, agent1_name, agent2_name):
        if agent1_name in self._nodes and agent2_name in self._nodes:
            self._nodes[agent1_name].add_outgoing(self._nodes[agent2_name])
            self._nodes[agent2_name].add_incoming(self._nodes[agent1_name])

    def execute(self, question):
        self._transcript.append(f"Question: {question}")
        self._nodes["QuestionNode"].set_question(question)
        agent_nodes = list(self._nodes.values())
        while len(agent_nodes) > 0:
            ready_nodes = []
            for node in agent_nodes:
                if node.check_informed():
                    ready_nodes.append(node)
            if len(ready_nodes) == 0:
                raise Exception("No informed nodes available to execute.")
            else:
                node = ready_nodes[0]
                agent_nodes.remove(node)
                node.call_agent()
                for n in node.get_outgoing():
                    n.receive_message(node.get_output())
                self._transcript.append(node.get_output())

        return self._nodes["SinkNode"].get_output()     
    
    def get_number_of_agents(self):
        return len(self._nodes) - 2 # Exclude QuestionNode and SinkNode
    
def main():
    question = "What is the capital of France?"
    planner = Agent("Planner", "Plan the steps to answer the question.")
    reader = Agent("Reader", "Read the relevant information.")
    solver = Agent("Solver", "Solve the problem using the information.")
    verifier = Agent("Verifier", "Verify the solution.")


    agents = [planner, reader, solver, verifier]
    edges = [("QuestionNode", "Planner"), ("QuestionNode", "Reader"), 
                ("QuestionNode", "Verifier"), ("Reader", "Solver"), 
                ("Solver", "Verifier"), ("Verifier", "SinkNode")]
    mas = MAS(agents, edges)
    answer = mas.execute(question)
    print("Answer:", answer)
    print("Transcript:")
    for line in mas._transcript:
        print(line)

if __name__ == "__main__":    main()