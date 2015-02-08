from collections import namedtuple
from pprint import pprint as pp
 
 
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')
 
class Graph():
    def __init__(self, edges):
        self.edges = edges2 = [Edge(*edge) for edge in edges]
        self.vertices = set(sum(([e.start, e.end] for e in edges2), []))
 
    def dijkstra(self, source, dest):
        assert source in self.vertices
        dist = {vertex: inf for vertex in self.vertices}
        previous = {vertex: None for vertex in self.vertices}
        dist[source] = 0
        q = self.vertices.copy()
        neighbours = {vertex: set() for vertex in self.vertices}
        for start, end, cost in self.edges:
            neighbours[start].add((end, cost))
        #pp(neighbours)
 
        while q:
            u = min(q, key=lambda vertex: dist[vertex])
            q.remove(u)
            if dist[u] == inf or u == dest:
                break
            for v, cost in neighbours[u]:
                alt = dist[u] + cost
                if alt < dist[v]:                                  # Relax (u,v,a)
                    dist[v] = alt
                    previous[v] = u
        #pp(previous)
        s, u = [], dest
        while previous[u]:
            s.insert(0, u)
            u = previous[u]
        s.insert(0, u)
        return s
 
 
#graph = Graph([("a", "b", 7),  ("a", "c", 9),  ("a", "f", 14), ("b", "c", 10),
#               ("b", "d", 15), ("c", "d", 11), ("c", "f", 2),  ("d", "e", 6),
#               ("e", "f", 9)])

graph = Graph([('A0', 'A1', 13), ('A0', 'B1', 9), 
('A0', 'C1', 9), ('A0', 'D1', 3), ('A1', 'A2', 9), 
('A1', 'B1', 16), ('A1', 'B2', 15), ('A1', 'C1', 4), ('A1', 'C2', 3), ('A1', 'D1', 14), 
('A1', 'D2', 17), ('A2', 'B1', 19), ('A2', 'B2', 18), ('A2', 'C1', 7), ('A2', 'C2', 8), 
('A2', 'D1', 17), ('A2', 'D2', 20), ('B1', 'A1', 16), ('B1', 'A2', 19), ('B1', 'B2', 13), 
('B1', 'C1', 12), ('B1', 'C2', 19), ('B1', 'D1', 6), ('B1', 'D2', 13), ('B2', 'A1', 15), 
('B2', 'A2', 18), ('B2', 'C1', 11), ('B2', 'C2', 18), ('B2', 'D1', 7), ('B2', 'D2', 2), 
('C1', 'A1', 4), ('C1', 'A2', 7), ('C1', 'B1', 12), ('C1', 'B2', 11), ('C1', 'C2', 7), 
('C1', 'D1', 10), ('C1', 'D2', 13), ('C2', 'A1', 3), ('C2', 'A2', 8), ('C2', 'B1', 19), 
('C2', 'B2', 18), ('C2', 'D1', 17), ('C2', 'D2', 20), ('D1', 'A1', 14), ('D1', 'A2', 17), 
('D1', 'B1', 6), ('D1', 'B2', 7), ('D1', 'C1', 10), ('D1', 'C2', 17), ('D1', 'D2', 7), 
('D2', 'A1', 17), ('D2', 'A2', 20), ('D2', 'B1', 13), ('D2', 'B2', 2), ('D2', 'C1', 13), ('D2', 'C2', 20)])

pp(graph.dijkstra("A0", "D2"))