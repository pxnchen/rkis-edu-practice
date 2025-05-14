"""
Задание 3.
Для данного задания требуется ознакомиться со следующим
материалом:
1) https://docs-python.ru/packages/modul-psutil-python/
Разработайте приложение Системный монитор. Приложение должно
давать следующую информацию:
1) Мониторинг загрузки CPU
2) Мониторинг использованной оперативной памяти
3) Процентное соотношение загруженности диска
Все данные должны сохраняться в базу данных со временем, когда
был проведен мониторинг компьютера.
Так же должна быть возможность посмотреть сохраненные данные
"""
import sqlite3 as sq
import psutil
from datetime import datetime

class SystemMonitor(object):
    def __init__(self, db_name='monitor.db'):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with sq.connect(self.db_name) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS system_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    cpu_percent REAL NOT NULL,
                    memory_percent REAL NOT NULL,
                    disk_percent REAL NOT NULL
                )
            ''')
            conn.commit()

    def collect_data(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        with sq.connect(self.db_name) as conn:
            conn.execute('''
                INSERT INTO system_stats (timestamp, cpu_percent, memory_percent, disk_percent)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, cpu, memory, disk))
            conn.commit()


    def show_current_stats(self):
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        print("\nТекущее состояние системы:")
        print(f"CPU: {cpu}%")
        print(f"Память: {memory.percent}% ({memory.used // (1024 ** 2)}/{memory.total // (1024 ** 2)} MB)")
        print(f"Диск: {disk.percent}% ({disk.used // (1024 ** 3)}/{disk.total // (1024 ** 3)} GB)")

    def show_history(self, hours=24):
        with sq.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, cpu_percent, memory_percent, disk_percent
                FROM system_stats
                WHERE timestamp >= datetime('now', ?)
                ORDER BY timestamp
            ''', (f'-{hours} hours',))

            print(f"\nИстория за последние {hours} часов:")
            print("Дата/Время | CPU% | Память% | Диск%")
            print("-----------------------------------------")
            for row in cursor.fetchall():
                print(f"{row[0][11:19]} | {row[1]:4.1f} | {row[2]:7.1f} | {row[3]:5.1f}")

def main():
    monitor = SystemMonitor()
    while True:
        print("\n=== Cистемный монитор ===")
        print("1. Показать текущее состояние")
        print("2. Собрать и сохранить данные")
        print("3. Показать историю")
        print("4. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            monitor.show_current_stats()
        elif choice == "2":
            monitor.collect_data()
            print("Данные сохранены!")
        elif choice == "3":
            try:
                hours = int(input("За сколько часов показать историю? ") or 24)
                monitor.show_history(hours)
            except ValueError:
                print("Ошибка: введите число")
        elif choice == "4":
            print("Выход из программы")
            break

if __name__ == "__main__":
    main()



