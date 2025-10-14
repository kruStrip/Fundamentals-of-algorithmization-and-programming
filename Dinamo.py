def max_expression_value(expression):
    # Разбиваем строку на токены по пробелам
    tokens = expression.split()
    if not tokens:
        return 0.0
    
    n = (len(tokens) + 1) // 2  # количество чисел
    nums = []
    ops = []
    
    # Извлекаем числа и операции
    for i in range(len(tokens)):
        if i % 2 == 0:
            nums.append(float(tokens[i]))
        else:
            ops.append(tokens[i])
    
    # Инициализация DP таблиц
    max_dp = [[0.0] * n for _ in range(n)]
    min_dp = [[0.0] * n for _ in range(n)]
    
    # Базовый случай: диагональные элементы
    for i in range(n):
        max_dp[i][i] = nums[i]
        min_dp[i][i] = nums[i]
    
    # Заполнение таблицы для подстрок разной длины
    for L in range(1, n):  # L - длина интервала минус 1
        for i in range(0, n - L):
            j = i + L
            max_dp[i][j] = -float('inf')
            min_dp[i][j] = float('inf')
            
            for k in range(i, j):
                left_max = max_dp[i][k]
                left_min = min_dp[i][k]
                right_max = max_dp[k+1][j]
                right_min = min_dp[k+1][j]
                op = ops[k]
                
                if op == '+':
                    val1 = left_max + right_max
                    val2 = left_min + right_min
                    max_dp[i][j] = max(max_dp[i][j], val1, val2)
                    min_dp[i][j] = min(min_dp[i][j], val1, val2)
                    
                elif op == '-':
                    val1 = left_max - right_min
                    val2 = left_min - right_max
                    max_dp[i][j] = max(max_dp[i][j], val1, val2)
                    min_dp[i][j] = min(min_dp[i][j], val1, val2)
                    
                elif op == '*':
                    val1 = left_max * right_max
                    val2 = left_max * right_min
                    val3 = left_min * right_max
                    val4 = left_min * right_min
                    max_dp[i][j] = max(max_dp[i][j], val1, val2, val3, val4)
                    min_dp[i][j] = min(min_dp[i][j], val1, val2, val3, val4)
                    
                elif op == '/':
                    # Проверка на возможное деление на ноль
                    if right_min <= 0.0 <= right_max:
                        continue
                    else:
                        val1 = left_max / right_max
                        val2 = left_max / right_min
                        val3 = left_min / right_max
                        val4 = left_min / right_min
                        max_dp[i][j] = max(max_dp[i][j], val1, val2, val3, val4)
                        min_dp[i][j] = min(min_dp[i][j], val1, val2, val3, val4)
    
    return max_dp[0][n-1]

# Примеры использования
if __name__ == "__main__":
    # Тестовые примеры
    test_expressions = [
        "1 + 2 * 3",           # 1 + (2*3) = 7
        "1 - 2 + 3 * 4",       # (1-2) + (3*4) = 11
        "0.5 * 2 - 1",         # (0.5*2) - 1 = 0
        "2 * 3 + 4 * 5",       # (2*3) + (4*5) = 26
        "1 - 2 - 3 - 4",       # 1 - 2 - 3 - 4 = -8
        "1 + 2 + 3 + 4",       # 1+2+3+4 = 10
        "2.5 * 2 * 2",         # 2.5*2*2 = 10
        "1 - 1 * 1",           # 1 - (1*1) = 0
        "3 / 2 * 4",           # (3/2)*4 = 6
    ]
    
    for expr in test_expressions:
        result = max_expression_value(expr)
        print(f"Выражение: {expr} -> Максимальное значение: {result}")