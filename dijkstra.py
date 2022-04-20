from collections import defaultdict


class Graph:
    def __init__(self, edge_list):
        self.graph = defaultdict(list)
        self.edge_list = edge_list
        self.nodes = []

    def show_cities(self):
        for n in self.graph:
            self.nodes.append(n)
        return self.nodes
    
    def build_graph(self):
        seen_edges = defaultdict(int)
        for src, dst, weight in self.edge_list:
            seen_edges[(src, dst, weight)] += 1
            if seen_edges[(src, dst, weight)] > 1:  # checking for duplicated edge entries
                continue
            self.graph[src].append((dst, weight))
            self.graph[dst].append((src, weight))  # remove this line of edge list is directed
        return self.graph

    def dijkstra(self, src, dst=None):

        q = set(self.nodes)
        self.nodes = list(q)
        dist = dict()   # distance to start
        prev = dict()   # previous node in shortest path
        for n in self.nodes:
            dist[n] = float('inf')
            prev[n] = None

        dist[src] = 0

        while q:
            u = min(q, key=dist.get)
            q.remove(u)

            if dst is not None and u == dst:
                return dist[dst], prev

            for v, w in self.graph.get(u, ()):
                newdist = dist[u] + w
                if newdist < dist[v]:
                    dist[v] = newdist
                    prev[v] = u

        return dist, prev
    
    def find_path(self, pr, node):  # generate path list based on parent points 'prev'
        p = []
        while node is not None:
            p.append(node)
            node = pr[node]
        return p[::-1]
    
    def price(self, d):
        if d <= 500:
            return 50000
        if d > 500 and d <= 1000:
            return 100000
        if d > 1000 and d <= 1500:
            return 150000
        if d > 1500 and d <= 2000:
            return 200000
        else:
            return 300000
    
    def priceByDay(self, day, cost):
        d = {
            "Monday" : cost * 1.1,
            "Tuesday" : cost * 1.1,
            "Wednesday" : cost * 1.1,
            "Thursday" : cost * 1.2,
            "Friday" : cost * 1.3,
            "Saturday" : cost * 1.8,
            "Sunday" : cost * 2.0,
        }
        return d[day]

if __name__ == "__main__":

    edges = []
    with open("routes.txt") as fhandle:
        for line in fhandle:
            edge_from, edge_to, cost = line.strip().split(" ")
            edges.append((edge_from, edge_to, int(cost)))

    graph = Graph(edges)

    g = graph.build_graph()

    print("=== Shortest Path ===")

    print("--- All Cities ---")
    cities = graph.show_cities()
    for i in range(len(cities) - 1):
        print("{}. {}".format(i + 1, cities[i]))

    print("--- From What City  To What City ---")
    city_from, city_to = map(str, input().strip().split())
    
    if city_from in g and city_to in g:
        d, prev = graph.dijkstra(city_from, city_to)
        if d == float('inf'):
            print("There is no possible routes from {} -> {}".format(city_from, city_to))
        else:
            path = graph.find_path(prev, city_to)
            cost = graph.price(d)
            print("{} -> {}: distance = {}, path = {}".format(city_from, city_to, d, path))
            day = str(input("The day you would like to go: "))
            print("The cost to your destination: " + str(graph.priceByDay(day, cost)))

    else:
        print("{} or {} is not in Kazakhtan".format(city_from, city_to))

    print("--- From What Point To All Destinations ---")
    city_from = str(input().strip())
    ds, prev = graph.dijkstra(city_from)
    for k in ds:
        path = graph.find_path(prev, k)
        print("{} -> {}: distance = {}, path = {}".format(city_from,k, ds[k], path))



        

