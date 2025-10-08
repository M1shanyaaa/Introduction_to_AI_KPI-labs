import random
import networkx as nx
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


class Create_Graph:
    def __init__(self, n, remove_edges):
        self.n = n
        self.remove_edges = remove_edges
        self.graph = None

        self.generate_graph()

    def generate_graph(
        self,
    ):
        self.graph = nx.grid_2d_graph(self.n, self.n)
        edges = list(self.graph.edges())
        random.shuffle(edges)

        removed = 0
        for u, v in edges:
            if removed >= self.remove_edges:
                break
            self.graph.remove_edge(u, v)
            if not nx.is_connected(self.graph):
                self.graph.add_edge(u, v)
            else:
                removed += 1
        return self.graph

    def visualization(self):
        pos = {node: (node[1], -node[0]) for node in self.graph.nodes()}
        nx.draw(self.graph, pos, node_color="white", edgecolors="black", node_size=200)
        plt.show()


if __name__ == "__main__":
    graph = Create_Graph(5, 13)
    graph.visualization()
    
