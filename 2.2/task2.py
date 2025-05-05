"""
Задание 2. Создайте класс с именем Train, содержащий свойства: название пункта
назначения, номер поезда, время отправления. Добавить возможность вывода
информации о поезде, номер которого введен пользователем. Написать программу,
демонстрирующую все возможности класса
"""

from datetime import time

class Train:
    def __init__(self, destination, train_num, departure_time):
        self.des = destination
        self.tn = train_num
        self.dt = time(departure_time)
    def print_train(self):
        print(f"Пункт назначения: {self.des}")
        print(f"Номер поезда: {self.tn}")
        print(f"Время отправления: {self.dt}")

    @staticmethod
    def find_train(trains, tn):
        for train in trains:
            if train.tn == tn:
                return train
        return None

trains = [
    Train("Томск", "1", 10),
    Train("Новосибирск", "2", 11),
    Train("Красноярск", "3", 12)
]
print("Демонстрация возможностей класса Student\n")
print("Поиск поезда")

search_train_num = input("Введите номер поезда: ")

found_train = Train.find_train(trains, search_train_num)

if found_train:
    print("\nПоезд найден:")
    found_train.print_train()
else:
    print("\nПоезд не найден.")

print("\nСписок всех поездов:")
for i, train  in enumerate(trains, 1):
    print(f"\tПоезд №{i}:")
    train.print_train()