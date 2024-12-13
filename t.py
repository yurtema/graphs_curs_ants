from itertools import combinations

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def fast_generate_random_graph(_n):
    weights = np.random.randint(1, 10, (_n, _n))  # веса рёбер

    # Симметризация матрицы, чтобы граф был неориентированным
    _matrix = np.triu(weights)  # оставляем верхний треугольник
    _matrix += _matrix.T - np.diag(_matrix.diagonal())  # симметризация

    _matrix = _matrix.astype(float)

    # Заполняем главную диагональ значениями np.inf
    np.fill_diagonal(_matrix, np.inf)

    return _matrix


def held_karp(graph):
    """
    Реализация алгоритма Хелда-Карпа для точного решения задачи коммивояжера.
    :param graph: Матрица смежности графа.
    :return: Оптимальная длина пути и список рёбер.
    """
    n = len(graph)
    dp = {}  # dp[subset][i] - минимальная стоимость, чтобы попасть в подмножество subset, заканчиваясь в i
    parent = {}

    # Инициализация для подмножеств с одной вершиной
    for i in range(1, n):
        dp[(1 << i, i)] = graph[0][i]
        parent[(1 << i, i)] = 0  # Все подмножества начинаются с 0

    # Итерация по размеру подмножеств
    for subset_size in range(2, n):
        for subset in combinations(range(1, n), subset_size):
            subset_mask = sum(1 << i for i in subset)
            for j in subset:
                prev_mask = subset_mask & ~(1 << j)  # Убираем текущую вершину
                best_cost, best_prev = min(
                    (dp[(prev_mask, k)] + graph[k][j], k)
                    for k in subset if k != j
                )
                dp[(subset_mask, j)] = best_cost
                parent[(subset_mask, j)] = best_prev

    # Завершаем цикл (включаем возврат в 0)
    subset_mask = (1 << n) - 1 - 1  # Все вершины кроме 0
    best_cost, last_node = min(
        (dp[(subset_mask, i)] + graph[i][0], i)
        for i in range(1, n)
    )

    # Восстанавливаем полный путь
    path = []
    current_mask = subset_mask
    current_node = last_node

    while current_node != 0:
        prev_node = parent[(current_mask, current_node)]
        path.append((prev_node, current_node))
        current_mask &= ~(1 << current_node)
        current_node = prev_node

    # Добавляем финальное ребро, замыкая цикл
    path.append((last_node, 0))
    path.reverse()  # Разворачиваем, чтобы путь начинался с вершины 0

    return best_cost, path



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

matr = fast_generate_random_graph(5)
print(matr)
show_graph(matr)
res = held_karp(matr)
print(res[0])
show_graph(matr, res[1])