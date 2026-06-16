from collections import defaultdict
import random

from src.agent import Agent, SlowGeminiAgent

ORDER = ["QuestionNode", "Planner", "Reader", "Solver", 
         "ArithmeticChecker", "Verifier", "Reflector", "SinkNode"]
PROMPTS = {"QuestionNode": " ", "Planner": " ", "Reader": " ", "Solver": " ", 
         "ArithmeticChecker": " ", "Verifier": " ", "Reflector": " ", "SinkNode": " " }
class GraphMutator():
    def __init__(self, vertices, edges, seed = 100) -> None:
        self._vertices = vertices[:]
        self._edges = edges[:]
        self._seed = seed
        
    def get_topology(self):
        return {"vertices": self._vertices, "edges": self._edges}
    
    def try_add_edge(self, new_edge):
        if new_edge in self._edges:
            return False
        elif new_edge[0] not in self._vertices:
            return False
        else:
            return (new_edge[1] in self._vertices)
    ##
    ##
    def try_remove_edge(self, old_edge):
        if (old_edge in self._edges):
            test_edges = self._edges[:]
            test_edges.remove(old_edge)
            test_ver_1, test_ver_2 = self._vertices[:], self._vertices[:]
            test_ver_1.insert(0, old_edge[0])
            test_ver_2.append(old_edge[1])
            test_1 = self.graph_is_connected(test_ver_1, test_edges)
            test_2 = self.graph_is_connected(test_ver_2, test_edges)
            return test_1 and test_2
        else: 
            return False
        
    def add_edge(self, new_edge):
        self._edges.append(new_edge)

    def remove_edge(self, old_edge):
        self._edges.remove(old_edge)
    
    def graph_is_connected(self, vertices, edges):
        # assume element 0 is the que
        # stion, element -1 is the sink
        if not vertices:
            return True

        # Build adjacency list
        graph = defaultdict(list)
        for e in edges:
            graph[e[0]].append(e[1])
        # DFS
        visited = set()

        def dfs(node):
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor)

        dfs(vertices[0])

        return vertices[-1] in visited
    
    def pick_mutation(self, seed=None) -> None:
        if seed is None:
            random.seed(self._seed)
        else:
            random.seed(seed)
        
        self._seed += 1
        mutation_found = False
        while (not mutation_found):

            left = random.randint(0, len(self._vertices)-2)
            right = random.randint(left + 1, len(self._vertices)-1)
            if self.try_add_edge((left, right)):
                self.add_edge((left, right))
                mutation_found = True
            elif self.try_remove_edge((left, right)):
                self.remove_edge((left, right))
                mutation_found = True
            else:
                mutation_found = False
    
class WorkflowGraphMutator(GraphMutator):
        #TODO: when cleaning, have list of agent names(vertices) and list of agent objects extend
        def __init__(self, vertices, edges, seed = 100) -> None:
            self._agents = vertices
            super().__init__([v.get_name() for v in vertices], edges, seed)
        def get_topology(self):
            return {"agents": self._agents, "edges": self._edges, "vertices": self._vertices}
        def pick_mutation(self, seed=None) -> None:
            if seed is None:
                random.seed(self._seed)
            else:
                random.seed(seed)
            
            self._seed += 1
            mutation_found = False
            while(not mutation_found):
                left = random.randint(0, len(ORDER)-2)
                right = random.randint(left, len(ORDER)-1)
                left = ORDER[left]
                right = ORDER[right]
                if left == right and self.try_add_agent(left):
                    self.add_agent(left)
                    mutation_found = True
                elif left == right and self.try_remove_agent(left):
                    self.remove_agent(left)
                    mutation_found = True
                elif left != right and self.try_add_edge((left, right)):
                    self.add_edge((left, right))    
                    mutation_found = True
                elif left != right and self.try_remove_edge((left, right)):
                    self.remove_edge((left, right))
                    mutation_found = True
                else:
                    mutation_found = False
        
        def try_remove_agent(self, agent: str) -> bool:
            if agent in ["QuestionNode", "Planner", "Solver", "SinkNode"]: return False
            elif agent not in self._vertices: return False
            else: return True
        
        def remove_agent(self, agent:str) -> None:
            '''Removes agent object with name <agent>.
            Preconditions: agent.get_name() are unique;
            self.try_remove_agent(agent) == True.'''
            pred = []
            succ = []
            for e in self._edges:
                if e[0] == agent: 
                    succ.append(e[1])
                elif e[1] == agent: 
                    pred.append(e[0])
            for p in pred:
                for s in succ:
                    if self.try_add_edge((p, s)): self.add_edge((p, s))
            for p in pred:
                self.remove_edge((p, agent))
            for s in succ:
                self.remove_edge((agent, s))
            
            index = self._vertices.index(agent)
            self._vertices.pop(index)
            self._agents.pop(index)

        def try_add_agent(self, agent:str) -> bool:
            return not agent in self._vertices
        
        def add_agent(self, agent:str) -> None:
            agent_index = ORDER.index(agent)
            pred_agents = ORDER[:agent_index:][::-1]
            for p in pred_agents:
                pred_name = p
                if p in self._vertices: break
            for e in self._edges:
                if (e[0] == pred_name) and (ORDER.index(e[1]) > agent_index): 
                    succ_name = e[1]
                    break

            self.add_edge((pred_name, agent))
            self.add_edge((agent, succ_name))
            self.remove_edge((pred_name, succ_name))

            pred_index = self._vertices.index(pred_name)
            agent_obj = SlowGeminiAgent(agent, PROMPTS[agent]) # TODO fix this prompt
            self._agents.insert(pred_index + 1, agent_obj)
            self._vertices.insert(pred_index + 1, agent)


            
