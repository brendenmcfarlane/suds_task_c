import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def dag_layout(G):
    levels = {}

    for node in nx.topological_sort(G):
        parents = list(G.predecessors(node))
        levels[node] = (
            max(levels[p] for p in parents) + 1
            if parents else 0
        )

    pos = {}
    level_nodes = {}

    for node, level in levels.items():
        level_nodes.setdefault(level, []).append(node)

    # #before
    # for level, nodes in level_nodes.items():
    #     for i, node in enumerate(nodes):
    #         pos[node] = (i, -level)
    #afer
    for node, level in levels.items():
        G.nodes[node]["layer"] = level

    #---
    return pos

edges = [
    ("QuestionNode", "Planner"),
    ("QuestionNode", "Reader"),
    ("QuestionNode", "Verifier"),
    ("Planner", "Reader"),
    ("Planner", "Solver"),
    ("Reader", "Solver"),
    ("Solver", "Verifier"),
    ("Verifier", "SinkNode"),
]

G = nx.DiGraph()
G.add_edges_from(edges)

fig, ax = plt.subplots(figsize=(8, 6))

#before
# pos = dag_layout(G)
#after

pos = nx.multipartite_layout(
    G,
    subset_key="layer"
)
#---
nx.draw(
    G,
    pos,
    with_labels=True,
    arrows=True,
    connectionstyle="arc3,rad=0.1",
    node_size=2000,
    ax=ax
)

st.pyplot(fig)