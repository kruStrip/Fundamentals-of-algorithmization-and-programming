import random
import numpy as np

# Данные: матрица расстояний между 5 городами
distances = [
    [0, 12, 10, 19, 8],
    [12, 0, 3, 7, 6],
    [10, 3, 0, 2, 20],
    [19, 7, 2, 0, 4],
    [8, 6, 20, 4, 0]
]
n_cities = len(distances)

# Параметры ГА
POP_SIZE = 50
GENERATIONS = 200
MUTATION_RATE = 0.1

# 1. Функция приспособленности
def fitness(route):
    total_distance = 0
    for i in range(len(route)):
        total_distance += distances[route[i]][route[(i+1) % n_cities]]
    return 1 / total_distance

# 2. Создание начальной популяции
def create_population():
    return [random.sample(range(n_cities), n_cities) for _ in range(POP_SIZE)]

# 3. Турнирная селекция
def select(population, k=3):
    selected = random.sample(population, k)
    return max(selected, key=fitness)

# 4. PMX-кроссинговер
def pmx_crossover(parent1, parent2):
    size = len(parent1)
    cx1, cx2 = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[cx1:cx2+1] = parent1[cx1:cx2+1]
    
    for i in range(cx1, cx2+1):
        if parent2[i] not in child:
            j = i
            while child[j] is not None:
                j = parent2.index(parent1[j])
            child[j] = parent2[i]
    
    for i in range(size):
        if child[i] is None:
            child[i] = parent2[i]
    return child

# 5. Мутация (обмен двух городов)
def mutate(route):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

# 6. Основной цикл ГА
population = create_population()
best_route = None
best_fitness = 0

for gen in range(GENERATIONS):
    new_population = []
    for _ in range(POP_SIZE):
        parent1 = select(population)
        parent2 = select(population)
        child = pmx_crossover(parent1, parent2)
        child = mutate(child)
        new_population.append(child)
        
        # Обновляем лучшее решение
        child_fitness = fitness(child)
        if child_fitness > best_fitness:
            best_fitness = child_fitness
            best_route = child[:]
    
    population = new_population
    if gen % 20 == 0:
        print(f"Поколение {gen}: Лучшая длина = {1 / best_fitness:.2f}")

print("Лучший маршрут:", best_route)
print("Длина маршрута:", 1 / best_fitness)