import time
import numpy as np
import random
import networkx as nx
from solve_tsp import AntColony
import matplotlib.pyplot as plt

# --------------------------- Н А С Т Р О Й К И --------------------------- #

NUMBER_OF_GRAPHS_FOR_EACH_N = 3  # На скольки графах запускать алгоритм для каждого количества вершин
MAX_N = 500  # До скольки доводить количество вершин
N_STEP = 5  # Шаг количества вершин
WEIGHTS_RANGE = (1, 100)  # Диапазон из которого выбираются веса 143 309 518

# ------------------------------------------------------------------------- #

np.random.seed(8)


def fast_generate_random_graph(_n):
    weights = np.random.randint(*WEIGHTS_RANGE, (_n, _n))  # веса рёбер

    # Симметризация матрицы, чтобы граф был неориентированным
    _matrix = np.triu(weights)  # оставляем верхний треугольник
    _matrix += _matrix.T - np.diag(_matrix.diagonal())  # симметризация

    _matrix = _matrix.astype(float)

    # Заполняем главную диагональ значениями np.inf
    np.fill_diagonal(_matrix, np.inf)

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


matrix = fast_generate_random_graph(10)
shortest = AntColony(matrix).run()
show_graph(matrix, shortest[0])


for n in range(max(N_STEP, 4), MAX_N + 1, N_STEP):
    start = time.time()
    for _ in range(0, NUMBER_OF_GRAPHS_FOR_EACH_N):
        matrix = fast_generate_random_graph(n)
        AntColony(matrix).run()
    print(f"{n} \t {str((time.time() - start) / NUMBER_OF_GRAPHS_FOR_EACH_N).replace(".", ",")}")



