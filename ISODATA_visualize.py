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
    # Добавьте больше классов и их цветов по мере необходимости
}

with open('result.txt', 'r') as file:
    for line in file:
        # Разделяем строку на значения и преобразуем их в целые числа
        x, y, class_num = map(float, line.split())
        x_coords.append(x)
        y_coords.append(y)
        classes.append(class_num)

# Создаем график
plt.figure(figsize=(8, 6))

# Отображаем точки с учетом класса
for class_num in set(classes):  # Уникальные номера классов
    indices = [i for i, c in enumerate(classes) if c == class_num]
    plt.scatter([x_coords[i] for i in indices], [y_coords[i] for i in indices],
                # Цвет по умолчанию черный
                color=colors.get(class_num, 'black'),
                marker='o', label=f'Класс {class_num}')

# Настраиваем график
plt.title('Двумерный график точек')
plt.xlabel('Ось X')
plt.ylabel('Ось Y')
plt.grid(True)
plt.legend()  # Добавляем легенду

# Показываем график
plt.show()
