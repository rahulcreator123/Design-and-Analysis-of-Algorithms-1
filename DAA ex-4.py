import heapq

# ---------- Dijkstra's Algorithm ----------
def dijkstra(graph, source, n):
    dist = [float('inf')] * n
    prev = [None] * n

    dist[source] = 0
    pq = [(0, source)]  # (distance, vertex)

    while pq:
        d, u = heapq.heappop(pq)

        # Ignore outdated entries
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
n = int(input("Enter the number of vertices: "))
e = int(input("Enter the number of edges: "))

graph = {i: [] for i in range(n)}

print("\nEnter each edge in the format:")
print("Source Destination Weight")

for i in range(e):
    u, v, w = map(int, input(f"Edge {i+1}: ").split())
    graph[u].append((v, w))      # Directed graph
    # Uncomment the next line for an undirected graph
    # graph[v].append((u, w))

source = int(input("\nEnter the source vertex: "))

# ---------- Run Algorithm ----------
dist, prev = dijkstra(graph, source, n)

# ---------- Display Results ----------
print(f"\nShortest Paths from Vertex {source}")
print("-" * 60)
print("{:<10}{:<12}{}".format("Vertex", "Distance", "Path"))
print("-" * 60)

for v in range(n):
    path = reconstruct_path(prev, source, v)

    if dist[v] == float('inf'):
        distance = "INF"
        path_str = "No Path"
    else:
        distance = dist[v]
        path_str = " -> ".join(map(str, path))

    print("{:<10}{:<12}{}".format(v, distance, path_str))