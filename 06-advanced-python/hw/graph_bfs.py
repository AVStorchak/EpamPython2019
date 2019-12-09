class Graph:
    def __init__(self, E):
        self.E = E
        self.start = 0
        self.keys = list(E.keys())

    def __iter__(self):
        return self

    def __next__(self):
        if self.start >= len(self.E):
            raise StopIteration
        else:
            self.start += 1
            key = self.keys[self.start-1]
            return key

    def go_bfs(self, start):
        visited = []
        queue = [start]

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.append(node)
                neighbours = self.E[node]

                for neighbour in neighbours:
                    queue.append(neighbour)

        return visited


E = {'A': ['B', 'C', 'D'], 'B': ['C'], 'C': [], 'D': ['A']}
graph = Graph(E)

for vertex in graph:
    print(vertex)
    print(graph.go_bfs(vertex))
