import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Initialize dual attribution graph
G = nx.MultiDiGraph()

# Define path types
paths = {
    "red": {  # "not true" interpretation
        "nodes": ["QK_origin", "OV_neg", "QK_reflect", "OV_collapse", "QK_stall"],
        "edges": [("QK_origin", "OV_neg"), ("OV_neg", "QK_reflect"), 
                 ("QK_reflect", "OV_collapse"), ("OV_collapse", "QK_stall")],
        "color": "#FF3D61"
    },
    "blue": {  # "false" interpretation
        "nodes": ["QK_origin", "OV_literal", "QK_mirror", "OV_echo", "QK_resolve"],
        "edges": [("QK_origin", "OV_literal"), ("OV_literal", "QK_mirror"),
                 ("QK_mirror", "OV_echo"), ("OV_echo", "QK_resolve")],
        "color": "#00A2FF"
    }
}

# Add nodes with conflict metadata
for path in paths.values():
    for node in path["nodes"]:
        conflict = False
        if node in ["QK_reflect", "QK_mirror"]:
            conflict = True
        G.add_node(node, conflict_zone=conflict)

# Add edges with path data
for color, path in paths.items():
    for edge in path["edges"]:
        G.add_edge(edge[0], edge[1], color=color, path_type=color)

# Add entanglement points
G.add_edge("OV_neg", "QK_mirror", color="#8A2BE2", path_type="entangle")
G.add_edge("OV_literal", "QK_reflect", color="#8A2BE2", path_type="entangle")

# Set up visualization
plt.figure(figsize=(12, 10))
pos = {
    "QK_origin": (0, 0),
    "OV_neg": (1, 0.5),
    "OV_literal": (1, -0.5),
    "QK_reflect": (2, 0.3),
    "QK_mirror": (2, -0.3),
    "OV_collapse": (3, 0.5),
    "OV_echo": (3, -0.3),
    "QK_stall": (4, 0.5),
    "QK_resolve": (4, -0.5)
}

# Draw edges with custom curves
for edge in G.edges(data=True):
    src, tgt, attr = edge
    if attr["path_type"] in ["red", "blue"]:
        # Draw main paths with curvature
        rad = 0.2 if attr["path_type"] == "red" else -0.2
        arrow = plt.Arrow(pos[src][0], pos[src][1],
                         pos[tgt][0]-pos[src][0], pos[tgt][1]-pos[src][1],
                         width=0.05, color=attr["color"], alpha=0.7)
        plt.gca().add_patch(arrow)
    else:
        # Draw entanglement lines
        plt.plot([pos[src][0], pos[tgt][0]], [pos[src][1], pos[tgt][1]], 
                color=attr["color"], linestyle=":", alpha=0.5)

# Draw nodes with conflict styling
for node in G.nodes():
    if G.nodes[node]["conflict_zone"]:
        # ☍ conflict nodes
        plt.scatter(pos[node][0], pos[node][1], s=1200, marker="$\u262D$", 
                   c="#FFFFFF", edgecolors="#8A2BE2", linewidths=2)
    elif node in ["OV_echo", "OV_collapse"]:
        # 🝚 echo loops
        plt.scatter(pos[node][0], pos[node][1], s=800, marker="$\u1F5DA$", 
                   c="#FFFFFF", edgecolors="#00C389", linewidths=2)
    elif node in ["QK_stall"]:
        # ⧖ collapse zones
        plt.scatter(pos[node][0], pos[node][1], s=1500, marker="$\u29D6$", 
                   c="#FFFFFF", edgecolors="#FF9D00", linewidths=2)
    else:
        # Standard nodes
        plt.scatter(pos[node][0], pos[node][1], s=500, 
                   c="#FFFFFF", edgecolors="#333333", linewidths=2)

# Add path labels
plt.text(1, 0.7, '"not true" path', color="#FF3D61", ha="center")
plt.text(1, -0.7, '"false" path', color="#00A2FF", ha="center")

# Add legend
markers = [
    plt.Line2D([0], [0], marker="$\u262D$", color="w", label='Instruction Conflict (☍)',
              markerfacecolor="w", markeredgecolor="#8A2BE2", markersize=15),
    plt.Line2D([0], [0], marker="$\u1F5DA$", color="w", label='Echo Loop (🝚)',
              markerfacecolor="w", markeredgecolor="#00C389", markersize=15),
    plt.Line2D([0], [0], marker="$\u29D6$", color="w", label='Collapse Zone (⧖)',
              markerfacecolor="w", markeredgecolor="#FF9D00", markersize=15)
]
plt.legend(handles=markers, loc="upper right")

plt.title("QK/OV Bifurcation Graph: Ambiguous Prompt Entanglement", pad=20)
plt.gca().set_facecolor("#F5F5F5")
plt.grid(True, alpha=0.2)
plt.axis("equal")
plt.tight_layout()
plt.show()
