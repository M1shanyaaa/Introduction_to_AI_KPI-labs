import random

import matplotlib
import networkx as nx

matplotlib.use("TkAgg")  # або "Qt5Agg", якщо встановлений PyQt5
import matplotlib.pyplot as plt


def generate_graph(n, remove_edges=13):
    graph = nx.grid_2d_graph(n, n)
    edges = list(graph.edges())
    random.shuffle(edges)

    removed = 0
    for u, v in edges:
        if removed >= remove_edges:
            break
        graph.remove_edge(u, v)
        if not nx.is_connected(graph):  # перевіряємо зв’язність
            graph.add_edge(u, v)  # відновлюємо, бо розвалився
        else:
            removed += 1
    return graph


def visualization(graph):
    pos = {node: (node[1], -node[0]) for node in graph.nodes()}
    nx.draw(graph, pos, node_color="white", edgecolors="black", node_size=200)
    plt.show()


graph = generate_graph(5)
visualization(graph)
