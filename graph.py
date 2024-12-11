import numpy as np
import matplotlib.pyplot as plt

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

# Чтение данных из result.txt
with open('result.txt', 'r') as file:
    for line in file:
        data_points = line.strip().split()  # Разделяем строку по пробелам
        x_coords.append(int(data_points[0]))  # Первое значение - x-координата
        y_coords.append(int(data_points[1]))  # Второе значение - y-координата
        classes.append(int(data_points[2]))  # Третье значение - номер класса

# Преобразуем списки в массивы numpy
X = np.array(list(zip(x_coords, y_coords)))
y = np.array(classes)

# Чтение данных из файлов distances_*.txt
distances = {}
for i in range(1, len(classes) + 1):  # Проходим по каждому классу
    with open(f"distances_{i}.txt", 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')  # Разделяем по двоеточию
            distances[f"class_{i}_{key}"] = float(value)  # Сохраняем данные в словарь


# Функция для алгоритма Хо-Кашьяпа
def ho_kashyap(X, y):
    # Инициализация параметров с наклоном
    w = np.array([1.0, 1.0])  # Начальные значения для весов (наклон)
    b = -1.0  # Начальное смещение
    learning_rate = 0.1
    max_iterations = 1000

    # Обучение
    for _ in range(max_iterations):
        misclassified = False
        for i in range(len(X)):
            if (y[i] == 1 and np.dot(w, X[i]) + b <= 0) or (y[i] == -1 and np.dot(w, X[i]) + b > 0):
                # Обновление весов и смещения
                if y[i] == 1:
                    w += learning_rate * X[i]
                    b += learning_rate
                else:
                    w -= learning_rate * X[i]
                    b -= learning_rate
                misclassified = True

        if not misclassified:
            break

    return w, b


# Преобразуем классы для Хо-Кашьяпа (например, 1 и -1)
binary_classes = np.where(y == 1, 1, -1)

# Обучаем алгоритм Хо-Кашьяпа
weights, bias = ho_kashyap(X, binary_classes)

# Создаем график
plt.figure(figsize=(8, 6))

# Отображаем точки с учетом класса
for class_num in set(classes):
    indices = [i for i, c in enumerate(classes) if c == class_num]
    plt.scatter([x_coords[i] for i in indices], [y_coords[i] for i in indices],
                color=colors.get(class_num, 'black'),
                marker='o', label=f'Класс {class_num}')

# Отображение гиперплоскости
x_min, x_max = plt.xlim()
y_min = -(weights[0] * x_min + bias) / weights[1]
y_max = -(weights[0] * x_max + bias) / weights[1]
plt.plot([x_min, x_max], [y_min, y_max], 'k--', label='Гиперплоскость')

# Вывод информации о расстояниях
print("Средние расстояния между классами:")
for i in range(1, len(classes) + 1):
    print(f"Класс {i}:")
    print(f"  Среднее Евклидово расстояние: {distances[f'class_{i}_Average Euclidean Distance']}")
    print(f"  Среднее Манхэттенское расстояние: {distances[f'class_{i}_Average Manhattan Distance']}")

# Настраиваем график
plt.title('Двумерный график точек с гиперплоскостью')
plt.xlabel('Ось X')
plt.ylabel('Ось Y')
plt.grid(True)
plt.legend()

# Показываем график
plt.show()