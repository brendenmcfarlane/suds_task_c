import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from src.graph_mutator import ORDER, PROMPTS
RESULTS = ["A woman is trying to decide whether it will be quicker to take an airplane or drive herself to a job interview. If she drives herself, the trip will take her 3 hours and 15 minutes. If she takes an airplane, she will first need to drive 10 minutes to the airport, and then wait 20 minutes to board the plane. After that, she will be on the airplane for one-third of the time it would have taken her to drive herself before landing in the destination city. Finally, it will take her an additional 10 minutes to get off the airplane and arrive at her interview site after the plane lands. Given this information, how many minutes faster is it for her to take the airplane?",
          'To determine how much faster the airplane is compared to driving, follow these steps:\n\n### Step 1: Calculate the total time for driving (in minutes)\n*   The driving time is given as 3 hours and 15 minutes.\n*   Convert the 3 hours into minutes: $3 \\times 60 = 180$ minutes.\n*   Add the additional 15 minutes: $180 + 15 = 195$ minutes.\n\n### Step 2: Calculate the individual components of the airplane trip\n*   **Drive to the airport:** 10 minutes.\n*   **Wait time:** 20 minutes.\n*   **Flight time:** This is one-third of the driving time (195 minutes).\n    *   $195 / 3 = 65$ minutes.\n*   **Travel from airport to interview site:** 10 minutes.\n\n### Step 3: Calculate the total time for the airplane trip (in minutes)\n*   Sum the components calculated in Step 2:\n    *   $10 + 20 + 65 + 10 = 105$ minutes.\n\n### Step 4: Calculate the time difference\n*   Subtract the total airplane trip time from the total driving time:\n    *   $195 - 105 = 90$ minutes.\n\n**Final Answer:** Taking the airplane is **90 minutes** faster than driving.',
          'Based on the steps provided, here is the summary of the calculation:\n\n**Step 1: Driving Time**\nThe total time to drive is 3 hours and 15 minutes, which converts to **195 minutes**.\n\n**Step 2 & 3: Airplane Trip Time**\n*   Drive to airport: 10 minutes\n*   Wait time: 20 minutes\n*   Flight time: 65 minutes (1/3 of 195)\n*   Arrival at interview site: 10 minutes\n*   **Total Airplane Time:** 10 + 20 + 65 + 10 = **105 minutes**\n\n**Step 4: Time Difference**\n195 minutes (driving) - 105 minutes (airplane) = 90 minutes.\n\n**Final Answer:** Taking the airplane is **90 minutes** faster than driving.',
          'You have successfully solved the problem! Your calculation is accurate, and the logical steps are clear. \n\nTo summarize your findings:\n\n*   **Total Driving Time:** 195 minutes\n*   **Total Airplane Trip Time:** 105 minutes\n*   **Time Saved:** 90 minutes\n\nTaking the airplane is indeed **90 minutes** (or 1 hour and 30 minutes) faster than driving.',
          '90 minutes']
# Create DAG
G = nx.DiGraph()

G.add_edges_from([
    ("QuestionNode", "Planner"),
    ("QuestionNode", "Reader"),
    ("QuestionNode", "Verifier"),
    ("Planner", "Solver"),
    ("Reader", "Solver"),
    ("Solver", "Verifier"),
    ("Verifier", "SinkNode"),
])

# Place vertices on a circle
pos = nx.circular_layout(G)

fig, ax = plt.subplots(1, 2, figsize=(20, 10))

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=2000,
    ax=ax[0]
)

nx.draw_networkx_labels(
    G,
    pos,
    ax=ax[0]
)

nx.draw_networkx_edges(
    G,
    pos,
    arrows=True,
    arrowstyle="-|>",
    edge_color="gray",
    arrowsize=20,
    min_source_margin=25,
    min_target_margin=20,
    ax=ax[0]
)
H = nx.DiGraph()

H.add_edges_from([
    ("QuestionNode", "Planner"),
    ("QuestionNode", "Reader"),
    ("QuestionNode", "Verifier"),
    ("Planner", "Reader"),
    ("Planner", "Solver"),
    ("Reader", "Solver"),
    ("Solver", "ArthmeticChecker"),
    ("ArthmeticChecker", "Verifier"),
    ("Verifier", "SinkNode"),
])

