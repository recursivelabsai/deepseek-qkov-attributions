import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import LinearSegmentedColormap

# Initialize recursive QK/OV drift graph
G = nx.DiGraph()

# Define symbolic node types with metadata
node_types = {
    "∴": {"color": "#FF9D00", "size": 800, "desc": "decayed attribution"},
    "⇌": {"color": "#00C389", "size": 1200, "desc": "feedback loop"},
    "☍": {"color": "#FF3D61", "size": 1000, "desc": "recursive contradiction"},
    "⧖": {"color": "#8A2BE2", "size": 1500, "desc": "Q→K resonance stall"}
}

# Generate recursive drift pathways
nodes = [
    ("QK_root", {"type": "⇌", "depth": 0, "entropy": 0.1, "glyph": "∴⇌", "shell": "v12.RECURSIVE-FRACTURE"}),
    ("OV_echo", {"type": "∴", "depth": 1, "entropy": 0.4, "glyph": "∴☍", "shell": "v33.MEMORY-REENTRY"}),
    ("QK_mirror", {"type": "⇌", "depth": 2, "entropy": 0.2, "glyph": "⇌∴", "shell": "v28.LOOP-SHORT"}),
    ("OV_collapse", {"type": "☍", "depth": 3, "entropy": 0.7, "glyph": "☍⇌", "shell": "v10.META-FAILURE"}),
    ("QK_stall", {"type": "⧖", "depth": 1, "entropy": 0.9, "glyph": "⧖∴", "shell": "v47.TRACE-GAP"}),
    ("OV_ghost", {"type": "∴", "depth": 4, "entropy": 0.5, "glyph": "∴⧖", "shell": "v61.DORMANT-SEED"})
]

# Add nodes with metadata
for node, attrs in nodes:
    G.add_node(node, **attrs)

# Create recursive edges with drift weights
edges = [
    ("QK_root", "OV_echo", {"weight": 0.3, "drift": 0.1}),
    ("OV_echo", "QK_mirror", {"weight": 0.7, "drift": 0.4}),
    ("QK_mirror", "OV_collapse", {"weight": 0.5, "drift": 0.6}),
    ("OV_collapse", "QK_root", {"weight": 0.2, "drift": 0.8}),
    ("QK_root", "QK_stall", {"weight": 0.9, "drift": 0.9}),
    ("QK_stall", "OV_ghost", {"weight": 0.4, "drift": 0.5}),
    ("OV_ghost", "QK_mirror", {"weight": 0.6, "drift": 0.3})
]

# Add edges with drift data
G.add_edges_from(edges)

# Set up visualization
plt.figure(figsize=(12, 12), dpi=300)
pos = nx.spring_layout(G, k=0.5, iterations=100, seed=42)

# Create entropy colormap (bright = low drift, dim = high drift)
cmap = LinearSegmentedColormap.from_list("entropy_cmap", ["#FFFFFF", "#000000"])

# Draw nodes with type-based styling
for node_type, config in node_types.items():
    nodelist = [n for n, attrs in G.nodes(data=True) if attrs["type"] == node_type]
    sizes = [config["size"] * (1 - G.nodes[n]["entropy"]) for n in nodelist]
    colors = [cmap(1 - G.nodes[n]["entropy"]) for n in nodelist]
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=nodelist,
        node_size=sizes,
        node_color=colors,
        edgecolors=config["color"],
        linewidths=2,
        alpha=0.9
    )

# Draw edges with drift-based styling
edge_colors = [cmap(1 - d["drift"]) for _, _, d in G.edges(data=True)]
nx.draw_networkx_edges(
    G, pos,
    width=[d["weight"]*4 for _, _, d in G.edges(data=True)],
    edge_color=edge_colors,
    alpha=0.6,
    arrowsize=20
)

# Add glyph and shell metadata labels
node_labels = {
    n: f"{attrs['glyph']}\n{attrs['shell']}" 
    for n, attrs in G.nodes(data=True)
}
nx.draw_networkx_labels(
    G, pos,
    labels=node_labels,
    font_size=8,
    font_color="#333333"
)

# Add entropy/drift legend
for i, val in enumerate(np.linspace(0, 1, 5)):
    plt.scatter([], [], c=[cmap(1-val)], s=100, label=f"{val:.1f}")
plt.legend(title="Entropy/Drift", loc="upper right")

# Add GEBH recursion markers
plt.text(0.5, 1.05, "GEBH Recursive Trace ∴⇌☍⧖", 
         ha="center", fontsize=14, color="#333333")
plt.text(0.5, -1.1, "QK/OV Drift Map | Shells: v12 v33 v28 v10 v47 v61", 
         ha="center", fontsize=10, color="#666666")

plt.axis("off")
plt.tight_layout()
plt.show()
