import streamlit as st
import folium
from streamlit_folium import st_folium
import osmnx as ox

from src.config import get_settings
from src.a_star_algorithm import run_a_star, calculate_haversine
from src.data.load_graph_data import get_map_data

settings = get_settings()
st.set_page_config(page_title="AI Pathfinding", layout="wide")


nodes_data, graph_data = get_map_data()

def get_nearest_node(lat: float, lon: float, nodes: dict) -> str:
    """
    Find nearest node
    Use haversine to calculate distance.
    """
    min_dist = float('inf')
    nearest_node = None

    for node_id, data in nodes.items():
        dist = calculate_haversine(lat, lon, float(data['y']), float(data['x']))
        if dist < min_dist:
            min_dist = dist
            nearest_node = node_id

    return nearest_node


st.title("🗺️ Hệ thống AI Tìm Đường Ngắn Nhất")
st.markdown(f"**Khu vực hoạt động:** {settings.PLACE_NAME}")

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("📍 Nhập địa chỉ")
    st.info("Mẹo: Nhập chi tiết tên đường + Thành phố (VD: Tràng Tiền, Hà Nội) để AI tìm chính xác nhất.")

    start_address = st.text_input("Điểm xuất phát (A):", placeholder="VD: Nhà hát lớn Hà Nội")
    end_address = st.text_input("Điểm đến (B):", placeholder="VD: Chợ Đồng Xuân, Hà Nội")

    find_button = st.button("🚀 Tìm đường đi", use_container_width=True)

with col2:
    first_node = next(iter(nodes_data.values()))
    m = folium.Map(location=[float(first_node['y']), float(first_node['x'])], zoom_start=14)

    if find_button and start_address and end_address:
        with st.spinner("Đang xử lý tọa độ và tính toán bằng AI..."):
            try:
                # Bước 1: Geocoding - Đổi Text thành Tọa độ thực tế
                lat1, lon1 = ox.geocode(start_address)
                lat2, lon2 = ox.geocode(end_address)

                # Bước 2: Map tọa độ thực tế vào Đồ thị (Nearest Node)
                start_id = get_nearest_node(lat1, lon1, nodes_data)
                goal_id = get_nearest_node(lat2, lon2, nodes_data)

                # Bước 3: Chạy thuật toán A*
                path, distance = run_a_star(nodes_data, graph_data, start_id, goal_id)

                if path:
                    st.success(f"✅ Đã tìm thấy đường đi! Tổng khoảng cách: **{distance:.2f} mét**")

                    # Bước 4: Vẽ đường đi lên Folium
                    route_coords = [(float(nodes_data[n]['y']), float(nodes_data[n]['x'])) for n in path]

                    # Marker điểm A và B
                    folium.Marker([lat1, lon1], popup="A (Thực tế)", icon=folium.Icon(color="green")).add_to(m)
                    folium.Marker([lat2, lon2], popup="B (Thực tế)", icon=folium.Icon(color="red")).add_to(m)

                    # Vẽ đường (PolyLine)
                    folium.PolyLine(route_coords, color="#3388ff", weight=6, opacity=0.8).add_to(m)

                    # Zoom bản đồ vừa vặn với đường đi
                    m.fit_bounds(m.get_bounds())
                else:
                    st.error("❌ Không tìm thấy đường đi nối giữa 2 khu vực này trên đồ thị.")

            except Exception as e:
                st.error("⚠️ Lỗi trích xuất địa chỉ. Vui lòng thử nhập tên rõ ràng hơn (VD thêm chữ 'Hà Nội').")
                st.write(f"Chi tiết lỗi hệ thống: {e}")

    # Hiển thị bản đồ lên Web
    st_folium(m, width=800, height=500, returned_objects=[])