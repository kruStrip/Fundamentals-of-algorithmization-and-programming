items = ["хлеб", "молоко", "масло", "сыр", "пиво",
         "газировка", "яблоки", "яйца", "чай", "колбаса",
         "лук", "сок", "чипсы", "тропические фрукты"]

transactions = [
    ["хлеб", "молоко", "масло"],
    ["пиво", "газировка", "чипсы"],
    ["хлеб", "сыр", "колбаса", "яблоки"],
    ["молоко", "яйца", "хлеб"],
    ["пиво", "сок", "газировка"],
    ["чай", "тропические фрукты"],
    ["сыр", "колбаса", "лук"],
    ["хлеб", "масло", "яйца", "молоко"]
]

n = len(transactions)  

# Считаем, в скольких чеках встречается каждый товар 
count_single = {it: 0 for it in items}
for t in transactions:
    for it in t:
        count_single[it] += 1

# Для одиночного товара
def support_item(it):
    return count_single.get(it, 0) / n

count_pair = {}  
for x in items:
    for y in items:
        if x == y:
            continue
        count = 0
        for t in transactions:
            if x in t and y in t:
                count += 1
        count_pair[(x, y)] = count

# Порог мин. поддержки
min_support = 0.01  

# Список товаров, которые не редкие
frequent = [it for it in items if support_item(it) >= min_support]

# Метрики
def support_pair(x, y):
    return count_pair.get((x, y), 0) / n

def confidence(x, y):
    s_x = support_item(x)
    if s_x == 0:
        return 0.0
    return support_pair(x, y) / s_x

def lift(x, y):
    s_y = support_item(y)
    if s_y == 0:
        return 0.0
    return confidence(x, y) / s_y

def conviction(x, y):
    conf = confidence(x, y)
    s_y = support_item(y)
    if conf == 1.0:
        return float('inf')  
    denom = 1 - conf
    if denom == 0:
        return float('inf')
    return (1 - s_y) / denom

# Результаты!
print(f"Всего транзакций: {n}\n")

print("Поддержки одиночных товаров:")
for it in sorted(frequent, key=lambda x: -count_single[x]):
    print(f" - {it}: {count_single[it]} / {support_item(it):.3f}")
print()

print("Лучшие пары 'X -> Y', (пара встречалась хотя бы в 1 транзакции):")
out = []
for x in frequent:
    for y in frequent:
        if x == y:
            continue
        cnt = count_pair.get((x,y), 0)
        if cnt == 0:
            continue
        sxy = support_pair(x, y)
        conf = confidence(x, y)
        lf = lift(x, y)
        conv = conviction(x, y)
        out.append((conv, x, y, cnt, sxy, conf, lf))

# Сортируем по убедительности в уменьш. порядке
out.sort(key=lambda x: (-float('inf') if x[0] == float('inf') else -x[0]))

# Выводим топ-10
for conv, x, y, cnt, sxy, conf, lf in out[:20]:
    conv_str = "inf" if conv == float('inf') else f"{conv:.3f}"
    print(f"{x} -> {y}: Кол-во={cnt}, Поддержка={sxy:.3f}, Достоверность={conf:.3f}, Лифт={lf:.3f}, Убедительность={conv_str}")

print("\nВыводы (на основе 'Уверенности' и вероятности), что купят Y при покупке X):")
for conv, x, y, cnt, sxy, conf, lf in out[:10]:
    print(f" - Если покупают '{x}', вероятность купить '{y}' ≈ {conf*100:.1f}% (пара встречалась в {cnt} чеках).")
