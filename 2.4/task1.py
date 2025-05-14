"""
Задание 1.
Разработайте приложение по работе со студентами. Приложение
должно хранить данные о студентах в базе данных. Сущность
студента должна описываться в виде класса, у которого будут
следующие поля:
1) Имя
2) Фамилия
3) Отчество
4) Группа
5) Оценки(массив из 4 элементов)
В приложении должен быть следующий функционал:
1) Добавление нового студента
2) Просмотр всех студентов
3) Просмотр одного студента, включая его средний балл
4) Редактирование студента
5) Удаление студента
6) Просмотр среднего балла студентов у конкретной группы
"""
import sqlite3 as sq

class Student(object):
    def __init__(self, name, surname, patronymic, group_name, grades):
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.group_name = group_name
        self.grades = list(grades)

class StudentWorkApplication(object):
    def __init__(self, db_name="students.db"):
        self.con = sq.connect(db_name)
        self.cur = self.con.cursor()
        self._create_table()

    def _create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                patronymic TEXT,
                group_name TEXT NOT NULL,
                grade1 INTEGER,
                grade2 INTEGER,
                grade3 INTEGER,
                grade4 INTEGER)
        """)
        self.con.commit()
    def add_student(self, student: Student):
        if len(student.grades) != 4:
            raise ValueError("Должно быть 4 оценки!")

        self.cur.execute("""
        INSERT INTO students
        (name, surname, patronymic, group_name, grade1, grade2, grade3, grade4)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student.name,
            student.surname,
            student.patronymic,
            student.group_name,
            *student.grades
        ))
        self.con.commit()

    def get_all_students(self):
        self.cur.execute('SELECT * FROM students')
        return self.cur.fetchall()

    def get_student(self, student_id):
        self.cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student_data = self.cur.fetchone()
        if not student_data:
            return None

        grades = student_data[5:9]
        avg_grade = sum(grades) / len(grades) if grades else 0
        return student_data, avg_grade

    def update_student(self, student_id, student: Student):
        if len(student.grades) != 4:
            raise ValueError("Должно быть 4 оценки")
        self.cur.execute('''
            UPDATE students 
            SET name = ?, surname = ?, patronymic = ?, group_name = ?,
                grade1 = ?, grade2 = ?, grade3 = ?, grade4 = ?
            WHERE id = ?
        ''', (
            student.name,
            student.surname,
            student.patronymic,
            student.group_name,
            *student.grades,
            student_id
        ))
        self.con.commit()

    def delete_student(self, student_id):
        self.cur.execute('DELETE FROM students WHERE id = ?', (student_id,))
        self.con.commit()

    def get_group_average(self, group_name):
        self.cur.execute('''
            SELECT grade1, grade2, grade3, grade4 
            FROM students 
            WHERE group_name = ?
        ''', (group_name,))

        all_grades = []
        for row in self.cur.fetchall():
            all_grades.extend(row)

        if not all_grades:
            return 0

        return sum(all_grades) / len(all_grades)

    def close(self):
        self.con.close()

def main():
    application = StudentWorkApplication()

    while True:
        print("\nМеню:")
        print("1. Добавить студента")
        print("2. Просмотреть всех студентов")
        print("3. Просмотреть одного студента")
        print("4. Редактировать студента")
        print("5. Удалить студента")
        print("6. Просмотреть средний балл группы")
        print("7. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Имя: ")
            surname = input("Фамилия: ")
            patronymic = input("Отчество: ")
            group_name = input("Группа: ")
            grades = []
            for i in range(4):
                grade = int(input(f"Оценка {i + 1}: "))
                grades.append(grade)

            student = Student(name, surname, patronymic, group_name, grades)
            application.add_student(student)
            print("Студент добавлен!")
        elif choice == "2":
            students = application.get_all_students()
            if not students:
                print("Нет студентов в базе")
            else:
                print("\nСписок студентов:")
                for student in students:
                    print(f"ID: {student[0]}, {student[2]} {student[1]} {student[3]}, Группа: {student[4]}")

        elif choice == "3":
            student_id = int(input("Введите ID студента: "))
            student_data = application.get_student(student_id)
            if not student_data:
                print("Студент не найден")
            else:
                student, avg_grade = student_data
                print(f"\nID: {student[0]}")
                print(f"ФИО: {student[2]} {student[1]} {student[3]}")
                print(f"Группа: {student[4]}")
                print(f"Оценки: {student[5]}, {student[6]}, {student[7]}, {student[8]}")
                print(f"Средний балл: {avg_grade:.2f}")

        elif choice == "4":
            student_id = int(input("Введите ID студента для редактирования: "))
            student_data = application.get_student(student_id)
            if not student_data:
                print("Студент не найден")
            else:
                print("Введите новые данные (оставьте пустым, чтобы не изменять):")
                first_name = input(f"Имя [{student_data[0][1]}]: ") or student_data[0][1]
                last_name = input(f"Фамилия [{student_data[0][2]}]: ") or student_data[0][2]
                middle_name = input(f"Отчество [{student_data[0][3]}]: ") or student_data[0][3]
                group = input(f"Группа [{student_data[0][4]}]: ") or student_data[0][4]

                grades = []
                for i in range(4):
                    grade = input(f"Оценка {i + 1} [{student_data[0][5 + i]}]: ")
                    grades.append(int(grade) if grade else student_data[0][5 + i])

                student = Student(first_name, last_name, middle_name, group, grades)
                application.update_student(student_id, student)
                print("Данные студента обновлены!")

        elif choice == "5":
            student_id = int(input("Введите ID студента для удаления: "))
            application.delete_student(student_id)
            print("Студент удален!")

        elif choice == "6":
            group = input("Введите название группы: ")
            avg = application.get_group_average(group)
            print(f"Средний балл группы {group}: {avg:.2f}")

        elif choice == "7":
            application.close()
            print("Выход из программы")
            break

        else:
            print("Неверный ввод, попробуйте снова")
if __name__ == "__main__":
    main()