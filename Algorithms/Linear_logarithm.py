import random

"""Аналитическое значение T = O(log (N))
Потому что на каждом шаге массив делится на две части (log n уровней рекурсии),
и на каждом уровне выполняется линейное количество операций (n).
"""

"""Эксперементальные значения:
Случайный массив: [40, 39, 42, 19, 32, 15, 5, 2, 24]
Отсортированный массив: [2, 5, 15, 19, 24, 32, 39, 40, 42]
Количество операций T = 69 

Не отсортированый массив: [41, 5, 37, 2, 45, 1]
Отсортированный массив: [1, 2, 5, 37, 41, 45]
Количество операций T = 36 

Массив отсортированный в обратную сторону: [45, 41, 37, 5, 2, 1]
Отсортированный массив: [1, 2, 5, 37, 41, 45]
Количество операций T = 36 

Массив отсортированный наполовину: [1, 2, 5, 41, 37, 45]
Отсортированный массив: [1, 2, 5, 37, 41, 45]
Количество операций T = 36 

Отсортированный массив: [1, 2, 5, 37, 41, 45]
Отсортированный массив: [1, 2, 5, 37, 41, 45]
Количество операций T = 36 
"""

def quick_sort(arr, T):
    T += 1
    if len(arr) <= 1:
        T += 2
        return arr, T  # возвращаем КОРТЕЖ (список, T)
    
    T += 1  # else
    pivot = arr[len(arr) // 2]  # Опорный элемент
    T += 1
    left = [x for x in arr if x < pivot]
    T += 1
    middle = [x for x in arr if x == pivot]
    T += 1
    right = [x for x in arr if x > pivot]

    # рекурсивно сортируем левую и правую части
    T += 1
    left_sorted, T = quick_sort(left, T)
    T += 1
    right_sorted, T = quick_sort(right, T)
    
    T += 1
    return left_sorted + middle + right_sorted, T


n = random.randint(5, 10)  # размер массива
arr = random.sample(range(1, 50), n)
T = 0
print("Случайный массив:", arr)
sorted_array, T = quick_sort(arr, T)
print("Отсортированный массив:", sorted_array)
print("Количество операций T =", T, '\n')

arr_not_sorted = [41, 5, 37, 2, 45, 1]
print("Не отсортированый массив:", arr_not_sorted)
T = 0
result, T = quick_sort(arr_not_sorted, T)
print("Отсортированный массив:", result)
print("Количество операций T =", T, '\n')

arr_sorted_back = [45, 41, 37, 5, 2, 1]
print("Массив отсортированный в обратную сторону:", arr_sorted_back)
T = 0
result, T = quick_sort(arr_sorted_back, T)
print("Отсортированный массив:", result)
print("Количество операций T =", T, '\n')

arr_sorted_in_half = [1, 2, 5, 41, 37, 45]
print("Массив отсортированный наполовину:", arr_sorted_in_half)
T = 0
result, T = quick_sort(arr_sorted_in_half, T)
print("Отсортированный массив:", result)
print("Количество операций T =", T, '\n')


arr_sorted = [1, 2, 5, 37, 41, 45]
print("Отсортированный массив:", arr_sorted)
T = 0
result, T = quick_sort(arr_sorted, T)
print("Отсортированный массив:", result)
print("Количество операций T =", T, '\n')