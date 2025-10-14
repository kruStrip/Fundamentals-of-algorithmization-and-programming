import time
import random
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

class StringSearchAlgorithms:
    """Класс для реализации и сравнения алгоритмов поиска подстрок"""
    
    def __init__(self):
        self.comparison_count = 0
    
    def reset_counter(self):
        self.comparison_count = 0
    
    # 1. Наивный алгоритм
    def naive_search(self, text, pattern):
        """Наивный алгоритм поиска подстроки"""
        self.reset_counter()
        n = len(text)
        m = len(pattern)
        
        for i in range(n - m + 1):
            j = 0
            while j < m:
                self.comparison_count += 1
                if text[i + j] != pattern[j]:
                    break
                j += 1
            if j == m:
                return i, self.comparison_count
        return -1, self.comparison_count
    
    # 2. Алгоритм Рабина-Карпа
    def rabin_karp_search(self, text, pattern, q=101):
        """Алгоритм Рабина-Карпа"""
        self.reset_counter()
        n = len(text)
        m = len(pattern)
        d = 256  # размер алфавита
        
        # Вычисление хеша для pattern и первого окна text
        h = 1
        for i in range(m-1):
            h = (h * d) % q
        
        pattern_hash = 0
        text_hash = 0
        
        for i in range(m):
            pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
            text_hash = (d * text_hash + ord(text[i])) % q
        
        # Поиск
        for i in range(n - m + 1):
            self.comparison_count += 1
            if pattern_hash == text_hash:
                # Проверка на коллизию
                for j in range(m):
                    self.comparison_count += 1
                    if text[i + j] != pattern[j]:
                        break
                else:
                    return i, self.comparison_count
            
            if i < n - m:
                text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % q
                if text_hash < 0:
                    text_hash += q
        
        return -1, self.comparison_count
    
    # 3. Алгоритм Бойера-Мура (упрощенная версия)
    def boyer_moore_search(self, text, pattern):
        """Алгоритм Бойера-Мура с правилом плохого символа"""
        self.reset_counter()
        n = len(text)
        m = len(pattern)
        
        # Таблица плохого символа
        bad_char = {}
        for i in range(m):
            bad_char[pattern[i]] = i
        
        i = 0
        while i <= n - m:
            j = m - 1
            # Сравнение с конца
            while j >= 0:
                self.comparison_count += 1
                if pattern[j] != text[i + j]:
                    break
                j -= 1
            
            if j < 0:
                return i, self.comparison_count
            else:
                # Сдвиг по правилу плохого символа
                char = text[i + j]
                shift = bad_char.get(char, -1)
                i += max(1, j - shift)
        
        return -1, self.comparison_count
    
    # 4. Алгоритм Кнута-Морриса-Пратта
    def kmp_search(self, text, pattern):
        """Алгоритм Кнута-Морриса-Пратта"""
        self.reset_counter()
        n = len(text)
        m = len(pattern)
        
        # Префикс-функция
        lps = [0] * m
        length = 0
        i = 1
        
        while i < m:
            self.comparison_count += 1
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        
        # Поиск
        i = j = 0
        while i < n:
            self.comparison_count += 1
            if pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == m:
                return i - j, self.comparison_count
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        
        return -1, self.comparison_count

# Генерация тестовых данных
def generate_test_cases():
    """Генерация тестовых данных для разных сценариев"""
    
    # Лучший случай для каждого алгоритма
    best_cases = {
        'naive': ('a' * 1000 + 'b', 'a' * 100),  # Паттерн в начале
        'rabin_karp': ('abc' * 100, 'abc'),  # Минимум коллизий
        'boyer_moore': ('x' * 100 + 'pattern', 'pattern'),  # Паттерн в конце
        'kmp': ('a' * 1000, 'a' * 50)  # Длинные совпадения
    }
    
    # Худший случай для каждого алгоритма
    worst_cases = {
        'naive': ('a' * 1000, 'a' * 50 + 'b'),  # Много частичных совпадений
        'rabin_karp': ('abc' * 100, 'abd'),  # Много коллизий хешей
        'boyer_moore': ('a' * 1000, 'b' * 50),  # Нет совпадений
        'kmp': ('a' * 1000 + 'b', 'a' * 50 + 'b')  # Длинные префиксы
    }
    
    return best_cases, worst_cases

# Проведение тестирования
def run_comparison():
    """Запуск сравнения алгоритмов"""
    searcher = StringSearchAlgorithms()
    best_cases, worst_cases = generate_test_cases()
    
    algorithms = {
        'Naive': searcher.naive_search,
        'Rabin-Karp': searcher.rabin_karp_search,
        'Boyer-Moore': searcher.boyer_moore_search,
        'KMP': searcher.kmp_search
    }
    
    results = {'best': {}, 'worst': {}}
    
    # Тестирование лучших случаев
    print("=== ЛУЧШИЕ СЛУЧАИ ===")
    for algo_name, algo_func in algorithms.items():
        case_key = algo_name.lower().replace('-', '_').split(' ')[0]
        if case_key in best_cases:
            text, pattern = best_cases[case_key]
            
            start_time = time.time()
            position, comparisons = algo_func(text, pattern)
            end_time = time.time()
            
            results['best'][algo_name] = {
                'time': (end_time - start_time) * 1000,  # мс
                'comparisons': comparisons,
                'position': position
            }
            
            print(f"{algo_name}: {results['best'][algo_name]}")
    
    # Тестирование худших случаев
    print("\n=== ХУДШИЕ СЛУЧАИ ===")
    for algo_name, algo_func in algorithms.items():
        case_key = algo_name.lower().replace('-', '_').split(' ')[0]
        if case_key in worst_cases:
            text, pattern = worst_cases[case_key]
            
            start_time = time.time()
            position, comparisons = algo_func(text, pattern)
            end_time = time.time()
            
            results['worst'][algo_name] = {
                'time': (end_time - start_time) * 1000,  # мс
                'comparisons': comparisons,
                'position': position
            }
            
            print(f"{algo_name}: {results['worst'][algo_name]}")
    
    return results

