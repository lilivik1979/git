#include <iostream> // Подключает стандартную библиотеку ввода/вывода (cout, cin, cerr)
#include <fstream> // Подключает библиотеку для работы с файлами (ifstream, ofstream)
#include <vector> // Подключает библиотеку для работы с динамическими массивами (vector)
#include <cmath> // Подключает математическую библиотеку (sqrt, pow)
#include <cstdlib> // Подключает библиотеку функций из C (rand, srand)
#include <ctime> // Подключает библиотеку для работы со временем (time)
#include <algorithm> // Подключает библиотеку со стандартными алгоритмами (min_element)
#include <limits> // Подключает библиотеку с предельными значениями (numeric_limits)

//Функция, которая реализует алгоритм ISODATA
void isodata(const std::vector<std::pair<double, double>> &points, int initial_k, const std::string &filename, int max_iter = 100, double tol = 1e-4)
{
    int n_points = points.size(); // Сохраняет количество точек в переменную n_points
    std::vector<std::pair<double, double>> centers(initial_k); // Создает вектор центров кластеров размером initial_k
    std::vector<int> labels(n_points); // Создает вектор меток кластеров размером n_points, которые изначально не определены

    // Инициализация центров кластеров случайными точками
    std::srand(42); // Устанавливает seed для генератора случайных чисел, обеспечивая воспроизводимость результатов
    for (int i = 0; i < initial_k; ++i) // Цикл по количеству начальных центров кластеров
    {
        int random_index = std::rand() % n_points; // Генерирует случайный индекс точки
        centers[i] = points[random_index]; // Устанавливает случайную точку в качестве центра кластера
    }

    for (int iteration = 0; iteration < max_iter; ++iteration) // Цикл итераций алгоритма
    {
        // Шаг 1: Присвоение меток кластерам
        std::vector<std::vector<double>> distances(n_points, std::vector<double>(initial_k)); // Создает матрицу расстояний между точками и центрами кластеров
        for (int i = 0; i < initial_k; ++i) // Цикл по центрам кластеров
        {
            for (int j = 0; j < n_points; ++j) // Цикл по точкам
            {
                distances[j][i] = std::sqrt(std::pow(points[j].first - centers[i].first, 2) + std::pow(points[j].second - centers[i].second, 2)); // Вычисляет евклидово расстояние между точкой и центром кластера
            }
        }

        for (int j = 0; j < n_points; ++j) // Цикл по точкам
        {
            labels[j] = std::min_element(distances[j].begin(), distances[j].end()) - distances[j].begin(); // Находит индекс минимального расстояния (номер кластера) для каждой точки
        }

        // Шаг 2: Обновление центров кластеров
        std::vector<std::pair<double, double>> new_centers(initial_k, {0.0, 0.0}); // Создает вектор новых центров кластеров
        std::vector<int> counts(initial_k, 0); // Создает вектор счетчиков точек в каждом кластере

        for (int j = 0; j < n_points; ++j) // Цикл по точкам
        {
            new_centers[labels[j]].first += points[j].first; // Суммирует координаты x точек в кластере
            new_centers[labels[j]].second += points[j].second; // Суммирует координаты y точек в кластере
            counts[labels[j]]++; // Увеличивает счетчик точек в кластере
        }

        for (int i = 0; i < initial_k; ++i) // Цикл по центрам кластеров
        {
            if (counts[i] > 0) // Проверка на то, что кластер не пустой
            {
                new_centers[i].first /= counts[i]; // Вычисляет среднее значение координаты x для центра кластера
                new_centers[i].second /= counts[i]; // Вычисляет среднее значение координаты y для центра кластера
            }
            else
            {
                new_centers[i] = centers[i]; // Если кластер пустой, оставляем старый центр
            }
        }

        // Проверка на сходимость
        double max_shift = 0.0; // Максимальное смещение центра кластера
        for (int i = 0; i < initial_k; ++i) // Цикл по центрам кластеров
        {
            max_shift = std::max(max_shift, std::sqrt(std::pow(new_centers[i].first - centers[i].first, 2) + std::pow(new_centers[i].second - centers[i].second, 2))); // Вычисляет максимальное смещение центра кластера между итерациями
        }

        if (max_shift < tol) // Проверка на сходимость алгоритма
        {
            break; // Выход из цикла, если алгоритм сошелся
        }

        centers = new_centers; // Обновление центров кластеров
    }

    // Сохранение результатов в файл
    std::ofstream outfile(filename); // Открытие файла для записи результатов
    for (int j = 0; j < n_points; ++j) // Цикл по точкам
    {
        outfile << points[j].first << " " << points[j].second << " " << labels[j] + 1 << std::endl; // Запись координат точки и номера кластера в файл
    }

    // Сохранение центров кластеров
    for (const auto &center : centers) // Цикл по центрам кластеров
    {
        outfile << center.first << " " << center.second << " " << 4 << std::endl; // Запись координат центра кластера в файл
    }
}

int main()
{
    std::ifstream infile("data.txt"); // Открытие файла с данными
    std::vector<std::pair<double, double>> points; // Создание вектора для хранения точек

    double x, y; // Переменные для хранения координат точки
    int class_label; // Переменная для хранения номера класса (игнорируется)

    while (infile >> x >> y >> class_label) // Цикл чтения данных из файла
    {
        points.emplace_back(x, y); // Добавление точки в вектор
    }

    int initial_k = 3; // Задание начального количества кластеров
    isodata(points, initial_k, "result.txt"); // Вызов функции isodata для выполнения кластеризации
    return 0; // Возврат 0, если программа выполнилась успешно
}
