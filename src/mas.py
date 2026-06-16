from src.agent import Agent, SlowGeminiAgent
from src.node import AgentNode, QuestionNode, SinkNode
import json
from src.testing.q_a_pairs import Q_A_PAIRS_TEST

class MAS:
    def __init__(self, List_of_agents, List_of_edges):
        self._nodes = {}
        self._transcript = []
        self._edges = List_of_edges
        self._agents = List_of_agents
        self._answer = ""
        self._correct = None
        for agent in List_of_agents:
            self._nodes[agent.get_name()] = AgentNode(agent)
            if agent.get_name() == "QuestionNode": self._nodes[agent.get_name()] = QuestionNode()
            if agent.get_name() == "SinkNode": self._nodes[agent.get_name()] = SinkNode()


        for edge in List_of_edges:
            self.add_edge(edge[0], edge[1])

    def add_edge(self, agent1_name, agent2_name):
        if agent1_name in self._nodes and agent2_name in self._nodes:
            self._nodes[agent1_name].add_outgoing(self._nodes[agent2_name])
            self._nodes[agent2_name].add_incoming(self._nodes[agent1_name])

    def get_question(self):
        return self._nodes["QuestionNode"].get_output()
    
    def get_answer(self):
        return self._nodes["SinkNode"].get_output()

    def execute(self, question): #TODO: Refactor to assume topological sort
        self._nodes["QuestionNode"].set_question(question)
        self.extend_transcript("QuestionNode")
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
                self.extend_transcript(node.get_agent_name())

        return self._nodes["SinkNode"].get_output()     
    
    def get_topology(self):
        if ("QuestionNode" not in self._agents):
            self._agents.insert("QuestionNode", 0)
        if ("SinkNode" not in self._agents):
            self._agents.append("SinkNode")
        return {"nodes": self._agents, "edges": self._edges}

    def extend_transcript(self, agent_name):
        self._transcript.append((agent_name, self._nodes[agent_name].get_output()))

    def get_number_of_agents(self):
        return len(self._nodes) - 2 # Exclude QuestionNode and SinkNode
    
    def reset_mas(self):
        for node in self._nodes.values():
            node._messages = []
            node._output = None
        self._transcript = []
        self._answer = ""
    
    def get_transcript(self):
        return self._transcript
    
    def set_correctness(self, correct):
        self._correct = correct

    def get_correctness(self):
        return self._correct
    
    def export_trajectory(self):
        transcript = [{"agent": agent_name, "output": output} for agent_name, output in self.get_transcript()]

        trajectory = { "topology": self.get_topology(), "question": self.get_question(),
                    "final_answer": self.get_answer(), "agent_calls": self.get_number_of_agents(), 
                    "correct": self.get_correctness(), "transcript": transcript }

        trajectory_json = json.dumps(trajectory, indent=4)
        return trajectory_json

    def export_results(self):
        results = { "topology": self.get_topology(), "question": self.get_question(), 
                "agent_calls": self.get_number_of_agents(), "correct": self.get_correctness() }

        results_json = json.dumps(results, indent=4)
        return results_json
    
def main():
    q_agent = Agent("QuestionNode")
    planner = SlowGeminiAgent("Planner", "Plan the steps to answer the question.")
    reader = SlowGeminiAgent("Reader", "Read the relevant information.")
    solver = SlowGeminiAgent("Solver", "Solve the problem using the information.")
    verifier = SlowGeminiAgent("Verifier", "Verify the solution. Provide the correct final result only")
    sink_agent = Agent("SinkNode", "")


    agents = [q_agent, planner, reader, solver, verifier, sink_agent]
    edges = [("QuestionNode", "Planner"), ("QuestionNode", "Reader"), 
                ("QuestionNode", "Verifier"), ("Planner", "Solver"), 
                 ("Reader", "Solver"), 
                ("Solver", "Verifier"), ("Verifier", "SinkNode")]
    mas = MAS(agents, edges)
    for question, ground_truth in zip(Q_A_PAIRS_TEST[0],Q_A_PAIRS_TEST[1]):
        answer = mas.execute(question)
        print(f"Question: {question}\n\n==========================\n Ground Truth: {ground_truth}\n\n =================================\n")
        print("Answer: " + answer)
        print("\n")
        print()

        print("Transcript:")
        for line in mas._transcript:
            print(line)
        mas.reset_mas()

if __name__ == "__main__":    main()