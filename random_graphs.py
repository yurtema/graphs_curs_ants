import time
import numpy as np
import random
import networkx as nx
from solve_tsp import AntColony
import matplotlib.pyplot as plt

# --------------------------- Н А С Т Р О Й К И --------------------------- #

NUMBER_OF_GRAPHS_FOR_EACH_N = 10  # На скольки графах запускать алгоритм для каждого количества вершин
MAX_N = 500  # До скольки доводить количество вершин
N_STEP = 5  # Шаг количества вершин
WEIGHTS_RANGE = (1, 100)  # Диапазон из которого выбираются веса

# ------------------------------------------------------------------------- #

np.random.seed(8)


def fast_generate_random_graph(_n):
    # Генерация случайной матрицы плотности
    random_matrix = np.random.rand(_n, _n)
    weights = np.random.randint(*WEIGHTS_RANGE, (_n, _n))  # веса рёбер

    # Применяем веса к рёбрам в соответствии с плотностью
    _matrix = np.where(random_matrix, weights, 0)

    # Симметризация матрицы, чтобы граф был неориентированным
    _matrix = np.triu(_matrix)  # оставляем верхний треугольник
    _matrix += _matrix.T - np.diag(_matrix.diagonal())  # симметризация

    _matrix = _matrix.astype(float)

    # Заполняем главную диагональ значениями np.inf
    np.fill_diagonal(_matrix, np.inf)

    return _matrix


def generate_random_graph(_n):
    # n - количество узлов

    _matrix = np.zeros((_n, _n), dtype=int)

    for i in range(_n):
        for j in range(i + 1, _n):
            weight = random.randint(1, 10)
            _matrix[i][j] = weight
            _matrix[j][i] = weight  # для симметрии графа

    return _matrix


def show_graph(_m, red_edges=None):
    _m = np.nan_to_num(_m, posinf=0)
    g = nx.from_numpy_array(_m)
    pos = nx.spring_layout(g, weight='weight', seed=42)

    plt.figure(figsize=(8, 6))

    # Нарисуем все узлы и ребра обычным цветом
    nx.draw(g, pos, with_labels=True, node_color='lightblue', font_weight='bold', width=1)
    nx.draw_networkx_edge_labels(g, pos, edge_labels={(i, j): _m[i, j] for i, j in g.edges})

    # Если есть кратчайший путь, выделим его
    if red_edges:
        nx.draw_networkx_edges(g, pos, edgelist=red_edges, edge_color='red', width=2)

    plt.show()


#
# start = time.time()
#
# for n in range(N_STEP, MAX_N + 1, N_STEP):
#     print(n)
#     for _ in range(0, NUMBER_OF_GRAPHS_FOR_EACH_N):
#         fast_generate_random_graph(max(4, n))
#
# print(time.time()-start)
#
# matrix = fast_generate_random_graph(5)
#
# print(matrix)
#
# shortest_path = AntColony(matrix).run()[0]
# print(shortest_path)
# show_graph(matrix, shortest_path)


# for n in range(N_STEP, MAX_N + 1, N_STEP):
#     start = time.time()
#     for _ in range(0, NUMBER_OF_GRAPHS_FOR_EACH_N):
#         matrix = fast_generate_random_graph(n)
#         AntColony(matrix).run()
#     print(f"Решение для {n} вершин заняло {time.time()-start} секунд")

matrix = fast_generate_random_graph(500)
# print(matrix)
shortest = AntColony(matrix).run()
print("Самый короткий:", shortest[1])
# show_graph(matrix, shortest[0])