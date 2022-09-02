
# Extraído de https://www.geeksforgeeks.org/bellman-ford-algorithm-dp-23/
class Graph_Bellman:
    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = []
 
    # function to add an edge to graph
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])
 
    # utility function used to print the solution
    def printArr(self, dist):
        print("Vertex Distance from Source")
        for i in range(self.V):
            print("{0}\t\t{1}".format(i, dist[i]))
 
    def BellmanFord(self, src, dest):
        path = {}
        # Step 1: Initialize distances from src to all other vertices
        # as INFINITE
        dist = [float("Inf")] * self.V
        dist[src] = 0
        # llenar el objeto con arreglos vacios para cada vertice
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
        self.printArr(dist)
        return shortest_path, dist[og_dest]
 
 
# Driver's code
if __name__ == '__main__':
    g = Graph_Bellman(5)
    g.addEdge(0, 1, -1)
    g.addEdge(0, 2, 4)
    g.addEdge(1, 2, 3)
    g.addEdge(1, 3, 2)
    g.addEdge(1, 4, 2)
    g.addEdge(3, 2, 5)
    g.addEdge(3, 1, 1)
    g.addEdge(4, 3, -3)
 
    # function call
    g.BellmanFord(0, 2)
 
# Initially, Contributed by Neelam Yadav
# Later On, Edited by Himanshu Garg