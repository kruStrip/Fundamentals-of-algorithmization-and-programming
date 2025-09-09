import random
import itertools

""" Аналитическое значение T = O(n!)
Потому что время выполнения алгоритма растёт пропорционально числу всех перестановок массива.
"""

"""Эксперементальные значения:
Случайный массив: [5, 18, 19, 30, 42, 36, 33, 44, 35, 29]
Отсортированный массив: [5, 18, 19, 29, 30, 33, 35, 36, 42, 44]
Количество операций T = 8779 

Не отсортированый массив: [41, 5, 37, 2, 45, 1]
Отсортированный массив: [1, 2, 5, 37, 41, 45]
Количество операций T = 1363 

Массив отсортированный в обратную сторону: [45, 41, 37, 5, 2, 1]
Отсортированный массив: [1, 2, 5, 37, 41, 45]
Количество операций T = 1441 

Массив отсортированный наполовину: [1, 2, 5, 41, 37, 45]
Отсортированный массив: [1, 2, 5, 37, 41, 45]
Количество операций T = 7 

Отсортированный массив: [1, 2, 5, 37, 41, 45]
Отсортированный массив: [1, 2, 5, 37, 41, 45]
Количество операций T = 3 
"""

def brute_force_sort(arr):

    T = 0  

    for perm in itertools.permutations(arr):
        T += 1
        if list(perm) == sorted(arr):
            T += 2
            return list(perm), T
        T += 1
    T += 1
    return arr, T


n = random.randint(5, 10)  # размер массива
arr_random = random.sample(range(1, 50), n) 
print("Случайный массив:", arr_random)

result, T = brute_force_sort(arr_random)
print("Отсортированный массив:", result)
print("Количество операций T =", T, '\n')

arr_not_sorted = [41, 5, 37, 2, 45, 1]
print("Не отсортированый массив:", arr_not_sorted)

result, T = brute_force_sort(arr_not_sorted)
print("Отсортированный массив:", result)
print("Количество операций T =", T, '\n')

arr_sorted_back = [45, 41, 37, 5, 2, 1]
print("Массив отсортированный в обратную сторону:", arr_sorted_back)

result, T = brute_force_sort(arr_sorted_back)
print("Отсортированный массив:", result)
print("Количество операций T =", T, '\n')

arr_sorted_in_half = [1, 2, 5, 41, 37, 45]
print("Массив отсортированный наполовину:", arr_sorted_in_half)

result, T = brute_force_sort(arr_sorted_in_half)
print("Отсортированный массив:", result)
print("Количество операций T =", T, '\n')


arr_sorted = [1, 2, 5, 37, 41, 45]
print("Отсортированный массив:", arr_sorted)

result, T = brute_force_sort(arr_sorted)
print("Отсортированный массив:", result)
print("Количество операций T =", T, '\n')