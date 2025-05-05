"""
Задание 4. Описать класс, реализующий счетчик, который может увеличивать или
уменьшать свое значение на единицу. Предусмотреть инициализацию счетчика со
значением по умолчанию и произвольным значением. Счетчик имеет два метода:
увеличения и уменьшения, — и свойство, позволяющее получить его текущее состояние.
Написать программу, демонстрирующую все возможности класса
"""
import random
class Counter(object):
    def __init__(self, value = random.randrange(0, 101)):
        self.value = value
    def increase(self):
        self.value += 1
    def decrease(self):
        self.value -= 1
    def display_value(self):
        return self.value
counter = Counter() # определение объекта counter
counter.increase() # увеличение значения на 1
counter.decrease() # уменьшение значения на 1
print(counter.value) # получение текущего состояния счетчика
