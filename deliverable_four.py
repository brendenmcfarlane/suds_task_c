from graph_mutator import GraphMutator

agents = range(5)
edges = [(0,1), (1,2), (2, 3), (3, 4), (0, 2)]

def main():
    print("expected: range(0, 5)\n[(0,1), (1,2), (2, 3), (3, 4), (0, 2)]\nTrue\nFalse\nTrue\nFalse\nFalse\nTrue\nTrue\nFalse\nFalse")
    mutator = GraphMutator(agents, edges)
    print(f"actual: {mutator._vertices}")
    print(mutator._edges)
    print(mutator.try_add_edge((1,3)))
    print(mutator.try_add_edge((2,3)))
    print(mutator.try_remove_edge((0,2)))
    print(mutator.try_remove_edge((2,3)))
    print(mutator.try_remove_edge((1,3)))

    mutator.add_edge((1, 4))
    print(mutator.try_remove_edge((1, 4)))
    print(mutator.try_remove_edge((2, 3)))

    mutator.remove_edge((1, 4))
    print(mutator.try_remove_edge((1, 4)))
    print(mutator.try_remove_edge((2, 3)))

    mutator.pick_mutation()
    print(mutator._edges)
    mutator.pick_mutation()
    print(mutator._edges)
    mutator.pick_mutation(10)
    print(mutator._edges)


if __name__ == "__main__": main()