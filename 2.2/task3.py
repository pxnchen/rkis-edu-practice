"""
Задание 3. Создайте класс с двумя свойствами для хранения целых чисел. Добавить
метод для вывода на экран и метод для изменения этих чисел. Добавить метод, который
находит сумму значений этих чисел и метод, который находит наибольшее значение из
этих чисел. Написать программу, демонстрирующую все возможности класса
"""

class Class(object):
    def __init__(self, int_storage1, int_storage2):
        self.pr1 = int_storage1 # первое свойство для хранения целого числа
        self.pr2 = int_storage2 # второе свойство для хранения целого числа
    def display_info(self):
        print(f"Число 1: {self.pr1}\tЧисло 2: {self.pr2}")
    def change_of_number(self, pr1, pr2):
        self.pr1 = pr1
        self.pr2 = pr2
    def sum(self):
        return self.pr1 + self.pr2
    def max(self):
        return max(self.pr1, self.pr2)
numbers = Class(8, 9) # определение объекта numbers
numbers.display_info() # вывод на экран
numbers.change_of_number(3, 4) # изменение чисел
print(numbers.sum()) # сумма
print(numbers.max()) # максимальное число