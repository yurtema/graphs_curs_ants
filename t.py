import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def show_weighted_graph(_m, shortest_path_edges=None):
    # Преобразуем `np.nan` в 0 для несуществующих ребер
    _m = np.nan_to_num(_m, posinf=0)

    # Создаем граф из матрицы смежности
    g = nx.from_numpy_array(_m)

    # Применяем веса для раскладки
    pos = nx.drawing.nx_agraph.graphviz_layout(g)

    plt.figure(figsize=(8, 6))

    # Рисуем узлы и ребра
    nx.draw(g, pos, with_labels=True, node_color='lightblue', font_weight='bold')
    nx.draw_networkx_edge_labels(
        g, pos, edge_labels={(i, j): f'{_m[i, j]:.1f}' for i, j in g.edges if _m[i, j] > 0}
    )

    # Если передан кратчайший путь, выделяем его
    if shortest_path_edges:
        nx.draw_networkx_edges(g, pos, edgelist=shortest_path_edges, edge_color='red', width=2)

    plt.show()


# Пример использования:
_m = np.array([
    [0, 2, np.nan, 3, np.nan],
    [2, 0, 4, np.nan, 5],
    [np.nan, 4, 0, 6, np.nan],
    [3, np.nan, 6, 0, 7],
    [np.nan, 5, np.nan, 7, 0]
])
shortest_path = [(0, 3), (3, 1), (1, 4), (4, 2), (2, 0)]

show_weighted_graph(_m, shortest_path_edges=shortest_path)