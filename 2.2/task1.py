"""
Задание 1. Создайте класс с именем Student, содержащий свойства: фамилия, дата
рождения, номер группы, успеваемость (массив из пяти элементов). Добавить возможность
изменения фамилии, даты рождения и номера группы. Добавить возможность вывода
информации о студенте, фамилия и дата рождения которого введены пользователем.
Написать программу, демонстрирующую все возможности класса
"""

class Student:
    def __init__(self,surname, birth_date, group_num, achievement):
        self.surname = surname
        self.birth_date = birth_date
        self.group_num = group_num
        if len(achievement) == 5:
            self.achievement = achievement
        else:
            self.achievement = [0]*5
    def change_sn(self, sn):
        self.surname = sn
    def change_bd(self, bd):
        self.birth_date = bd
    def change_gr(self, gr):
        self.group_num = gr
    def print_student(self):
        print(f"Фамилия: {self.surname}")
        print(f"Дата рождения: {self.birth_date}")
        print(f"Номер группы: {self.group_num}")
        print(f"Успеваемость: {', '.join(map(str, self.achievement))}")

    @staticmethod
    def find_student(students, surname, birth_date):
        for student in students:
            if student.surname == surname and student.birth_date == birth_date:
                return student
        return None

students = [
    Student("Панченко", "24.01.2005", 722, [5, 4, 5, 4, 5]),
    Student("Сабельфельд", "07.05.2007", 632, [4, 4, 3, 5, 4]),
    Student("Узолин", "19.08.2007", 622, [5, 5, 5, 5, 5])
]
print("Демонстрация возможностей класса Student\n")

print("1. Изменение данных студента:")
student = students[0]
print("До изменения:")
student.print_student()

student.change_sn("Дудецкая")
student.change_bd("31.07.2006")
student.change_gr(932)

print("\nПосле изменения:")
student.print_student()

print("\n2. Поиск студента:")
search_surname = input("Введите фамилию студента: ")
search_birth_date = input("Введите дату рождения (DD.MM.YYYY): ")

found_student = Student.find_student(students, search_surname, search_birth_date)

if found_student:
    print("\nНайден студент:")
    found_student.print_student()
else:
    print("\nСтудент не найден.")

print("\n3. Список всех студентов:")
for i, student in enumerate(students, 1):
    print(f"\nСтудент №{i}:")
    student.print_student()