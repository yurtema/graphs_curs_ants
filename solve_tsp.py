import numpy as np
from numpy.random import choice as np_choice

# -------------------------------------- Н А С Т Р О Й К И -------------------------------------- #

ITERATIONS = 50
ANTS_AMOUNT = 0.1  # На какое число умножить количество вершин чтобы получить количество муравьев
BEST_ANTS_AMOUNT = 0.5  # Какую долю лучших муравьев брать для откладывания феромона
DECAY = 0.95  # На какое число умножаются все феромоны после каждой итерации
PHEROMONE_WEIGHT = 0.3  # Доля феромона в принятии решения муравьем (доля дистанции будет 1 - PHEROMONE_WEIGHT)


# ----------------------------------------------------------------------------------------------- #


class AntColony:

    def __init__(self, matrix):

        self.distances = matrix
        self.pheromone = np.ones(self.distances.shape) / len(matrix)
        self.all_inds = range(len(matrix))
        self.n_ants = 50
        self.n_best = int(BEST_ANTS_AMOUNT * self.n_ants)
        self.n_iterations = ITERATIONS
        self.decay = DECAY
        temp = 1 / min(PHEROMONE_WEIGHT, 1 - PHEROMONE_WEIGHT)
        self.alpha = PHEROMONE_WEIGHT * temp
        self.beta = (1 - PHEROMONE_WEIGHT) * temp

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            print(shortest_path[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self.pheromone = self.pheromone * self.decay
        return all_time_shortest_path

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))  # going back to where we started
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)

        norm_row = row / row.sum()

        move = np_choice(self.all_inds, 1, p=norm_row)[0]
        return move