import osmnx as ox
import json
import os


def download_and_preprocess_map(place_name, output_dir="data"):
    print(f"[*] Đang tải dữ liệu bản đồ cho: {place_name}...")
    # Tối ưu 1: Chỉ lấy mạng lưới đường giao thông (không lấy đường sắt, đường đi bộ rườm rà)
    G = ox.graph_from_place(place_name, network_type='drive')
    print(f"[+] Đã tải xong! Đồ thị có {len(G.nodes)} đỉnh và {len(G.edges)} cạnh.")

    nodes_data = {}
    edges_data = []

    print("[*] Đang tiền xử lý Nodes và Edges...")
    # Tối ưu 2: Trích xuất Nodes (Chỉ giữ lại tọa độ y: latitude, x: longitude)
    for node_id, data in G.nodes(data=True):
        nodes_data[node_id] = {
            "y": data['y'],  # Vĩ độ
            "x": data['x']  # Kinh độ
        }

    # Tối ưu 3: Trích xuất Edges (Chỉ giữ điểm đầu u, điểm cuối v, và trọng số length)
    for u, v, key, data in G.edges(keys=True, data=True):
        # Trọng số của thuật toán tìm đường chính là chiều dài đoạn đường (length)
        edges_data.append({
            "u": u,
            "v": v,
            "length": data.get('length', 1.0)  # Fallback là 1.0 nếu mất data
        })

    # Tạo thư mục data nếu chưa có
    os.makedirs(output_dir, exist_ok=True)

    # Lưu ra file JSON
    nodes_path = os.path.join(output_dir, "nodes.json")
    edges_path = os.path.join(output_dir, "edges.json")

    with open(nodes_path, "w", encoding="utf-8") as f:
        json.dump(nodes_data, f)

    with open(edges_path, "w", encoding="utf-8") as f:
        json.dump(edges_data, f)

    print(f"[+] Hoàn tất! Đã lưu dữ liệu tại: {nodes_path} và {edges_path}")


if __name__ == "__main__":
    # Điền tên khu vực bạn muốn test. Khuyên dùng khu vực nhỏ trước để test thuật toán cho lẹ.
    PLACE_NAME = "Hoan Kiem, Hanoi, Vietnam"
    download_and_preprocess_map(PLACE_NAME)