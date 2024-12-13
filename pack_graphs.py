import pickle
import json
import os
import time
from itertools import combinations

import networkx as nx
import numpy as np

import solve_tsp

NUMBER_OF_GRAPHS_FOR_EACH_N = 1  # На скольки графах запускать алгоритм для каждого количества вершин
MAX_N = 500  # До скольки доводить количество вершин
N_STEP = 2  # Шаг количества вершин
WEIGHTS_RANGE = (1, 100)  # Диапазон из которого выбираются веса

RESULTS_FILE = "results.json"  # Файл для сохранения результатов


def fast_generate_random_graph(_n):
    weights = np.random.randint(*WEIGHTS_RANGE, (_n, _n))  # веса рёбер

    # Симметризация матрицы, чтобы граф был неориентированным
    _matrix = np.triu(weights)  # оставляем верхний треугольник
    _matrix += _matrix.T - np.diag(_matrix.diagonal())  # симметризация

    _matrix = _matrix.astype(float)

    # Заполняем главную диагональ значениями np.inf
    np.fill_diagonal(_matrix, np.inf)

    return _matrix


def save_result(result):
    """Добавляет новую запись в JSON-файл."""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                data = {}
    else:
        data = {}
    data.update(result)
    with open(RESULTS_FILE, "w") as f:
        json.dump(data, f, indent=4)



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


if not os.path.exists("graphs"):
    os.makedirs("graphs")

for n in range(max(N_STEP, 4), MAX_N + 1, N_STEP):
    for i in range(NUMBER_OF_GRAPHS_FOR_EACH_N):
        matrix = fast_generate_random_graph(n)
        graph_file = f"graphs/{n}_{i}.pkl"
        with open(graph_file, "wb") as file:
            pickle.dump(matrix, file)

        # Решаем задачу коммивояжера
        try:
            print(f"Решаю задачу для {n} вершин...")
            t = time.time()
            tsp_length = held_karp(matrix)[0]
            hld = time.time() - t
            t = time.time()
            ants = solve_tsp.AntColony(matrix).run()[1]
            nts = time.time() - t
            print(f"Идеальный за {hld}, муравьи за {nts}")
            if tsp_length < ants:
                print(f"{(ants-tsp_length)/ants*100}%")
        except MemoryError:
            print(f"Пропущен граф {n}_{i} из-за недостатка памяти.")
            continue

        # Сохраняем результат
        result = {f"{n}_{i}":{"graph_id": i, "tsp_length": tsp_length}}
        save_result(result)
