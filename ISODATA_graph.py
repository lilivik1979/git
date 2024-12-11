import numpy as np
import matplotlib.pyplot as plt


def isodata(points, initial_k, max_iter=100, tol=1e-4):
    """Алгоритм ISODATA для кластеризации точек."""
    n_points = points.shape[0]

    # Инициализация центров кластеров случайными точками
    np.random.seed(42)  # Для воспроизводимости
    centers = points[np.random.choice(n_points, initial_k, replace=False)]

    # Инициализация переменных
    labels = np.zeros(n_points)
    distances = np.zeros((n_points, initial_k))

    for iteration in range(max_iter):
        # Шаг 1: Присвоение меток кластерам
        for i in range(initial_k):
            distances[:, i] = np.linalg.norm(points - centers[i], axis=1)

        labels = np.argmin(distances, axis=1)

        # Шаг 2: Обновление центров кластеров
        new_centers = np.array([points[labels == i].mean(axis=0)
                                for i in range(initial_k)])

        # Проверка на сходимость
        if np.linalg.norm(new_centers - centers) < tol:
            break

        centers = new_centers

        # Шаг 3: Удаление пустых кластеров и объединение близких
        unique_labels, counts = np.unique(labels, return_counts=True)

        # Удаляем пустые кластеры
        centers = centers[unique_labels]

        # Объединяем близкие кластеры
        if len(centers) < initial_k:
            initial_k = len(centers)

    return labels, centers


x_coords = []
y_coords = []
classes = []


colors = {
    1: 'blue',
    2: 'red',
    3: 'green',
}

with open('result.txt', 'r') as file:
    for line in file:
        x, y, class_num = map(float, line.split())
        x_coords.append(x)
        y_coords.append(y)
        classes.append(class_num)

# Объединяем координаты в массив точек
points = np.array(list(zip(x_coords, y_coords)))

# Применяем алгоритм ISODATA
initial_k = 3  # Начальное количество кластеров
labels, centers = isodata(points, initial_k)

# Создаем график
plt.figure(figsize=(10, 8))

# Отображаем точки с учетом меток кластеров
for i in range(initial_k):
    plt.scatter(points[labels == i][:, 0], points[labels == i][:, 1],
                marker='o', label=f'Кластер {i + 1}')

# Отображаем центры кластеров
plt.scatter(centers[:, 0], centers[:, 1], color='black', marker='x', s=200,
            label='Центры кластеров')

# Настраиваем график
plt.title('Двумерный график точек с кластеризацией ISODATA')
plt.xlabel('Ось X')
plt.ylabel('Ось Y')
plt.grid(True)
plt.legend()  # Добавляем легенду

# Показываем график
plt.show()
