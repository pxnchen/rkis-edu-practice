"""
Задание 5. Создать класс с двумя свойствами. Добавить конструктор с входными
параметрами. Добавить конструктор, инициализирующий свойства по умолчанию.
Добавить деструктор, выводящий на экран сообщение об удалении объекта. Написать
программу, демонстрирующую все возможности класса
"""
class Class(object):
    def __init__(self, name="Nikolay", age=20):
        self.name = name
        self.age = age
    def display_info(self):
        print(f"Имя: {self.name}\tВозраст: {self.age}")
    def __del__(self):
        print('Удаляется объект {} класса SomeClass'.format(self.name))
obj = Class()
obj.display_info()
del obj