import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import defaultdict, deque
import heapq

def dijkstra(graph, start_node):

    # Инициализация расстояний
    distances = {node: float('infinity') for node in graph}
    distances[start_node] = 0
    previous_nodes = {node: None for node in graph}
    
    # Очередь с приоритетами
    priority_queue = [(0, start_node)]
    
    visited_nodes = []
    steps = []  # Для записи шагов алгоритма
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Если уже нашли более короткий путь - пропускаем
        if current_distance > distances[current_node]:
            continue
            
        visited_nodes.append(current_node)
        
        # Записываем текущее состояние
        steps.append({
            'current_node': current_node,
            'distances': distances.copy(),
            'visited': visited_nodes.copy()
        })
        
        # Обход соседей
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            # Если нашли более короткий путь
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, previous_nodes, steps

def bellman_ford(graph, start_node):

    # Инициализация расстояний
    distances = {node: float('infinity') for node in graph}
    distances[start_node] = 0
    previous_nodes = {node: None for node in graph}
    
    edges = []
    # Создаем список всех ребер
    for node in graph:
        for neighbor, weight in graph[node].items():
            edges.append((node, neighbor, weight))
    
    steps = []
    n = len(graph)
    
    # Основной цикл релаксации
    for i in range(n - 1):
        updated = False
        for u, v, w in edges:
            if distances[u] != float('infinity') and distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                previous_nodes[v] = u
                updated = True
        
        # Записываем состояние после итерации
        steps.append({
            'iteration': i + 1,
            'distances': distances.copy(),
            'updated': updated
        })
        
        if not updated:
            break
    
    # Проверка на отрицательные циклы
    has_negative_cycle = False
    for u, v, w in edges:
        if distances[u] != float('infinity') and distances[u] + w < distances[v]:
            has_negative_cycle = True
            break
    
    return distances, previous_nodes, steps, has_negative_cycle

def visualize_graph(graph, shortest_paths=None, title="Graph Visualization", algorithm_name=""):

    G = nx.DiGraph()
    
    # Добавляем узлы и ребра
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)
    
    plt.figure(figsize=(12, 8))
    
    # Позиционирование узлов
    pos = nx.spring_layout(G, seed=42)  # Фиксируем seed для одинакового расположения
    
    # Рисуем узлы
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='lightblue', 
                          alpha=0.9, linewidths=2, edgecolors='black')
    
    # Рисуем ребра
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True,
                          arrowsize=20, arrowstyle='->', width=2)
    
    # Подписи узлов
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Веса ребер
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    
    # Выделяем кратчайшие пути если они заданы
    if shortest_paths:
        path_edges = []
        for i in range(len(shortest_paths) - 1):
            path_edges.append((shortest_paths[i], shortest_paths[i + 1]))
        
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                              edge_color='red', width=4, arrows=True,
                              arrowsize=25, arrowstyle='->')
        
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_paths,
                              node_color='red', node_size=1000,
                              alpha=0.8, linewidths=3, edgecolors='darkred')
        
        # Добавляем информацию о пути в заголовок
        if algorithm_name:
            path_length = sum(G[u][v]['weight'] for u, v in path_edges)
            title += f"\n{algorithm_name}: {' → '.join(shortest_paths)} (длина: {path_length})"
    
    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def plot_algorithm_comparison(dijkstra_distances, bellman_distances):

    nodes = list(dijkstra_distances.keys())
    dijkstra_values = [dijkstra_distances[node] for node in nodes]
    bellman_values = [bellman_distances[node] for node in nodes]
    
    x = np.arange(len(nodes))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars1 = ax.bar(x - width/2, dijkstra_values, width, label='Алгоритм Дейкстры', 
                   color='skyblue', edgecolor='navy', alpha=0.8)
    bars2 = ax.bar(x + width/2, bellman_values, width, label='Алгоритм Беллмана-Форда', 
                   color='lightcoral', edgecolor='darkred', alpha=0.8)
    
    ax.set_xlabel('Вершины', fontsize=12, fontweight='bold')
    ax.set_ylabel('Кратчайшее расстояние', fontsize=12, fontweight='bold')
    ax.set_title('Сравнение алгоритмов Дейкстры и Беллмана-Форда', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(nodes)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Добавляем подписи значений
    def autolabel(bars):
        for bar in bars:
            height = bar.get_height()
            if height < float('infinity'):
                ax.annotate(f'{height:.1f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom', fontweight='bold')
    
    autolabel(bars1)
    autolabel(bars2)
    
    plt.tight_layout()
    plt.show()

def print_detailed_analysis(dijkstra_results, bellman_results, start_node, target_node):

    print(f"\n{'='*80}")
    print("ДЕТАЛЬНЫЙ АНАЛИЗ РЕЗУЛЬТАТОВ")
    print(f"{'='*80}")
    
    print(f"\n--- АЛГОРИТМ ДЕЙКСТРЫ ---")
    print(f"Количество шагов: {len(dijkstra_results[2])}")
    print(f"Порядок посещения вершин: {dijkstra_results[2][-1]['visited']}")
    print(f"Кратчайший путь до {target_node}: {dijkstra_results[0][target_node]}")
    
    print(f"\n--- АЛГОРИТМ БЕЛЛМАНА-ФОРДА ---")
    print(f"Количество итераций: {len(bellman_results[2])}")
    print(f"Обнаружен отрицательный цикл: {bellman_results[3]}")
    print(f"Кратчайший путь до {target_node}: {bellman_results[0][target_node]}")
    
    print(f"\n--- СРАВНИТЕЛЬНЫЙ АНАЛИЗ ---")
    if dijkstra_results[0][target_node] == bellman_results[0][target_node]:
        print("✅ Оба алгоритма нашли одинаковые кратчайшие расстояния")
    else:
        print("❌ Алгоритмы дали разные результаты")
        
    if bellman_results[3]:
        print("⚠️  Обнаружен отрицательный цикл! Алгоритм Дейкстры может дать некорректные результаты")

# Создаем тестовый граф
test_graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'C': 1, 'D': 5},
    'C': {'D': 8, 'E': 10},
    'D': {'E': 2, 'F': 6},
    'E': {'F': 2},
    'F': {}
}

