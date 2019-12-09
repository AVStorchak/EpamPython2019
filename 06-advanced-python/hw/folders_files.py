class PrintableFolder:
    graph = {}

    def __init__(self, name, content):
        self.name = name
        self.content = content
        try:
            self.graph[name] = [i.name for i in self.content]
            for i in self.content:
                if isinstance(i, PrintableFile):
                    self.graph[i.name] = []
            self.all_nodes = self.go_dfs(self.graph, name)
        except TypeError:
            print('The content must be passed as a tuple')

    def go_dfs(self, graph, start):
        stack, path = [start], []
        while stack:
            node = stack.pop()
            if node in path:
                continue
            path.append(node)
            for neighbor in graph[node]:
                stack.append(neighbor)
        return path

    def __str__(self):
        def find_path(graph, start, end, path=[]):
            path = path + [start]
            if start == end:
                return path
            if start not in graph:
                return None
            for node in graph[start]:
                if node not in path:
                    newpath = find_path(graph, node, end, path)
                    if newpath:
                        return newpath
            return None

        def pretty_view(i):
            view = ''
            distance = len(find_path(self.graph, self.name, i)) - 2
            if isinstance(globals()[i], PrintableFolder):
                view += '\n' + '|   '*distance + '|-> V ' + i
            else:
                view += '\n' + '|   '*distance + '|-> ' + i
            return view

        out = self.name

        for i in self.all_nodes[1:]:
            out += pretty_view(i)
        return out

    def __contains__(self, other):
        return other.name in iter(self.all_nodes)


class PrintableFile:
    def __init__(self, name):
        self.name = name
        self.content = 0

    def __str__(self):
        return self.name
