#include <iostream>
#include <random>
#include <vector>
#include <fstream>
#include <cmath>
#include <locale> // For setlocale

// ... (классы Image и ImageContainer остаются без изменений) ...

class ImageClass
{
public:
    ImageClass(int quantity, int parameters, int min_value, int max_value)
        : container(quantity, parameters, min_value, max_value) {}

    void display() const
    {
        container.display();
    }

    void writeToFile(std::ofstream &output_file, int class_number) const
    {
        container.writeToFile(output_file, class_number);
    }

    std::vector<double> getEuclideanDistances() const {
        return container.calculateEuclideanDistances();
    }

    double averageEuclideanDistance() const {
        return container.averageEuclideanDistance();
    }

    double averageManhattanDistance() const {
        return container.averageManhattanDistance();
    }

    void writeDistancesToFile(const std::string& filename) const {
        std::ofstream distancesFile(filename);
        if (!distancesFile) {
            std::cerr << "Ошибка открытия файла: " << filename << std::endl;
            return;
        }

        distancesFile << "Average Euclidean Distance: " << averageEuclideanDistance() << std::endl;
        distancesFile << "Average Manhattan Distance: " << averageManhattanDistance() << std::endl;

        distancesFile.close();
    }

    const ImageContainer& getContainer() const {
        return container;
    } 

private:
    ImageContainer container;
};

class ImageClassContainer
{
public:
    void run()
    {
        int class_nums;
        std::cout << "Введите количество классов: ";
        std::cin >> class_nums;

        std::ofstream output_file("result.txt");
        if (!output_file)
        {
            std::cerr << "Ошибка при открытии файла!" << std::endl;
            return;
        }

        std::vector<ImageClass> classes;
        for (int i = 0; i < class_nums; i++)
        {
            int quantity, parameters, min_value, max_value;

            std::cout << "Введите количество элементов в классе: ";
            std::cin >> quantity;
            std::cout << "Введите количество измерений в классе: ";
            std::cin >> parameters;
            std::cout << "Введите минимальное значение: ";
            std::cin >> min_value;
            std::cout << "Введите максимальное значение: ";
            std::cin >> max_value;

            ImageClass imageClass(quantity, parameters, min_value, max_value);
            classes.push_back(imageClass);

            std::cout << "Класс " << i + 1 << ":" << std::endl;
            imageClass.display();

            std::cout << "Среднее евклидово расстояние: " << imageClass.averageEuclideanDistance() << std::endl;
            std::cout << "Среднее манхэттенское расстояние: " << imageClass.averageManhattanDistance() << std::endl;

            imageClass.writeToFile(output_file, i + 1);
            // Write distances to a separate file
            imageClass.writeDistancesToFile("distances_" + std::to_string(i + 1) + ".txt");
        }

        output_file.close();

        // Calculate Euclidean distances between classes
        for (size_t i = 0; i < classes.size() - 1; ++i) {
            for (size_t j = i + 1; j < classes.size(); ++j) {
                // Используем getContainer() для доступа к контейнеру
                std::vector<double> distances = classes[i].getContainer().calculateEuclideanDistancesBetweenContainers(classes[j].getContainer());

                std::cout << "Среднее Евклидово расстояние между классами " << i + 1 << " и " << j + 1 << ": "
                          << average(distances) << std::endl;

                // You can further process the distances here, e.g., write them to a file, output statistics, etc.
            }
        }
    }

private:
    // Helper function to calculate the average of a vector
    double average(const std::vector<double>& values) const {
        if (values.empty()) {
            return 0.0; 
        }
        double sum = 0.0;
        for (const auto& value : values) {
            sum += value;
        }
        return sum / values.size();
    }
};

int main()
{
   
    setlocale(LC_ALL, "ru_RU.utf8");

    ImageClassContainer imageClassContainer;
    imageClassContainer.run();
    return 0;
}