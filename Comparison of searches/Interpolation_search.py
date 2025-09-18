def interpolation_search(arr, target):

    n = len(arr)
    if n == 0:
        return -1

    left = 0
    right = n - 1

    # Пока целевое значение находится в границах текущего диапазона
    while left <= right and arr[left] <= target <= arr[right]:

        # Если крайние значения равны, проверяем совпадение и выходим
        if arr[right] == arr[left]:
            return left if arr[left] == target else -1

        # Интерполяционная оценка позиции
        pos = left + int((target - arr[left]) * (right - left) / (arr[right] - arr[left]))

        # Защита: ограничиваем позицию текущими границами
        if pos < left:
            pos = left
        elif pos > right:
            pos = right

        if arr[pos] == target:
            return pos
        if arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1

    return -1
