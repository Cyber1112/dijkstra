from collections import defaultdict

def build_graph(edge_list):
    graph = defaultdict(list)
    seen_edges = defaultdict(int)
    for src, dst, weight in edge_list:
        seen_edges[(src, dst, weight)] += 1
        if seen_edges[(src, dst, weight)] > 1:  # checking for duplicated edge entries
            continue
        graph[src].append((dst, weight))
        graph[dst].append((src, weight))  # remove this line of edge list is directed
    return graph


def dijkstra(graph, src, dst=None):
    nodes = []
    for n in graph:
        nodes.append(n)
        nodes += [x[0] for x in graph[n]]

    q = set(nodes)
    nodes = list(q)
    dist = dict()
    prev = dict()
    for n in nodes:
        dist[n] = float('inf')
        prev[n] = None

    dist[src] = 0

    while q:
        u = min(q, key=dist.get)
        q.remove(u)

        if dst is not None and u == dst:
            return dist[dst], prev

        for v, w in graph.get(u, ()):
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev


def find_path(pr, node):  # generate path list based on parent points 'prev'
    p = []
    while node is not None:
        p.append(node)
        node = pr[node]
    return p[::-1]


if __name__ == "__main__":

    edges = []
    with open("routes.txt") as fhandle:
        for line in fhandle:
            edge_from, edge_to, cost = line.strip().split(" ")
            edges.append((edge_from, edge_to, int(cost)))
    print(edges)

    g = build_graph(edges)

    print("=== Shortest Path ===")

    print("--- From What City  To What City ---")
    city_from, city_to = map(str, input().strip().split())

    d, prev = dijkstra(g, city_from, city_to)
    path = find_path(prev, city_to)
    print("{} -> {}: distance = {}, path = {}".format(city_from, city_to, d, path))

    print("--- From What Point To All Destinations ---")
    city_from = str(input().strip())
    ds, prev = dijkstra(g, city_from)
    for k in ds:
        path = find_path(prev, k)
        print("{} -> {}: distance = {}, path = {}".format(city_from,k, ds[k], path))

