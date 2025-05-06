"""
Задание 1. Реализуйте класс Worker, который будет иметь следующие свойства: name,
surname, rate (ставка за день работы), days (количество отработанных дней). Также класс
должен иметь метод GetSalary(), который будет выводить зарплату работника. Зарплата -
это произведение ставки rate на количество отработанных дней days
"""
class Worker(object):
    def __init__(self, name, surname, rate, days):
        self.nm = name
        self.snm = surname
        self.rt = rate
        self.days = days
    def display_info(self):
        print(f"Имя: {self.nm}\tФамилия: {self.snm}\tСтавка за день работы: {self.rt}\tКоличество отработанных дней: {self.days}")
    def GetSalary(self):
        print("Зарплата работника: ", format(self.rt * self.days))

worker = Worker("Николай", "Панченко", 2640, 13) # определение объекта worker
worker.display_info() # вывод информации о работнике
worker.GetSalary() # вывод зарплаты работника
