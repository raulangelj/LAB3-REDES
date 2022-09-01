
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
 
    # The main function that finds shortest distances from src to
    # all other vertices using Bellman-Ford algorithm. The function
    # also detects negative weight cycle
    def BellmanFord(self, src, dest):
        path = {}
        # Step 1: Initialize distances from src to all other vertices
        # as INFINITE
        dist = [float("Inf")] * self.V
        dist[src] = 0
        # llenar el objeto con arreglos vacios para cada vertice
        for i in range(self.V):
            path[i] = (0,0)
 
        # Step 2: Relax all edges |V| - 1 times. A simple shortest
        # path from src to any other vertex can have at-most |V| - 1
        # edges
        for _ in range(self.V - 1):
            # Update dist value and parent index of the adjacent vertices of
            # the picked vertex. Consider only those vertices which are still in
            # queue
            for u, v, w in self.graph:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    path[v] = (u, v)
                    # print(u, v, w, 'AQUIII')
 
        # Step 3: check for negative-weight cycles. The above step
        # guarantees shortest distances if graph doesn't contain
        # negative weight cycle. If we get a shorter path, then there
        # is a cycle.
 
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
 
        # print all distance
        # print('path', path)
        # print('shortest_path', shortest_path)
        # print('Distancia', dist)
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