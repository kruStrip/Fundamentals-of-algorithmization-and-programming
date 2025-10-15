import random
import math
import string

BASE_STRING = "the rule is good"
CHARSET = string.ascii_lowercase + ' '
MAX_GENERATIONS = 100

def main():
    random.seed()
    
    # individuals = ["hfksfbnrugdkfnt ", "lfjgntcgasdtrcjd", "pqwlrbc dhfyriem"]
    individuals = generate_rand_individs(16, CHARSET, 100)
    
    print(f" Целевая строка: '{BASE_STRING}'")
    print(f" Длина: {len(BASE_STRING)} символов\n")
    
    population = create_population(individuals)
    
    print(" Начальная популяция:")
    for i, ind in enumerate(population):
        print(f"  {i+1}: '{ind}'")
    print()
    
    generation = 0
    best_distance = math.inf
    best_individ = ""
    
    while generation < MAX_GENERATIONS:
        generation += 1
        
        distance_map = distance_haming(BASE_STRING, population)
        current_bests, current_distance = sort_the_best_individs(distance_map)
        current_best = current_bests[0]
        
        if current_distance < best_distance:
            best_distance = current_distance
            best_individ = current_best
            
        if generation % 100 == 0:
            print(f"Поколение {generation:4d} | Лучшая: '{current_best}' | Расстояние: {current_distance:2d}")
            
        if current_distance == 0:
            print(f"\n Решение найдено за {generation} поколений!")
            print(f"  Результат: '{current_best}'")
            print(f"  Расстояние Хэмминга: {current_distance} (идеально!)")
            return
            
        population = mutation(current_best, CHARSET)
        
    print(f"\n Достигнуто максимальное количество поколений: {MAX_GENERATIONS}")
    print(f" Лучший результат: '{best_individ}'")
    print(f" Расстояние Хэмминга: {best_distance}")

def generate_rand_individs(length, charset, quantity):
    individs = []
    for _ in range(quantity):
        individ = ''.join(random.choice(charset) for _ in range(length))
        individs.append(individ)
    return individs

def create_population(individuals):
    return [ind.lower() for ind in individuals]

def distance_haming(base_string, population):
    table_of_distance = {}
    for individ in population:
        distance = sum(1 for a, b in zip(base_string, individ) if a != b)
        key = distance
        while key in table_of_distance:
            key += 1000
        table_of_distance[key] = individ
    return table_of_distance

def sort_the_best_individs(table_of_distance):
    best_individs = [""] * 2
    min_key = math.inf
    second_min_key = math.inf
    
    for key in table_of_distance:
        real_key = key % 1000
        if real_key < min_key:
            min_key = real_key
            
    for key in table_of_distance:
        real_key = key % 1000
        if real_key == min_key:
            best_individs[0] = table_of_distance[key]
        elif real_key < second_min_key:
            second_min_key = real_key
            
    for key in table_of_distance:
        real_key = key % 1000
        if real_key == second_min_key:
            best_individs[1] = table_of_distance[key]
            break
            
    return best_individs, min_key

def mutation(individual, charset):
    mutants = []
    for _ in range(1000):
        mutant_list = list(individual)
        position = random.randint(0, len(mutant_list)-1)
        mutant_list[position] = random.choice(charset)
        mutants.append(''.join(mutant_list))
    return mutants

if __name__ == "__main__":
    main()