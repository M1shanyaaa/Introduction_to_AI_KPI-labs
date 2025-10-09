import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import networkx as nx
from Lab_1.Lab_1_main import Create_Graph


class Agent:
    """Раціональний агент-автомобіль з обмеженим баченням."""

    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.position = start
        self.path = [start]
        self.visited_nodes = {start}
        self.visited_edges = set()

    def see_neighbors(self):
        """Агент бачить тільки сусідів поточного вузла."""
        return list(self.graph.neighbors(self.position))

    def move(self, next_node):
        """Рух агента: зберігаємо пройдений шлях, вузли та дороги."""
        if next_node in self.graph.neighbors(self.position):
            self.visited_edges.add((self.position, next_node))
            self.visited_edges.add((next_node, self.position))
            self.visited_nodes.add(next_node)

            # оновлюємо положення
            self.position = next_node
            self.path.append(next_node)
        else:
            raise ValueError("Не можна рухатися до цієї вершини!")

    def heuristic(self, node):
        """Манхеттенська відстань до цілі (для вибору напрямку)."""
        return abs(node[0] - self.goal[0]) + abs(node[1] - self.goal[1])

    def decide_next(self):
        """Вибір наступного кроку: сусід, найближчий до цілі."""
        neighbors = self.see_neighbors()
        unvisited = [n for n in neighbors if n not in self.visited_nodes]

        if unvisited:
            return min(unvisited, key=lambda n: self.heuristic(n))
        else:
            if len(self.path) > 1:
                return self.path[-2]
            return self.position

    def search(self):
        """Пошук цілі з обмеженим баченням (поступово)."""
        while self.position != self.goal:
            next_node = self.decide_next()
            self.move(next_node)
        return self.path

    def animate_path(self, delay=0.5):
        """Анімація руху агента."""
        pos = {node: (node[1], -node[0]) for node in self.graph.nodes()}

        for i in range(1, len(self.path) + 1):
            plt.clf()
            nx.draw(
                self.graph, pos, node_color="white", edgecolors="black", node_size=300
            )

            nx.draw_networkx_nodes(
                self.graph,
                pos,
                nodelist=[self.start],
                node_color="green",
                node_size=400,
            )
            nx.draw_networkx_nodes(
                self.graph, pos, nodelist=[self.goal], node_color="red", node_size=400
            )

            if i > 1:
                edges = [(self.path[j], self.path[j + 1]) for j in range(i - 1)]
                nx.draw_networkx_edges(
                    self.graph, pos, edgelist=edges, edge_color="orange", width=2
                )

            nx.draw_networkx_nodes(
                self.graph,
                pos,
                nodelist=[self.path[i - 1]],
                node_color="blue",
                node_size=350,
            )

            plt.pause(delay)

        plt.show()


if __name__ == "__main__":
    graph_creator = Create_Graph(5, 13)
    graph_creator.visualization()
    start = (0, 0)
    goal = (4, 4)

    agent = Agent(graph_creator.graph, start, goal)
    final_path = agent.search()
    agent.animate_path(delay=0.4)
