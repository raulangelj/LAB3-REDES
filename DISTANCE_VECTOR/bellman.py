class Graph_Bellman:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []
 
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])
 
    def BellmanFord(self, src, dest):
        path = {}
        dist = [float("Inf")] * self.V
        dist[src] = 0
        for i in range(self.V):
            path[i] = (0,0)
 
        for _ in range(self.V - 1):
            for u, v, w in self.graph:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    path[v] = (u, v)
                    # print(u, v, w, 'AQUIII')
 
        for u, v, w in self.graph:
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                print("Graph contains negative weight cycle")
                return

        finished = False
        shortest_path = [dest] 
        og_dest = dest
        while not finished:
            for i in path:
                # print(path[i])
                orgigin, fdest = path[i]
                if dest == fdest:
                    shortest_path.append(orgigin)
                    dest = orgigin
                    # print(orgigin, fdest)
                    # return
                    if orgigin == src:
                        finished = True
                        break
        shortest_path = shortest_path[::-1]
        return shortest_path, dist[og_dest]
 