# Граф с отрицательными весами для демонстрации Беллмана-Форда
graph_with_negative = {
    'A': {'B': 1, 'C': 4},
    'B': {'C': -2, 'D': 5},  # Отрицательный вес
    'C': {'D': 1},
    'D': {'E': -3},  # Отрицательный вес
    'E': {'B': 2},   # Создаем цикл
    'F': {}
}

def main():
    print("=" * 70)
    print("АЛГОРИТМЫ ПОИСКА КРАТЧАЙШИХ ПУТЕЙ: ДЕЙКСТРА И БЕЛЛМАН-ФОРД")
    print("=" * 70)
    
    print("\n1. ВИЗУАЛИЗАЦИЯ ИСХОДНОГО ГРАФА")
    visualize_graph(test_graph, title="Исходный граф (без отрицательных весов)")
    
    start_node = 'A'
    target_node = 'F'
    
    print(f"\n2. ПОИСК КРАТЧАЙШЕГО ПУТИ ОТ {start_node} ДО {target_node}")
    
    print(f"\n--- АЛГОРИТМ ДЕЙКСТРЫ ---")
    dijkstra_distances, dijkstra_previous, dijkstra_steps = dijkstra(test_graph, start_node)
    
    # Восстановление пути для Дейкстры
    path_dijkstra = []
    current = target_node
    while current is not None:
        path_dijkstra.append(current)
        current = dijkstra_previous[current]
    path_dijkstra.reverse()
    
    print(f"Кратчайшие расстояния: {dijkstra_distances}")
    print(f"Кратчайший путь до {target_node}: {' -> '.join(path_dijkstra)}")
    print(f"Длина пути: {dijkstra_distances[target_node]}")
    
    print(f"\n--- АЛГОРИТМ БЕЛЛМАНА-ФОРДА ---")
    bellman_distances, bellman_previous, bellman_steps, has_negative_cycle = bellman_ford(test_graph, start_node)
    
    # Восстановление пути для Беллмана-Форда
    path_bellman = []
    current = target_node
    while current is not None:
        path_bellman.append(current)
        current = bellman_previous[current]
    path_bellman.reverse()
    
    print(f"Кратчайшие расстояния: {bellman_distances}")
    print(f"Кратчайший путь до {target_node}: {' -> '.join(path_bellman)}")
    print(f"Длина пути: {bellman_distances[target_node]}")
    print(f"Обнаружен отрицательный цикл: {has_negative_cycle}")
    
    print(f"\n3. ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ АЛГОРИТМА ДЕЙКСТРЫ")
    visualize_graph(test_graph, path_dijkstra, 
                   f"Алгоритм Дейкстры: путь от {start_node} до {target_node}",
                   "Дейкстра")
    
    print(f"\n4. ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ АЛГОРИТМА БЕЛЛМАНА-ФОРДА")
    visualize_graph(test_graph, path_bellman, 
                   f"Алгоритм Беллмана-Форда: путь от {start_node} до {target_node}",
                   "Беллман-Форд")
    
    print(f"\n5. СРАВНИТЕЛЬНАЯ ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ")
    plot_algorithm_comparison(dijkstra_distances, bellman_distances)
    
    # Детальный анализ
    print_detailed_analysis(
        (dijkstra_distances, dijkstra_previous, dijkstra_steps),
        (bellman_distances, bellman_previous, bellman_steps, has_negative_cycle),
        start_node, target_node
    )
    
    print(f"\n6. ДЕМОНСТРАЦИЯ С ГРАФОМ, СОДЕРЖАЩИМ ОТРИЦАТЕЛЬНЫЕ ВЕСА")
    visualize_graph(graph_with_negative, title="Граф с отрицательными весами")
    
    # Проверяем граф с отрицательными весами
    bellman_neg_distances, bellman_neg_previous, bellman_neg_steps, has_neg_cycle = bellman_ford(graph_with_negative, 'A')
    
    print(f"Результаты Беллмана-Форда для графа с отрицательными весами: {bellman_neg_distances}")
    print(f"Обнаружен отрицательный цикл: {has_neg_cycle}")
    
    # Если нет отрицательного цикла, показываем путь
    if not has_neg_cycle:
        # Выбираем достижимую целевую вершину
        for node in ['D', 'E', 'C']:
            if bellman_neg_distances[node] < float('infinity'):
                path_bellman_neg = []
                current = node
                while current is not None:
                    path_bellman_neg.append(current)
                    current = bellman_neg_previous[current]
                path_bellman_neg.reverse()
                
                print(f"\nКратчайший путь до {node}: {' -> '.join(path_bellman_neg)}")
                visualize_graph(graph_with_negative, path_bellman_neg, 
                               f"Алгоритм Беллмана-Форда (отриц. веса): путь от A до {node}",
                               "Беллман-Форд")
                break


if __name__ == "__main__":
    main()