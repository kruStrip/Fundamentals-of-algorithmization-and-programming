import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.metrics import pairwise_distances_argmin
import matplotlib.cm as cm

class KMeans:
    def __init__(self, n_clusters=3, max_iters=100, random_state=42):
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.random_state = random_state
        self.centroids = None
        self.labels = None
        self.inertia_ = None
        
    def _initialize_centroids(self, X):
        """Инициализация центроидов методом k-means++"""
        np.random.seed(self.random_state)
        n_samples, n_features = X.shape
        
        # Первый центроид выбирается случайно
        centroids = [X[np.random.randint(n_samples)]]
        
        # Остальные центроиды выбираются с вероятностью пропорциональной квадрату расстояния
        for _ in range(1, self.n_clusters):
            distances = np.array([min([np.linalg.norm(x - c)**2 for c in centroids]) for x in X])
            probabilities = distances / distances.sum()
            cumulative_probs = probabilities.cumsum()
            r = np.random.rand()
            
            for j, p in enumerate(cumulative_probs):
                if r < p:
                    centroids.append(X[j])
                    break
        
        return np.array(centroids)
    
    def fit(self, X):
        """Обучение алгоритма k-Средних"""
        n_samples, n_features = X.shape
        
        # Инициализация центроидов
        self.centroids = self._initialize_centroids(X)
        
        for iteration in range(self.max_iters):
            # Шаг назначения: каждая точка назначается ближайшему центроиду
            labels = pairwise_distances_argmin(X, self.centroids)
            
            # Шаг обновления: пересчет центроидов
            new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(self.n_clusters)])
            
            # Проверка сходимости
            if np.allclose(self.centroids, new_centroids):
                break
                
            self.centroids = new_centroids
        
        self.labels_ = pairwise_distances_argmin(X, self.centroids)
        self.inertia_ = self._calculate_inertia(X)
        
        return self
    
    def _calculate_inertia(self, X):
        """Вычисление инерции (within-cluster sum of squares)"""
        inertia = 0
        for i in range(self.n_clusters):
            cluster_points = X[self.labels_ == i]
            if len(cluster_points) > 0:
                inertia += np.sum((cluster_points - self.centroids[i])**2)
        return inertia
    
    def predict(self, X):
        """Предсказание кластеров для новых данных"""
        return pairwise_distances_argmin(X, self.centroids)

# Генерация демонстрационных данных
np.random.seed(42)
X, y_true = make_blobs(n_samples=300, centers=4, n_features=2, 
                       cluster_std=0.60, random_state=42)

# Визуализация процесса работы алгоритма
def plot_kmeans_steps(X, k, max_iters=5):
    """Визуализация шагов алгоритма k-Средних"""
    kmeans = KMeans(n_clusters=k, max_iters=max_iters)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    # Инициализация
    centroids = kmeans._initialize_centroids(X)
    axes[0].scatter(X[:, 0], X[:, 1], alpha=0.6)
    axes[0].scatter(centroids[:, 0], centroids[:, 1], marker='x', s=200, linewidths=3, c='red')
    axes[0].set_title('Шаг 1: Инициализация центроидов')
    
    for i in range(1, 6):
        kmeans = KMeans(n_clusters=k, max_iters=i)
        kmeans.fit(X)
        
        colors = cm.tab10(np.linspace(0, 1, k))
        
        for cluster_id in range(k):
            cluster_points = X[kmeans.labels_ == cluster_id]
            axes[i].scatter(cluster_points[:, 0], cluster_points[:, 1], 
                          alpha=0.6, color=colors[cluster_id])
        
        axes[i].scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1], 
                       marker='x', s=200, linewidths=3, c='black')
        axes[i].set_title(f'Шаг {i+1}: Итерация {i}')
    
    plt.tight_layout()
    plt.show()

# Запуск визуализации
plot_kmeans_steps(X, k=4)

# Анализ оптимального числа кластеров с помощью метода локтя
def elbow_method(X, max_k=10):
    """Метод локтя для определения оптимального k"""
    inertias = []
    k_range = range(1, max_k + 1)
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
    
    plt.figure(figsize=(10, 6))
    plt.plot(k_range, inertias, 'bo-')
    plt.xlabel('Число кластеров (k)')
    plt.ylabel('Инерция (Within-cluster sum of squares)')
    plt.title('Метод локтя для определения оптимального k')
    plt.grid(True)
    plt.show()
    
    return inertias

# Применение метода локтя
inertias = elbow_method(X)

# Сравнение с реализацией из sklearn
from sklearn.cluster import KMeans as SKLearnKMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

# Наша реализация
our_kmeans = KMeans(n_clusters=4, random_state=42)
our_labels = our_kmeans.fit(X).labels_

# Sklearn реализация
sklearn_kmeans = SKLearnKMeans(n_clusters=4, random_state=42, init='k-means++')
sklearn_labels = sklearn_kmeans.fit_predict(X)

# Сравнение метрик
print("СРАВНЕНИЕ РЕАЛИЗАЦИЙ:")
print(f"Наша инерция: {our_kmeans.inertia_:.2f}")
print(f"Sklearn инерция: {sklearn_kmeans.inertia_:.2f}")
print(f"Adjusted Rand Score: {adjusted_rand_score(our_labels, sklearn_labels):.3f}")
print(f"Silhouette Score (наша): {silhouette_score(X, our_labels):.3f}")
print(f"Silhouette Score (sklearn): {silhouette_score(X, sklearn_labels):.3f}")

# Визуализация сравнения
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

colors = cm.tab10(np.linspace(0, 1, 4))

# Наша реализация
for cluster_id in range(4):
    cluster_points = X[our_labels == cluster_id]
    ax1.scatter(cluster_points[:, 0], cluster_points[:, 1], 
               alpha=0.6, color=colors[cluster_id], label=f'Кластер {cluster_id+1}')
ax1.scatter(our_kmeans.centroids[:, 0], our_kmeans.centroids[:, 1], 
           marker='x', s=200, linewidths=3, c='black', label='Центроиды')
ax1.set_title('Наша реализация k-Средних')
ax1.legend()

# Sklearn реализация
for cluster_id in range(4):
    cluster_points = X[sklearn_labels == cluster_id]
    ax2.scatter(cluster_points[:, 0], cluster_points[:, 1], 
               alpha=0.6, color=colors[cluster_id], label=f'Кластер {cluster_id+1}')
ax2.scatter(sklearn_kmeans.cluster_centers_[:, 0], sklearn_kmeans.cluster_centers_[:, 1], 
           marker='x', s=200, linewidths=3, c='black', label='Центроиды')
ax2.set_title('Sklearn реализация k-Средних')
ax2.legend()

plt.tight_layout()
plt.show()