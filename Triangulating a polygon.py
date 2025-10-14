import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
import numpy as np

# Определение класса Point, который отсутствовал
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def cross(self, other):
        return self.x * other.y - self.y * other.x
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# Алгоритм триангуляции "Ear Clipping"
def ear_clipping_triangulation(polygon):
    """
    Алгоритм отрезания ушей для триангуляции простого многоугольника
    """
    def is_ear(i, vertices):
        """Проверяет, является ли вершина ухом"""
        n = len(vertices)
        a = vertices[(i-1) % n]
        b = vertices[i]
        c = vertices[(i+1) % n]
        
        # Проверка выпуклости
        ab = b - a
        bc = c - b
        if ab.cross(bc) <= 0:  # Не выпуклый угол
            return False
        
        # Проверка, что внутри треугольника abc нет других вершин
        triangle = [a, b, c]
        for j in range(n):
            if j not in [(i-1) % n, i, (i+1) % n]:
                if point_in_triangle(vertices[j], triangle):
                    return False
        return True
    
    def point_in_triangle(p, triangle):
        """Проверяет, лежит ли точка внутри треугольника"""
        a, b, c = triangle
        
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
        
        d1 = sign(p, a, b)
        d2 = sign(p, b, c)
        d3 = sign(p, c, a)
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)
    
    vertices = polygon.copy()
    triangles = []
    
    while len(vertices) > 3:
        n = len(vertices)
        ear_found = False
        
        for i in range(n):
            if is_ear(i, vertices):
                # Отрезаем ухо
                a = vertices[(i-1) % n]
                b = vertices[i]
                c = vertices[(i+1) % n]
                triangles.append([a, b, c])
                vertices.pop(i)
                ear_found = True
                break
        
        if not ear_found:
            # Резервный метод - если не нашли ухо, используем первую вершину
            # (это может произойти для невыпуклых многоугольников)
            i = 0
            a = vertices[(i-1) % n]
            b = vertices[i]
            c = vertices[(i+1) % n]
            triangles.append([a, b, c])
            vertices.pop(i)
    
    # Добавляем последний треугольник
    if len(vertices) == 3:
        triangles.append(vertices)
    
    return triangles

def visualize_triangulation(polygon, triangles, title="Триангуляция многоугольника"):
    """Визуализация триангуляции"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Рисуем исходный многоугольник
    poly_coords = [(p.x, p.y) for p in polygon]
    poly_coords.append(poly_coords[0])  # Замыкаем многоугольник
    x, y = zip(*poly_coords)
    ax.plot(x, y, 'b-', linewidth=2, label='Исходный многоугольник')
    
    # Рисуем треугольники
    tri_patches = []
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'brown', 'gray', 'olive']
    for i, triangle in enumerate(triangles):
        tri_coords = [(p.x, p.y) for p in triangle]
        tri_patches.append(patches.Polygon(tri_coords, alpha=0.6, facecolor=colors[i % len(colors)]))
    
    # Добавляем треугольники на график
    for patch in tri_patches:
        ax.add_patch(patch)
    
    # Подписываем вершины
    for i, p in enumerate(polygon):
        ax.text(p.x, p.y, f'{i}', fontsize=12, ha='center', va='center',
               bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7))
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.axis('equal')
    ax.legend()
    plt.show()

def analyze_triangulation_quality(triangles):
    """Анализ качества триангуляции"""
    qualities = []
    min_angle = float('inf')
    max_angle = 0
    
    for triangle in triangles:
        a, b, c = triangle
        # Вычисляем длины сторон
        ab = np.sqrt((b.x - a.x)**2 + (b.y - a.y)**2)
        bc = np.sqrt((c.x - b.x)**2 + (c.y - b.y)**2)
        ca = np.sqrt((a.x - c.x)**2 + (a.y - c.y)**2)
        
        # Вычисляем углы по теореме косинусов
        def calculate_angle(a, b, c):
            """Вычисляет угол при вершине a"""
            ab = np.sqrt((b.x - a.x)**2 + (b.y - a.y)**2)
            ac = np.sqrt((c.x - a.x)**2 + (c.y - a.y)**2)
            bc = np.sqrt((c.x - b.x)**2 + (c.y - b.y)**2)
            
            # Теорема косинусов
            cos_angle = (ab**2 + ac**2 - bc**2) / (2 * ab * ac)
            # Обеспечиваем, чтобы значение было в допустимом диапазоне [-1, 1]
            cos_angle = max(-1.0, min(1.0, cos_angle))
            return np.arccos(cos_angle)
        
        angle_a = calculate_angle(a, b, c)
        angle_b = calculate_angle(b, a, c)
        angle_c = calculate_angle(c, a, b)
        
        angles = np.degrees([angle_a, angle_b, angle_c])
        min_tri_angle = np.min(angles)
        max_tri_angle = np.max(angles)
        
        qualities.append(min_tri_angle)
        min_angle = min(min_angle, min_tri_angle)
        max_angle = max(max_angle, max_tri_angle)
    
    return {
        'min_angle': min_angle,
        'max_angle': max_angle,
        'avg_min_angle': np.mean(qualities),
        'num_triangles': len(triangles),
        'quality_scores': qualities
    }

def experimental_analysis():
    """Экспериментальный анализ различных алгоритмов"""
    
    # Тестовые многоугольники (исправлены ошибки в Point(@, 0) -> Point(0, 0))
    test_polygons = [
        [Point(0, 0), Point(4, 0), Point(4, 3), Point(2, 5), Point(0, 3)],  # Выпуклый
        [Point(0, 0), Point(5, 0), Point(7, 3), Point(3, 6), Point(1, 4), Point(-1, 2)],  # Вогнутый
        [Point(0, 0), Point(6, 0), Point(8, 4), Point(4, 8), Point(2, 6), Point(0, 3)]   # Сложный
    ]
    
    results = []
    
    for i, polygon in enumerate(test_polygons):
        print(f"\n=== Анализ многоугольника {i+1} ===")
        print(f"Количество вершин: {len(polygon)}")
        
        # Тестируем Ear Clipping
        triangles_ear = ear_clipping_triangulation(polygon)
        quality_ear = analyze_triangulation_quality(triangles_ear)
        
        print("\nEar Clipping:")
        print(f"  Минимальный угол: {quality_ear['min_angle']:.2f}°")
        print(f"  Средний минимальный угол: {quality_ear['avg_min_angle']:.2f}°")
        print(f"  Количество треугольников: {quality_ear['num_triangles']}")
        
        # Визуализация
        visualize_triangulation(polygon, triangles_ear, 
                              f"Ear Clipping - Многоугольник {i+1}")
        
        results.append({
            'polygon': i+1,
            'ear_clipping': quality_ear
        })
    
    return results

# Запуск анализа
if __name__ == "__main__":
    results = experimental_analysis()