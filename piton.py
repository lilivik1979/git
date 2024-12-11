import matplotlib.pyplot as plt
import numpy as np

# Чтение данных из файла results.txt
try:
    data = np.loadtxt("results.txt", delimiter=" ")
    x1 = data[:, 0]
    x2 = data[:, 1]
    y = data[:, 2]
except FileNotFoundError:
    print("Ошибка: файл results.txt не найден.")
    exit()

# Разделение данных по классам
x1_class1 = x1[y == 1]
x2_class1 = x2[y == 1]
x1_class_minus1 = x1[y == -1]
x2_class_minus1 = x2[y == -1]

# Чтение весов из файла weights.txt (если существует)
try:
    with open("weights.txt", "r") as f:
        w0, w1, _ = map(float, f.readline().split())  # _ игнорирует предсказанный класс
    
    # Рисуем разделяющую прямую (гиперплоскость)
    x_values = np.array([0, 1])
    y_values = -(w0 * x_values) / w1  # y = -(w0*x + bias)/w1 (bias считается нулевым для простоты)
    plt.plot(x_values, y_values, 'k--', label='Разделяющая прямая')
except FileNotFoundError:
    print("Предупреждение: файл weights.txt не найден. Разделяющая прямая не будет построена.")

# Построение графика
plt.figure(figsize=(8, 6))
plt.scatter(x1_class1, x2_class1, c='blue', label='Класс 1', marker='o')
plt.scatter(x1_class_minus1, x2_class_minus1, c='red', label='Класс -1', marker='x')
plt.xlabel("x1")
plt.ylabel("x2")
plt.title("Визуализация результатов классификации")
plt.legend()
plt.grid(True)
plt.show()