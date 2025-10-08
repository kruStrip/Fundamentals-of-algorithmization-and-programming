class TreeNode:
    """Узел FP-дерева"""
    def __init__(self, name, count, parent):
        self.name = name
        self.count = count
        self.parent = parent
        self.children = {}
        self.next = None  # ссылка на следующий узел с таким же именем

    def increment(self, count):
        self.count += count

def create_fp_tree(dataset, min_support):
    """Строит FP-дерево из набора данных"""
    
    # Первый проход: подсчет поддержки для каждого элемента
    item_counts = {}
    for transaction in dataset:
        for item in transaction:
            item_counts[item] = item_counts.get(item, 0) + 1
    
    # Фильтрация элементов по минимальной поддержке
    frequent_items = {item: count for item, count in item_counts.items() 
                     if count >= min_support}
    
    if len(frequent_items) == 0:
        return None, None
    
    # Сортировка частых элементов по убыванию поддержки
    frequent_items = dict(sorted(frequent_items.items(), 
                                key=lambda x: (-x[1], x[0])))
    
    # Создание заголовочной таблицы
    header_table = {}
    for item in frequent_items:
        header_table[item] = [frequent_items[item], None]  # [count, head_node]
    
    # Второй проход: построение FP-дерева
    root = TreeNode("Null", 1, None)
    
    for transaction in dataset:
        # Фильтрация и сортировка элементов транзакции
        filtered_transaction = [item for item in transaction 
                              if item in frequent_items]
        filtered_transaction.sort(key=lambda x: (-frequent_items[x], x))
        
        current_node = root
        # Добавление элементов в дерево
        for item in filtered_transaction:
            if item in current_node.children:
                current_node.children[item].increment(1)
            else:
                new_node = TreeNode(item, 1, current_node)
                current_node.children[item] = new_node
                
                # Обновление заголовочной таблицы
                if header_table[item][1] is None:
                    header_table[item][1] = new_node
                else:
                    node = header_table[item][1]
                    while node.next is not None:
                        node = node.next
                    node.next = new_node
            
            current_node = current_node.children[item]
    
    return root, header_table

def ascend_tree(node, prefix_path):
    """Восстанавливает путь от узла до корня"""
    if node.parent is not None:
        prefix_path.append(node.name)
        ascend_tree(node.parent, prefix_path)

def find_prefix_path(base_pattern, header_table):
    """Находит условные базовые шаблоны для элемента"""
    conditional_patterns = {}
    node = header_table[base_pattern][1]
    
    while node is not None:
        prefix_path = []
        ascend_tree(node.parent, prefix_path)
        
        if len(prefix_path) > 0:
            conditional_patterns[tuple(prefix_path)] = node.count
        
        node = node.next
    
    return conditional_patterns

def mine_fp_tree(header_table, min_support, prefix, frequent_itemsets):
    # Сортировка элементов по поддержке (по возрастанию)
    sorted_items = sorted(header_table.items(), 
                         key=lambda x: (x[1][0], x[0]))
    
    for item, (count, node) in sorted_items:
        new_freq_set = prefix.copy()
        new_freq_set.add(item)
        frequent_itemsets[tuple(sorted(new_freq_set))] = count
        
        # Построение условных шаблонов
        conditional_patterns = find_prefix_path(item, header_table)
        
        if len(conditional_patterns) > 0:
            # Построение условного FP-дерева
            conditional_dataset = []
            for pattern, pattern_count in conditional_patterns.items():
                conditional_dataset.extend([list(pattern)] * pattern_count)
            
            conditional_tree, conditional_header = create_fp_tree(
                conditional_dataset, min_support)
            
            if conditional_header is not None:
                # Рекурсивный вызов для условного дерева
                mine_fp_tree(conditional_header, min_support, 
                           new_freq_set, frequent_itemsets)

def fpgrowth(dataset, min_support):
    # Построение начального FP-дерева
    root, header_table = create_fp_tree(dataset, min_support)
    
    if header_table is None:
        return {}
    
    # Извлечение частых наборов
    frequent_itemsets = {}
    mine_fp_tree(header_table, min_support, set(), frequent_itemsets)
    
    return frequent_itemsets

def print_results(frequent_itemsets):
    print("Найденные частые наборы\tПоддержка")
    print("-" * 40)
    
    # Сортировка по размеру набора и затем по элементам
    sorted_itemsets = sorted(frequent_itemsets.items(), 
                           key=lambda x: (len(x[0]), x[0]))
    
    for itemset, support in sorted_itemsets:
        itemset_str = "{" + ", ".join(map(str, itemset)) + "}"
        print(f"{itemset_str}\t{support}")

dataset = [
    [1, 2, 3, 5],    # T1
    [2, 3, 4, 5],    # T2  
    [1, 2, 3, 5],    # T3
    [1, 2, 3, 4, 5], # T4
    [1, 2, 3, 4]     # T5
]

min_support = 2
frequent_itemsets = fpgrowth(dataset, min_support)

print_results(frequent_itemsets)