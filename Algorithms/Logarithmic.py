import random

""" Аналитическое значение T = O(log n)
Потому что на каждом шаге массив делится пополам, 
и количество операций растёт пропорционально логарифму от размера входных данных.
"""

"""Эксперементальные значения:
Массив: [8, 13, 19, 20, 26, 27, 51, 78]
Ищем элемент: 51
Найден на позиции: 6
Количество операций T = 10 

Не отсортированый массив: [41, 5, 37, 2, 45, 1]
Ищем элемент: 5
Найден на позиции: -1
Количество операций T = 7 

Массив отсортированный в обратную сторону: [45, 41, 37, 5, 2, 1]
Ищем элемент: 2
Найден на позиции: -1
Количество операций T = 7 

Массив отсортированный наполовину: [1, 2, 5, 41, 37, 45]
Ищем элемент: 41
Найден на позиции: -1
Количество операций T = 10 

Отсортированный массив: [1, 2, 5, 37, 41, 45]
Ищем элемент: 37
Найден на позиции: 3
Количество операций T = 10 
"""


def binary_search(arr, target):

    T = 0
    T += 1
    left, right = 0, len(arr) - 1

    while left <= right:
        T += 1
        T += 1
        mid = (left + right) // 2
        if arr[mid] == target:
            T += 1
            return mid, T
        elif arr[mid] < target:
            T += 1
            left = mid + 1
        else:
            T += 1
            right = mid - 1

    return -1, T


n = random.randint(8, 12)  # размер массива
arr = sorted(random.sample(range(1, 100), n))
target = random.choice(arr) 

print("Массив:", arr)
print("Ищем элемент:", target)

index, T = binary_search(arr, target)
print("Найден на позиции:", index)
print("Количество операций T =", T, '\n')

arr_not_sorted = [41, 5, 37, 2, 45, 1]
target = random.choice(arr_not_sorted) 
print("Не отсортированый массив:", arr_not_sorted)
print("Ищем элемент:", target)

result, T = binary_search(arr_not_sorted, target)
print("Найден на позиции:", result)
print("Количество операций T =", T, '\n')

arr_sorted_back = [45, 41, 37, 5, 2, 1]
target = random.choice(arr_sorted_back) 
print("Массив отсортированный в обратную сторону:", arr_sorted_back)
print("Ищем элемент:", target)

result, T = binary_search(arr_sorted_back, target)
print("Найден на позиции:", result)
print("Количество операций T =", T, '\n')

arr_sorted_in_half = [1, 2, 5, 41, 37, 45]
target = random.choice(arr_sorted_in_half) 
print("Массив отсортированный наполовину:", arr_sorted_in_half)
print("Ищем элемент:", target)

result, T = binary_search(arr_sorted_in_half, target)
print("Найден на позиции:", result)
print("Количество операций T =", T, '\n')


arr_sorted = [1, 2, 5, 37, 41, 45]
target = random.choice(arr_sorted) 
print("Отсортированный массив:", arr_sorted)
print("Ищем элемент:", target)

result, T = binary_search(arr_sorted, target)
print("Найден на позиции:", result)
print("Количество операций T =", T, '\n')