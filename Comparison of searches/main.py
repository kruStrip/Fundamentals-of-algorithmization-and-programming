import random
import time

from Binary_search import binary_search
from Interpolation_search import interpolation_search


def generate_sorted_array(size, low=-1000, high=1000):
    
    # Генерируем массив
    
    arr = [random.randint(low, high) for _ in range(size)]
    arr.sort()
    return arr


def read_int(prompt):
    
    # Запрашиваем целое число
    
    while True:
        s = input(prompt)
        try:
            return int(s)
        except ValueError:
            print("Пожалуйста, введите целое число.")


def search_and_report(arrays, value):

    # Выполняем оба поиска

    for i, arr in enumerate(arrays, start=1):
        b_idx = binary_search(arr, value)
        it_idx = interpolation_search(arr, value)
        print(f"Массив {i}: длина={len(arr)}")
        print(f"  Бинарный поиск: {b_idx if b_idx != -1 else 'не найдено'}")
        print(f"  Интерполяционный поиск: {it_idx if it_idx != -1 else 'не найдено'}")


def benchmark(arrays, value, repeats=5):

    # Сравнивает  время работы 
    
    def time_call(func):
        total = 0.0
        for _ in range(repeats):
            t0 = time.perf_counter()
            func()
            t1 = time.perf_counter()
            total += (t1 - t0)
        return total / repeats

    bin_times = []
    it_times = []

    for arr in arrays:
        bin_avg = time_call(lambda: binary_search(arr, value))
        it_avg = time_call(lambda: interpolation_search(arr, value))
        bin_times.append(bin_avg)
        it_times.append(it_avg)

    bin_mean = sum(bin_times) / len(bin_times)
    it_mean = sum(it_times) / len(it_times)

    print("\nСравнение времени (сек., меньше — быстрее):")
    for i, (bt, it) in enumerate(zip(bin_times, it_times), start=1):
        print(f"  Массив {i}: бинарный={bt:.8f}, интерполяционный={it:.8f}")

    print(f"\nСреднее по массивам: бинарный={bin_mean:.8f}, интерполяционный={it_mean:.8f}")
    faster = "бинарный" if bin_mean < it_mean else "интерполяционный" if it_mean < bin_mean else "одинаково"
    print(f"Итог: быстрее в среднем — {faster}.")


if __name__ == "__main__":
    # Генерация трёх массивов 
    sizes = [50, 5_000, 200_000]
    arrays = [generate_sorted_array(n, -100_000, 100_000) for n in sizes]

    # Вывод массивов 
    print("Сгенерированные массивы:")
    for i, arr in enumerate(arrays, start=1):
        if len(arr) <= 100:
            print(f"Массив {i}:", arr)
        else:
            head = arr[:50]
            tail = arr[-5:]
            print(f"Массив {i}: длина={len(arr)}, первые 50: {head} ... последние 5: {tail}")

    # Ввод искомого значения
    value = read_int("\nВведите искомое число: ")

    # Поиск и результаты
    print("")
    search_and_report(arrays, value)

    # Сравнение скорости
    benchmark(arrays, value, repeats=7)


