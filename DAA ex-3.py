import heapq

# ---------- Union-Find (Disjoint Set) for Kruskal ----------
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path Compression
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx

        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True


# ---------- Kruskal's Algorithm ----------
def kruskal(n, edges):
    edges.sort()

    uf = UnionFind(n)
    mst = []
    cost = 0

    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w

            if len(mst) == n - 1:
                break

    return mst, cost


# ---------- Prim's Algorithm ----------
def prim(n, adj, start=0):
    INF = float('inf')

    key = [INF] * n
    parent = [-1] * n
    inMST = [False] * n

    key[start] = 0
    pq = [(0, start)]

    mst = []
    cost = 0

    while pq:
        w, u = heapq.heappop(pq)

        if inMST[u]:
            continue

        inMST[u] = True

        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w

        for v, wt in adj.get(u, []):
            if not inMST[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))

    return mst, cost


# ---------- User Input ----------
n = int(input("Enter the number of vertices: "))
e = int(input("Enter the number of edges: "))

edges = []
adj = {}

print("\nEnter each edge in the format:")
print("Source Destination Weight")

for i in range(e):
    u, v, w = map(int, input(f"Edge {i+1}: ").split())

    edges.append((w, u, v))

    adj.setdefault(u, []).append((v, w))
    adj.setdefault(v, []).append((u, w))


# ---------- Run Algorithms ----------
k_mst, k_cost = kruskal(n, edges[:])
p_mst, p_cost = prim(n, adj)


# ---------- Display Results ----------
print("\n=== Kruskal's Minimum Spanning Tree ===")
for u, v, w in k_mst:
    print(f"Edge ({u} - {v})  Weight = {w}")
print("Total MST Cost =", k_cost)

print("\n=== Prim's Minimum Spanning Tree ===")
for u, v, w in p_mst:
    print(f"Edge ({u} - {v})  Weight = {w}")
print("Total MST Cost =", p_cost)
