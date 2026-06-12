from collections import defaultdict
import random


class GraphMutator():
    def __init__(self, vertices, edges, seed = 100) -> None:
        self._vertices = vertices[:]
        self._edges = edges[:]
        self._seed = seed
        
    def get_topology(self):
        return {"vertices": self._vertices, "edges": self._edges}
    
    def try_add_edge(self, new_edge):
        if not(new_edge in self._edges):
            return True
        else: 
            return False
    
    def try_remove_edge(self, old_edge):
        if (old_edge in self._edges):
            test_edges = self._edges[:]
            test_edges.remove(old_edge)
            return self.graph_is_connected(self._vertices, test_edges)
        else: 
            return False
        
    def add_edge(self, new_edge):
        self._edges.append(new_edge)

    def remove_edge(self, old_edge):
        self._edges.remove(old_edge)
    
    def graph_is_connected(self, vertices, edges):
        # assume element 0 is the question, element -1 is the sink

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

        left = random.randint(0, len(self._vertices)-2)
        right = random.randint(left + 1, len(self._vertices)-1)
        if self.try_add_edge((left, right)):
            self.add_edge((left, right))
        elif self.try_remove_edge((left, right)):
            self.remove_edge((left, right))
        else:
            self.pick_mutation()
    
class WorkflowGraphMutator(GraphMutator):
        def __init__(self, vertices, edges, seed = 100) -> None:
            super().__init__(vertices, edges, seed)
        def get_topology(self):
            return {"agents": self._vertices, "edges": self._edges}
        def pick_mutation(self, seed=None) -> None:
            if seed is None:
                random.seed(self._seed)
            else:
                random.seed(seed)
            
            self._seed += 1

            left = random.randint(0, len(self._vertices)-2)
            right = random.randint(left + 1, len(self._vertices)-1)
            left = self._vertices[left].get_name()
            right = self._vertices[right].get_name()
            if self.try_add_edge((left, right)):
                self.add_edge((left, right))
            elif self.try_remove_edge((left, right)):
                self.remove_edge((left, right))
            else:
                self.pick_mutation()
