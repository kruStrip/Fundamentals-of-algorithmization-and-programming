import random

def fitness(chromosome):
    # вычисляем значение функции
    binary_string = ''.join(str(gene) for gene in chromosome)
    x = int(binary_string, 2)
    return x ** 2

def create_population(size, length):
    # Создаем случайную популяцию
    return [[random.randint(0, 1) for _ in range(length)] for _ in range(size)]

def select_parents(population, fitnesses, k=3):
    # Селекция (выбираем лучших для размножения)
    selected = []
    for _ in range(2):
        participants = random.sample(list(zip(population, fitnesses)), k)
        selected.append(max(participants, key=lambda x: x[1])[0])
    return selected

def crossover(parent1, parent2, rate):
    # Одноточечный кроссовер (скрещиваем их)
    if random.random() < rate:
        point = random.randint(1, len(parent1) - 1)
        return (
            parent1[:point] + parent2[point:],
            parent2[:point] + parent1[point:]
        )
    return parent1, parent2

def mutate(chromosome, rate):
    # Точечная мутация
    return [gene if random.random() > rate else 1 - gene for gene in chromosome]

def genetic_algorithm(
    generations=100,
    pop_size=50,
    chrom_length=8,
    crossover_rate=0.8,
    mutation_rate=0.1,
    elitism=2
):
    # Инициализация популяции
    population = create_population(pop_size, chrom_length)
    best_solution = None
    best_fitness = 0
    
    for generation in range(generations):
        # Оценка приспособленности
        fitnesses = [fitness(chrom) for chrom in population]
        
        # Обновление лучшего решения
        current_best = max(fitnesses)
        if current_best > best_fitness:
            best_fitness = current_best
            best_solution = population[fitnesses.index(current_best)]
        
        # Формирование новой популяции
        new_population = []
       
       # сохраняем лучших(элитизм)
        elite_indices = sorted(range(len(fitnesses)), 
                              key=lambda i: fitnesses[i], reverse=True)[:elitism]
        new_population.extend([population[i] for i in elite_indices])

        # Заполнение остальной части популяции
        while len(new_population) < pop_size:
            # Селекция
            parents = select_parents(population, fitnesses)
            
            # Кроссовер
            offspring = crossover(*parents, crossover_rate)
            
            # Мутация
            mutated_offspring = [mutate(child, mutation_rate) for child in offspring]
            
            new_population.extend(mutated_offspring[:pop_size - len(new_population)])
        
        population = new_population

        if generation % 10 == 0:
            avg_fitness = sum(fitnesses) / len(fitnesses)
            print(f"Поколение {generation}: Средняя приспособленность = {avg_fitness:.2f}")
    
    # Декодируем))
    best_x = int(''.join(str(gene) for gene in best_solution), 2)
    return best_x, best_fitness

    return best_solution, best_fitness
        

solution, value = genetic_algorithm()
print(f"Лучшее решение: x = {solution}, f(x) = {value}")