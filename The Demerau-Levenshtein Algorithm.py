def min_operations(s1, s2):
    m, n = len(word1), len(word2)

    DELETE = 1
    INSERT = 1
    REPLACE = 1

    dp = [[0] * (n+1) for _ in range(m+1)]
    operations = []

    for i in range(1, m+1):
        dp[i][0] = dp[i-1][0] + DELETE

    for j in range (1,n+1):
        dp[0][j] = dp[0][j-1] + INSERT


    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:

                dp[i][j] = min(
                    dp[i - 1][j] + DELETE,  # Удаление
                    dp[i][j - 1] + INSERT,  # Вставка
                    dp[i - 1][j - 1] + REPLACE  # Замена
                )

                if dp[i][j] == dp[i - 1][j] + DELETE:
                    operations.append('delete')
                elif dp[i][j] == dp[i][j - 1] + INSERT:
                    operations.append('insert')
                elif dp[i][j] == dp[i - 1][j - 1] + REPLACE:
                    operations.append('replace')

    find_ops = operations
    count_delete = find_ops.count('delete')
    count_insert = find_ops.count('insert')
    count_replace = find_ops.count('replace')

    print(f'ИТОГОВОЕ КОЛ-ВО ОПЕРАЦИЙ:\n'
          f'Удаление: {count_delete}\n'
          f'Вставка: {count_insert}\n'
          f'Замена: {count_replace}')

    for p in dp:
        print(p)
    return dp[m][n]


word1 = 'kitten'
word2 = 'sitteng'

print(f'Минимальное кол-во операций {min_operations(word1, word2)}')