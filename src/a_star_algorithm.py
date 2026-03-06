import math
import heapq

def calculate_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the great-circle distance between two points on Earth using the Haversine formula.
    This serves as the Heuristic function (h-score) for the A* algorithm.
    """
    r = 6371000  # Earth's radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def run_a_star(nodes: dict, graph: dict, start_id: str, goal_id: str):
    """
    Executes the A* pathfinding algorithm to find the optimal route.

    Returns:
        path (list): Sequence of node IDs forming the shortest path.
        total_distance (float): Total physical length of the path in meters.
    """
    if start_id not in nodes or goal_id not in nodes:
        print("Error: Start or Goal node not found in the dataset.")
        return None, 0.0

    goal_lat = float(nodes[goal_id]['y'])
    goal_lon = float(nodes[goal_id]['x'])

    # Priority Queue stores tuples of (f_score, node_id)
    open_set = [(0.0, start_id)]

    # g_scores: The exact cost from the start node to the current node
    g_scores = {start_id: 0.0}

    # came_from: Tracks the path for reconstruction
    came_from = {}

    while open_set:
        # 1. Pop the node with the lowest expected total cost (f_score)
        current_f, current_node = heapq.heappop(open_set)

        # 2. Check if the goal is reached
        if current_node == goal_id:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start_id)
            # Reverse the path to get start -> goal
            return path[::-1], g_scores[goal_id]

        # 3. Explore neighbors
        for neighbor, distance in graph.get(current_node, {}).items():
            tentative_g = g_scores[current_node] + distance

            # If a cheaper path to this neighbor is found
            if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                came_from[neighbor] = current_node
                g_scores[neighbor] = tentative_g

                # h_score: Estimate distance from neighbor to the goal
                h_score = calculate_haversine(
                    float(nodes[neighbor]['y']), float(nodes[neighbor]['x']),
                    goal_lat, goal_lon
                )

                # f_score = actual cost + estimated future cost
                f_score = tentative_g + h_score
                heapq.heappush(open_set, (f_score, neighbor))

    # Return None if the open set is empty and goal was never reached
    return None, 0.0
