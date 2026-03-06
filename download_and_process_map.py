import osmnx as ox
import json
import os
from src.config import get_settings

settings = get_settings()


def download_and_preprocess_map(place_name, output_dir):
    print(f"Downloading map for {place_name}...")
    g = ox.graph_from_place(place_name, network_type='drive') # Only install drive path
    print(f"Finished downloading! Graph has {len(g.nodes)} nodes and {len(g.edges)} edges.")

    nodes_data = {}
    edges_data = []

    print("Preprocessing map...")
    # Get latitude and longitude
    for node_id, data in g.nodes(data=True):
        nodes_data[node_id] = {
            "y": data['y'],  # get latitude
            "x": data['x']  # get longitude
        }

    # Get edges and path length
    for u, v, key, data in g.edges(keys = True, data = True):
        edges_data.append({
            "u": u,
            "v": v,
            "length": data.get('length', 1.0)  # Fallback is 1.0 meter
        })

    # Save nodes and edges files
    os.makedirs(output_dir, exist_ok=True)
    nodes_path = os.path.join(output_dir, "nodes.json")
    edges_path = os.path.join(output_dir, "edges.json")

    with open(nodes_path, "w", encoding="utf-8") as f:
        json.dump(nodes_data, f)
    with open(edges_path, "w", encoding="utf-8") as f:
        json.dump(edges_data, f)

    print(f"Saved: {nodes_path} and {edges_path}")


if __name__ == "__main__":
    download_and_preprocess_map(settings.PLACE_NAME, settings.DATA_PATH)