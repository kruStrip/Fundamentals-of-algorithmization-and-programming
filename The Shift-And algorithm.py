def debug_shift_and(text, pattern):
    """Визуализация работы алгоритма Shift-And"""
    print(f"Текст: {text}")
    print(f"Шаблон: {pattern}")
    print()
    
    n = len(text)
    m = len(pattern)
    
    # Создание масок
    char_masks = {}
    for i, char in enumerate(pattern):
        if char not in char_masks:
            char_masks[char] = 0
        char_masks[char] |= (1 << i)
    
    print("Битовые маски:")
    for char, mask in char_masks.items():
        print(f"  '{char}': {bin(mask)}")
    
    R = 0
    match_mask = 1 << (m - 1)
    
    print(f"\nМаска совпадения: {bin(match_mask)}")
    print("\nПроцесс поиска:")
    print("i | Символ | R (бинарно) | R (десятично) | Совпадение")
    print("-" * 55)
    
    for i, char in enumerate(text):
        old_R = R
        R = ((R << 1) | 1) & char_masks.get(char, 0)
        match = "ДА" if R & match_mask else "нет"
        print(f"{i:1} | '{char:5}' | {bin(R):12} | {R:8} | {match:10}")
        
        if R & match_mask:
            print(f"→ Найдено в позиции {i - m + 1}!")
            break

# Пример использования
debug_shift_and("ABCABCAB", "ABCAB")