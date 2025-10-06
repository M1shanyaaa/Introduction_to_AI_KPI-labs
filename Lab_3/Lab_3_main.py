import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from Lab_2.Lab_2_main import *


class KnowledgeBase:
    """База знань агента."""

    def __init__(self):
        self.knowledge = {}

    def tell(self, node, neighbors, signs=None):
        if node not in self.knowledge:
            self.knowledge[node] = {"neighbors": set(), "signs": {}}
        self.knowledge[node]["neighbors"].update(neighbors)
        if signs:
            self.knowledge[node]["signs"].update(signs)

    def ask_neighbors(self, node):
        if node in self.knowledge:
            return list(self.knowledge[node]["neighbors"])
        return []

    def ask_signs(self, node):
        if node in self.knowledge:
            return self.knowledge[node]["signs"]
        return {}


class Extended_Agent(Agent):
    """Агент на основі знань з реальним backtracking."""

    def __init__(self, graph, start, goal):
        super().__init__(graph, start, goal)
        self.kb = KnowledgeBase()
        self.full_path = [start]  # повний маршрут (вперед + назад)


    def perceive_and_update(self):
        """Оновлюємо базу знань про сусідів та знаки."""
        neighbors = self.see_neighbors()
        signs = {n: list(self.graph.neighbors(n)) for n in neighbors}
        self.kb.tell(self.position, neighbors, signs)
        print(signs)
    def step(self):
        """Робимо один крок вперед або назад по стеку DFS."""
        self.perceive_and_update()
        known_neighbors = self.kb.ask_neighbors(self.position)
        unvisited = [n for n in known_neighbors if n not in self.visited_nodes]

        if unvisited:
            # рух вперед
            next_node = min(unvisited, key=lambda n: self.heuristic(n))
            self.visited_nodes.add(next_node)
            self.path.append(next_node)
        else:
            # backtracking: крок назад по path
            if len(self.path) > 1:
                self.path.pop()
                next_node = self.path[-1]
            else:
                next_node = self.position  # залишаємося (крайній випадок)

        self.position = next_node
        self.full_path.append(next_node)

    def search(self, max_steps=10000):
        """Пошук з покроковим backtracking."""
        steps = 0
        while self.position != self.goal and steps < max_steps:
            self.step()
            steps += 1
        return self.full_path

    def decide_next(self):
        """Потрібно для сумісності з animate_path."""
        if len(self.full_path) > 1:
            return self.full_path[1]
        return self.position

    def print_knowledge(self):
        print(self.kb.knowledge)
        for node, data in self.kb.knowledge.items():
            print(f"Вузол {node}: сусіди={data['neighbors']}, знаки={data['signs']}")


if __name__ == "__main__":
    from Lab_1.learning import Create_Graph

    # Створюємо граф
    graph_creator = Create_Graph(5, 13)
    start = (0, 0)
    goal = (4, 4)

    agent = Agent(graph_creator, start, goal)
    if agent:
        pass

    print("\n=== Агент на основі знань ===")
    agent2 = Extended_Agent(graph_creator.graph, start, goal)
    path2 = agent2.search()
    print("Шлях KBA:", path2)

    print("\nБаза знань KBA:")
    agent2.print_knowledge()

    # Анімація руху для KBA
    agent2.animate_path(delay=0.5)
