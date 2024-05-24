from collections import deque

import matplotlib.pyplot as plt
import networkx as nx


class GraphVisualization:
    def __init__(self, num_nodes):
        self.graph = nx.Graph()
        self.pos = {}
        self.num_nodes = num_nodes


    def add_edge(self, u, v):
        self.graph.add_edge(u, v)

    def set_node_positions(self, current, x, y, level, width):
        self.pos[current] = (x, y)
        left = 2 * current + 1
        right = 2 * current + 2
        if left < self.num_nodes:
            self.set_node_positions(left, x - width / (2 ** (level + 1)), y - 1, level + 1, width)
        if right < self.num_nodes:
            self.set_node_positions(right, x + width / (2 ** (level + 1)), y - 1, level + 1, width)

    def draw_graph(self, visited_nodes=None):
        plt.figure(figsize=(10, 8))
        color_map = ['green' if node in visited_nodes else 'white' for node in self.graph.nodes()]
        nx.draw(self.graph, self.pos, with_labels=True, node_color=color_map, node_size=500, font_size=16,
                edge_color='black')
        plt.show()

    def bfs(self, start_node):
        visited = set()
        queue = deque([start_node])
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                self.draw_graph(visited)
                neighbors = set(self.graph[node]) - visited
                queue.extend(neighbors)
        return visited

    def dfs(self, start_node):
        visited = set()
        order = list()
        self._dfs_recursive(start_node, visited, order)
        return order

    def _dfs_recursive(self, node, visited, order):
        visited.add(node)
        order.append(node)
        self.draw_graph(visited)
        neighbors = sorted(set(self.graph[node]) - visited)  # Sortiere Nachbarn nach Knotenindex
        for neighbor in neighbors:
            self._dfs_recursive(neighbor, visited, order)



def create_binary_tree(gv, current, max_nodes):
    left = 2 * current + 1
    right = 2 * current + 2
    if left < max_nodes:
        gv.add_edge(current, left)
        create_binary_tree(gv, left, max_nodes)
    if right < max_nodes:
        gv.add_edge(current, right)
        create_binary_tree(gv, right, max_nodes)


def main():
    num_nodes = 20  # Anzahl der Knoten im Graphen
    gv = GraphVisualization(num_nodes)

    # Binärbaum mit 20 Knoten erstellen
    create_binary_tree(gv, 0, num_nodes)
    gv.set_node_positions(0, 0, 0, 0, 10)  # Root position is (0,0), adjust width for proper spacing

    # Startknoten für BFS
    start_node = 0
    visited = gv.bfs(start_node)
    print(f"Besuchte Knoten in BFS Reihenfolge: {visited}")


if __name__ == "__main__":
    main()