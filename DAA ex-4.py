import streamlit as st
import heapq

st.set_page_config(page_title="DAA Experiment 4", layout="centered")

st.title("DAA Experiment 4")
st.subheader("Dijkstra's Shortest Path Algorithm")


# ---------- Dijkstra's Algorithm ----------
def dijkstra(graph, source, n):
    dist = [float('inf')] * n
    prev = [None] * n

    dist[source] = 0
    pq = [(0, source)]

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


# ---------- Reconstruct Shortest Path ----------
def reconstruct_path(prev, source, target):
    path = []

    while target is not None:
        path.append(target)
        target = prev[target]

    path.reverse()

    if path and path[0] == source:
        return path
    return []


# ---------- User Input ----------
st.header("Graph Input")

n = st.number_input("Number of Vertices", min_value=2, step=1)
e = st.number_input("Number of Edges", min_value=1, step=1)

edges = []

st.write("Enter each edge:")

for i in range(int(e)):
    c1, c2, c3 = st.columns(3)

    with c1:
        u = st.number_input(
            f"Source {i+1}",
            min_value=0,
            max_value=int(n)-1,
            key=f"u{i}"
        )

    with c2:
        v = st.number_input(
            f"Destination {i+1}",
            min_value=0,
            max_value=int(n)-1,
            key=f"v{i}"
        )

    with c3:
        w = st.number_input(
            f"Weight {i+1}",
            min_value=1,
            step=1,
            key=f"w{i}"
        )

    edges.append((int(u), int(v), int(w)))

source = st.number_input(
    "Source Vertex",
    min_value=0,
    max_value=int(n)-1,
    step=1
)

if st.button("Run Dijkstra"):

    graph = {i: [] for i in range(int(n))}

    for u, v, w in edges:
        graph[u].append((v, w))

    dist, prev = dijkstra(graph, int(source), int(n))

    st.success(f"Shortest Paths from Vertex {source}")

    result = []

    for v in range(int(n)):
        path = reconstruct_path(prev, int(source), v)

        if dist[v] == float('inf'):
            distance = "INF"
            path_str = "No Path"
        else:
            distance = dist[v]
            path_str = " -> ".join(map(str, path))

        result.append({
            "Vertex": v,
            "Distance": distance,
            "Path": path_str
        })

    st.table(result)_str))
