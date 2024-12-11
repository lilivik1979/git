#include <iostream>
#include <random>
#include <vector>
#include <fstream>

class Image
{
public:
    Image(int parameters, int min_value, int max_value)
        : parameters(parameters), min_value(min_value), max_value(max_value)
    {
        generateValues();
    }

    void display() const
    {
        for (const auto &value : values)
        {
            std::cout << value << " ";
        }
        std::cout << std::endl;
    }

    const std::vector<int> &getValues() const
    {
        return values;
    }

private:
    int parameters;
    int min_value;
    int max_value;
    std::vector<int> values;

    void generateValues()
    {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(min_value, max_value);

        values.resize(parameters);
        for (int k = 0; k < parameters; k++)
        {
            values[k] = dis(gen);
        }
    }
};

class ImageContainer
{
public:
    ImageContainer(int quantity, int parameters, int min_value, int max_value)
    {
        for (int i = 0; i < quantity; ++i)
        {
            images.emplace_back(parameters, min_value, max_value);
        }
    }

    void display() const
    {
        for (const auto &image : images)
        {
            image.display();
        }
    }

    void writeToFile(std::ofstream &output_file, int class_number) const
    {
        for (const auto &image : images)
        {
            const auto &values = image.getValues();
            for (size_t k = 0; k < values.size(); ++k)
            {
                output_file << values[k];
                if (k < values.size() - 1)
                {
                    output_file << " ";
                }
            }
            output_file << " " << class_number << "\n";
        }
    }

private:
    std::vector<Image> images;
};

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
            imageClass.display();
            imageClass.writeToFile(output_file, i + 1);
        }

        output_file.close();
    }
};

int main()
{
    ImageClassContainer imageClassContainer;
    imageClassContainer.run();
    return 0;
}