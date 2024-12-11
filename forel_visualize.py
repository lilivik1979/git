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
}

with open('result.txt', 'r') as file:
    for line in file:
        # Разделяем строку на значения и преобразуем их в целые числа
        x, y, class_num = map(float, line.split())
        x_coords.append(x)
        y_coords.append(y)
        classes.append(class_num)

# Преобразуем данные в numpy массивы
X = np.array([x_coords, y_coords]).T
y = np.array(classes)

# Считываем центры кластеров
centroid_xs = []
centroid_ys = []

with open('centroids.txt', 'r') as file:
    for line in file:
        cx, cy = map(float, line.split())
        centroid_xs.append(cx)
        centroid_ys.append(cy)

# Преобразуем центры в numpy массивы
centroids = np.array([centroid_xs, centroid_ys]).T

# Создаем график
plt.figure(figsize=(8, 6))

# Отображаем точки с учетом класса
for i in range(3):  # Изменено на 3 для соответствия количеству кластеров
    indices = np.where(y == i + 1)[0]
    plt.scatter(X[indices, 0], X[indices, 1],
                color=colors.get(i + 1, 'black'),
                marker='o', label=f'Класс {i + 1}')

# Отображаем центры кластеров
plt.scatter(centroids[:, 0], centroids[:, 1], color='yellow', marker='X', s=200, label='Центры кластеров')

# Настраиваем график
plt.title('Двумерный график точек (кластеризация Forel)')
plt.xlabel('Ось X')
plt.ylabel('Ось Y')
plt.grid(True)
plt.legend()  # Добавляем легенду

# Показываем график
plt.show()
