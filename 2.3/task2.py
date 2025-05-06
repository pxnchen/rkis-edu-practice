"""
Задание 2. Модифицируйте класс Worker из предыдущей задачи, сделайте все его
свойства приватными, а для их чтения сделайте методы-геттеры
"""

class Worker(object):
    def __init__(self, name, surname, rate, days):
        self.__nm = name
        self.__snm = surname
        self.__rt = rate
        self.__days = days
    def get_name(self): # метод-геттер для чтения имени
        return self.__nm
    def get_surname(self): # метод-геттер для чтения фамилии
        return self.__snm
    def get_rate(self): # метод-геттер для чтения ставки
        return self.__rt
    def get_days(self): # метод-геттер для чтения количества дней
        return self.__days
    def print_worker(self):
        print(f"Имя: {self.__nm}\tФамилия: {self.__snm}\tСтавка за день работы: {self.__rt}\tКоличество отработанных дней: {self.__days}")
    def GetSalary(self):
        print(f"Зарплата работника: {self.__rt * self.__days}")

worker = Worker("Николай", "Панченко", 2640, 13) # определение объекта worker
print(worker.get_name()) #  Николай (обращение к геттеру)
print(worker.get_surname()) # Панченко (обращение к геттеру)
print(worker.get_rate()) # 2640 (обращение к геттеру)
print(worker.get_days()) # 13 (обращение к геттеру)
worker.print_worker() # вывод информации о работнике
worker.GetSalary() # вывод зарплаты работника