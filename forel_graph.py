import matplotlib.pyplot as plt
import numpy as np

# Считываем данные из файла
x_coords = []
y_coords = []
classes = []

# Определяем цвета для каждого класса
colors = {
    1: 'blue',
    2: 'red',
    3: 'green',
    # Добавьте больше классов и их цветов по мере необходимости
}

with open('result1.txt', 'r') as file:
    for line in file:
        # Разделяем строку на значения и преобразуем их в целые числа
        x, y, class_num = map(float, line.split())
        x_coords.append(x)
        y_coords.append(y)
        classes.append(class_num)

# Преобразуем данные в numpy массивы
X = np.array([x_coords, y_coords]).T
y = np.array(classes)

# Алгоритм Forel


def forel(X, k):
    """
    Алгоритм Forel для кластеризации.

    Args:
      X: Массив данных (N x D), где N - количество точек, D - размерность.
      k: Количество кластеров.

    Returns:
      labels: Массив меток кластеров (N).
      centroids: Массив центров кластеров (k x D).
    """

    # Инициализируем центры кластеров случайным образом
    centroids = X[np.random.choice(X.shape[0], k, replace=False)]

    # Инициализируем метки кластеров
    labels = np.zeros(X.shape[0], dtype=int)

    # Повторяем до сходимости
    while True:
        # Присваиваем точки ближайшим центрам
        for i in range(X.shape[0]):
            distances = np.linalg.norm(X[i] - centroids, axis=1)
            labels[i] = np.argmin(distances)

        # Обновляем центры кластеров
        new_centroids = np.zeros((k, X.shape[1]))
        for i in range(k):
            new_centroids[i] = np.mean(X[labels == i], axis=0)

        # Если центры не изменились, то сходимость достигнута
        if np.allclose(centroids, new_centroids):
            break

        # Обновляем центры кластеров
        centroids = new_centroids

    return labels, centroids


# Запускаем алгоритм Forel
k = 3  # Количество кластеров
labels, centroids = forel(X, k)

# Создаем график
plt.figure(figsize=(8, 6))

# Отображаем точки с учетом класса
for i in range(k):
    indices = np.where(labels == i)[0]
    plt.scatter(X[indices, 0], X[indices, 1],
                color=colors.get(i + 1, 'black'),
                marker='o', label=f'Кластер {i + 1}')

# Отображаем центры кластеров
plt.scatter(centroids[:, 0], centroids[:, 1],
            color='yellow',
            marker='X',
            s=200,
            label='Центры кластеров')

# Настраиваем график
plt.title('Двумерный график точек (кластеризация Forel)')
plt.xlabel('Ось X')
plt.ylabel('Ось Y')
plt.grid(True)
plt.legend()  # Добавляем легенду

# Показываем график
plt.show()
