import json
from src.config import get_settings
import streamlit as st

settings = get_settings()

def load_graph_data(nodes_path: str, edges_path: str):
    """
    Loads map data from JSON files and constructs an adjacency list representation.

    Returns:
        nodes (dict): Mapping of node_id to its geographical coordinates.
        graph (dict): Adjacency list representing the road network for O(1) lookups.
    """
    with open(nodes_path, 'r', encoding='utf-8') as f:
        nodes = json.load(f)

    with open(edges_path, 'r', encoding='utf-8') as f:
        edges = json.load(f)

    # Initialize an adjacency list for the graph
    graph = {node_id: {} for node_id in nodes.keys()}

    for edge in edges:
        u = str(edge['u'])
        v = str(edge['v'])
        length = float(edge['length'])

        # Build directed graph (u -> v) to respect one-way streets from OSMnx
        if u in graph:
            # If multiple edges exist between u and v, keep the shortest one
            if v in graph[u]:
                graph[u][v] = min(graph[u][v], length)
            else:
                graph[u][v] = length

    return nodes, graph

@st.cache_data
def get_map_data():
    """Load JSON data into RAM to optimize latency."""
    return load_graph_data(settings.NODES_DATA_PATH, settings.EDGES_DATA_PATH)