# Визуализация результатов
def plot_results(results):
    """Визуализация результатов сравнения"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Время выполнения
    best_times = [results['best'][algo]['time'] for algo in results['best']]
    worst_times = [results['worst'][algo]['time'] for algo in results['worst']]
    algorithms = list(results['best'].keys())
    
    x = np.arange(len(algorithms))
    width = 0.35
    
    ax1.bar(x - width/2, best_times, width, label='Лучший случай', alpha=0.8)
    ax1.bar(x + width/2, worst_times, width, label='Худший случай', alpha=0.8)
    ax1.set_xlabel('Алгоритмы')
    ax1.set_ylabel('Время (мс)')
    ax1.set_title('Сравнение времени выполнения')
    ax1.set_xticks(x)
    ax1.set_xticklabels(algorithms, rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Количество сравнений
    best_comparisons = [results['best'][algo]['comparisons'] for algo in results['best']]
    worst_comparisons = [results['worst'][algo]['comparisons'] for algo in results['worst']]
    
    ax2.bar(x - width/2, best_comparisons, width, label='Лучший случай', alpha=0.8)
    ax2.bar(x + width/2, worst_comparisons, width, label='Худший случай', alpha=0.8)
    ax2.set_xlabel('Алгоритмы')
    ax2.set_ylabel('Количество сравнений')
    ax2.set_title('Сравнение количества сравнений символов')
    ax2.set_xticks(x)
    ax2.set_xticklabels(algorithms, rotation=45)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Детальный анализ сложности
def complexity_analysis():
    """Анализ временной сложности алгоритмов"""
    analysis = {
        'Алгоритм': ['Наивный', 'Рабин-Карп', 'Бойер-Мур', 'KMP'],
        'Лучший случай': ['O(n)', 'O(n+m)', 'O(n/m)', 'O(n)'],
        'Худший случай': ['O(n×m)', 'O(n×m)', 'O(n×m)', 'O(n+m)'],
        'Средний случай': ['O(n×m)', 'O(n+m)', 'O(n)', 'O(n+m)'],
        'Память': ['O(1)', 'O(1)', 'O(m+s)', 'O(m)']
    }
    
    print("\n=== АНАЛИЗ СЛОЖНОСТИ ===")
    for i in range(len(analysis['Алгоритм'])):
        print(f"\n{analysis['Алгоритм'][i]}:")
        print(f"  Лучший случай: {analysis['Лучший случай'][i]}")
        print(f"  Худший случай: {analysis['Худший случай'][i]}")
        print(f"  Средний случай: {analysis['Средний случай'][i]}")
        print(f"  Память: {analysis['Память'][i]}")

# Практические рекомендации
def practical_recommendations():
    """Практические рекомендации по выбору алгоритма"""
    recommendations = [
        {
            'Ситуация': 'Короткие строки, простые паттерны',
            'Рекомендация': 'Наивный алгоритм',
            'Причина': 'Минимальные накладные расходы'
        },
        {
            'Ситуация': 'Поиск нескольких паттернов',
            'Рекомендация': 'Рабин-Карп',
            'Причина': 'Эффективное хеширование нескольких образцов'
        },
        {
            'Ситуация': 'Тексты на естественных языках',
            'Рекомендация': 'Бойер-Мур',
            'Причина': 'Быстрая работа на практике'
        },
        {
            'Ситуация': 'Жесткие требования к времени',
            'Рекомендация': 'KMP',
            'Причина': 'Гарантированная линейная сложность'
        },
        {
            'Ситуация': 'Паттерны с повторениями',
            'Рекомендация': 'KMP',
            'Причина': 'Эффективная обработка периодичных паттернов'
        }
    ]
    
    print("\n=== ПРАКТИЧЕСКИЕ РЕКОМЕНДАЦИИ ===")
    for rec in recommendations:
        print(f"\n{rec['Ситуация']}:")
        print(f"  Алгоритм: {rec['Рекомендация']}")
        print(f"  Причина: {rec['Причина']}")

# Запуск полного анализа
if __name__ == "__main__":
    print("ЗАПУСК СРАВНИТЕЛЬНОГО АНАЛИЗА АЛГОРИТМОВ ПОИСКА ПОДСТРОК")
    print("=" * 60)
    
    # Запуск тестов
    results = run_comparison()
    
    # Визуализация
    plot_results(results)
    
    # Анализ сложности
    complexity_analysis()
    
    # Рекомендации
    practical_recommendations()
    
    # Итоговый вывод
    print("\n" + "=" * 60)
    print("ИТОГОВЫЕ ВЫВОДЫ:")
    print("1. Бойер-Мур показывает лучшие результаты на практике")
    print("2. KMP гарантирует линейное время в худшем случае") 
    print("3. Наивный алгоритм эффективен только для коротких строк")
    print("4. Рабин-Карп хорош для поиска нескольких паттернов")
    print("5. Выбор алгоритма зависит от специфики задачи и данных")