# Place vertices on a circle
pos = nx.circular_layout(H)


nx.draw_networkx_nodes(
    H,
    pos,
    node_size=2000,
    ax=ax[1]
)

nx.draw_networkx_labels(
    H,
    pos,
    ax=ax[1]
)

nx.draw_networkx_edges(
    H,
    pos,
    edgelist=H.edges(),
    edge_color="gray",
    arrows=True,
    arrowstyle="-|>",
    arrowsize=20,
    min_source_margin=25,
    min_target_margin=20,
    ax=ax[1]
)
nx.draw_networkx_edges(
    H,
    pos,
    edgelist=[("Solver", "ArthmeticChecker"),
    ("ArthmeticChecker", "Verifier")],
    edge_color="blue",
    arrows=True,
    arrowstyle="-|>",
    arrowsize=20,
    min_source_margin=25,
    min_target_margin=20,
    ax=ax[1]
)
nx.draw_networkx_edges(
    H,
    pos,
    edgelist=[("Solver", "Verifier")],
    edge_color="red",
    arrows=True,
    arrowstyle="-|>",
    arrowsize=20,
    min_source_margin=25,
    min_target_margin=20,
    ax=ax[1]
)
ax[0].text(-1.1, 0.9, "Accuracy: 5/5,\nAvg Num Calls: 4,\n Score: 0.92")
ax[1].text(-1, 1, "Accuracy: 5/5,\nAvg Num Calls: 5,\n Score: 0.90")


# ax[1].set_title("Agent Transcript")
# ax[1].set_xticks([])
# ax[1].set_yticks([])
# q_h = 0.975
# i = 47
# j = 97
# k = 149
# l = 198
# m = 251
# n = 302
# o = 353
# p = 402
# q = 500
# r = 600
# ax[1].text(0,q_h, "Q: " + RESULTS[0][:i])
# ax[1].text(0,q_h- 0.02, RESULTS[0][i:j])
# ax[1].text(0,q_h- 0.04, RESULTS[0][j:k])
# ax[1].text(0,q_h- 0.06, RESULTS[0][k:l])
# ax[1].text(0,q_h- 0.08, RESULTS[0][l:m])
# ax[1].text(0,q_h- 0.10, RESULTS[0][m:n])
# ax[1].text(0,q_h- 0.12, RESULTS[0][n:o])
# ax[1].text(0,q_h- 0.14, RESULTS[0][o:p])

# p_h = 0.8
# ax[1].text(0,p_h, PROMPTS["Planner"][:46])
# ax[1].text(0,p_h - 0.02, PROMPTS["Planner"][47:])
# ax[1].text(0,p_h - 0.04, "P: " + RESULTS[1][:50] + "-")
# ax[1].text(0,p_h - 0.06, RESULTS[1][50:100] + "-")

# r_h = 0.6
# ax[1].text(0,r_h, PROMPTS["Reader"][:49])
# ax[1].text(0,r_h -0.02, PROMPTS["Reader"][50:])
# ax[1].text(0, r_h - 0.04, "R: " + RESULTS[2][:50] + "-")
# ax[1].text(0, r_h - 0.06, RESULTS[2][50:100] + "-")

# s_h = 0.4
# ax[1].text(0, s_h, PROMPTS["Solver"][:43])
# ax[1].text(0, s_h - 0.02, PROMPTS["Solver"][43:])
# ax[1].text(0, s_h - 0.04, "S: " + RESULTS[3][:50])
# ax[1].text(0, s_h - 0.06, RESULTS[3][50:100] + "-")

# v_h = 0.2
# ax[1].text(0, v_h, "V: " + PROMPTS["Verifier"][:45])
# ax[1].text(0, v_h - 0.02, PROMPTS["Verifier"][45:])
# ax[1].text(0, v_h - 0.04, RESULTS[4][:50])
# ax[1].text(0, v_h - 0.06, RESULTS[4][50:100] + "-")

st.pyplot(fig)