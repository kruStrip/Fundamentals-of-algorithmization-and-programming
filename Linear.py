import random

""" Аналитическое значение T = O (n)
Потому что в худшем случае алгоритм последовательно проверяет все элементы массива,
и время выполнения растёт линейно от размера входных данных.
"""

"""Эксперементальные значения:
Массив: [21, 26, 6, 32, 31, 46, 15]
Ищем элемент: 32
Найден на позиции: 3
Количество операций T = 8 

Не отсортированый массив: [41, 5, 37, 2, 45, 1]
Ищем элемент: 41
Найден на позиции: 0
Количество операций T = 2 

Массив отсортированный в обратную сторону: [45, 41, 37, 5, 2, 1]
Ищем элемент: 45
Найден на позиции: 0
Количество операций T = 2 

Массив отсортированный наполовину: [1, 2, 5, 41, 37, 45]
Ищем элемент: 5
Найден на позиции: 2
Количество операций T = 6 

Отсортированный массив: [1, 2, 5, 37, 41, 45]
Ищем элемент: 41
Найден на позиции: 4
Количество операций T = 10 
"""

def linear_search(arr, target):
    T = 0
    for i in range(len(arr)):
        T += 1  
        if arr[i] == target:
            T += 1  
            return i, T
        T += 1  
    T += 1  
    return -1, T

n = random.randint(5, 10)  # размер массива
arr = random.sample(range(1, 50), n)
target = random.choice(arr)  

print("Массив:", arr)
print("Ищем элемент:", target)

index, T = linear_search(arr, target)
print("Найден на позиции:", index)
print("Количество операций T =", T, '\n')

arr_not_sorted = [41, 5, 37, 2, 45, 1]
target = random.choice(arr_not_sorted) 
print("Не отсортированый массив:", arr_not_sorted)
print("Ищем элемент:", target)

result, T = linear_search(arr_not_sorted, target)
print("Найден на позиции:", result)
print("Количество операций T =", T, '\n')

arr_sorted_back = [45, 41, 37, 5, 2, 1]
target = random.choice(arr_sorted_back) 
print("Массив отсортированный в обратную сторону:", arr_sorted_back)
print("Ищем элемент:", target)

result, T = linear_search(arr_sorted_back, target)
print("Найден на позиции:", result)
print("Количество операций T =", T, '\n')

arr_sorted_in_half = [1, 2, 5, 41, 37, 45]
target = random.choice(arr_sorted_in_half) 
print("Массив отсортированный наполовину:", arr_sorted_in_half)
print("Ищем элемент:", target)

result, T = linear_search(arr_sorted_in_half, target)
print("Найден на позиции:", result)
print("Количество операций T =", T, '\n')


arr_sorted = [1, 2, 5, 37, 41, 45]
target = random.choice(arr_sorted) 
print("Отсортированный массив:", arr_sorted)
print("Ищем элемент:", target)

result, T = linear_search(arr_sorted, target)
print("Найден на позиции:", result)
print("Количество операций T =", T, '\n')