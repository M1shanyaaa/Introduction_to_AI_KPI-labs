from Lab_2.Lab_2_main import *


class Knowledge_Base:
    def __init__(self):
        self.knowledge_base = {}  # {position: {'neighbors': [], 'signs': {}, 'dead_end': False}}
        self.dead_nodes = set()  # множина мертвих точок

    def tell_kb(self, position, neighbors):
        """Додає інформацію про позицію та її сусідів."""
        if position not in self.knowledge_base:
            self.knowledge_base[position] = {'neighbors': neighbors, 'dead_end': False}
        else:
            # Оновлюємо інформацію, якщо потрібно
            self.knowledge_base[position]['neighbors'] = neighbors


    def mark_dead_end(self, position):
        """Позначає вершину як мертву точку."""
        if position in self.knowledge_base:
            self.knowledge_base[position]['dead_end'] = True
        self.dead_nodes.add(position)

    def ask_unvisited_neighbors(self, position, visited_nodes):
        """Повертає невідвіданих сусідів, які не є мертвими точками."""
        neighbors = [n for n in self.knowledge_base[position]['neighbors'] if n not in visited_nodes and n not in self.dead_nodes]
        return neighbors

    def check_dead_end(self, position, visited_nodes):
        """Перевіряє, чи є поточна позиція мертвою точкою."""
        if position not in self.knowledge_base:
            return False

        # Отримуємо всіх сусідів, які не є мертвими точками
        available_neighbors = [n for n in self.knowledge_base[position]['neighbors'] if n not in self.dead_nodes]

        # Якщо всі сусіди або відвідані, або мертві точки - це мертва точка
        unvisited_available = [n for n in available_neighbors if n not in visited_nodes]

        return len(unvisited_available) == 0


class Extended_Agent(Agent):
    def __init__(self, graph, start, goal):
        super().__init__(graph, start, goal)
        self.knowledge_base = Knowledge_Base()
        self.backtrack_path = []  # шлях для повернення
        self.search()
        print(self.path)

    def perceive_and_update(self):
        """Оновлюємо базу знань про сусідів та знаки."""
        neighbors = self.see_neighbors()
        self.knowledge_base.tell_kb(self.position, neighbors)

        # Перевіряємо, чи стала поточна позиція мертвою точкою
        if self.knowledge_base.check_dead_end(self.position, self.visited_nodes):
            self.knowledge_base.mark_dead_end(self.position)
            return True  # це мертва точка
        return False

    def decide_next(self):
        """Вибір наступного кроку з урахуванням мертвих точок."""
        # Спочатку оновлюємо інформацію про поточну позицію
        is_dead_end = self.perceive_and_update()

        # Шукаємо невідвіданих сусідів, які не є мертвими точками
        unvisited = self.knowledge_base.ask_unvisited_neighbors(self.position, self.visited_nodes)

        if unvisited:
            # Вибираємо найближчого до цілі
            return min(unvisited, key=lambda n: self.heuristic(n))
        else:
            # Якщо немає доступних сусідів - повертаємось
            return self.backtrack()

    def backtrack(self):
        """Повернення назад по пройденому шляху."""
        if len(self.path) > 1:
            # Повертаємось на попередню позицію
            backtrack_node = self.path[-2]

            # Перевіряємо, чи не стала попередня позиція мертвою точкою
            if backtrack_node in self.knowledge_base.dead_nodes:
                # Якщо так, шукаємо інший шлях для повернення
                available_backtrack = [node for node in self.path[:-1] if node not in self.knowledge_base.dead_nodes]
                if available_backtrack:
                    return available_backtrack[-1]
            return backtrack_node


    def search(self):
        """Пошук цілі з обмеженим баченням та запам'ятовуванням мертвих точок."""
        # Спочатку додаємо інформацію про стартову позицію
        self.perceive_and_update()

        while self.position != self.goal:
            next_node = self.decide_next()
            self.move(next_node)

        return self.path


if __name__ == "__main__":
    # Створюємо граф
    graph_creator = Create_Graph(5, 13)
    start = (0, 0)
    goal = (4, 4)

    agent = Extended_Agent(graph_creator.graph, start, goal)
    agent.animate_path(delay=0.4)

