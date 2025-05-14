"""
Задание 2.
Разработайте приложение „I love drink“, со следующим
функционалом:
1) Учет напитков:
1.1) Хранение данных об алкогольных напитках и ингредиентах
1.2) Учет остатков на складе
2) Управление коктейлями:
2.1) Хранение данных о коктейлях(название,
крепость(автоматический расчет исходя из крепости алкогольных
напитков), состав, цена)
3) Операции
3.1) Продажа коктейлей и алкогольных напитков
3.2) Пополнение запасов
В приложении должна использоваться база данных для хранения
информации.
"""
import sqlite3 as sq
from dataclasses import dataclass
from typing import Dict, List

@dataclass()
class Drink:
    id: int = None
    name: str = ""
    alcohol_percent: float = 0.0
    volume_ml: int = 0
    price: float = 0.0
    quantity: int = 0

@dataclass()
class Cocktail:
    id: int = None
    name: str = ""
    strength: float = 0.0
    ingredients: Dict[str, int] = None
    price: float = 0.0

class BarManager:
    def __init__(self, db_name='bar.db'):
        self.conn = sq.connect(db_name)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS drinks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                alcohol_percent REAL NOT NULL,
                volume_ml INTEGER NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cocktails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                strength REAL NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cocktail_ingredients (
                cocktail_id INTEGER NOT NULL,
                drink_id INTEGER NOT NULL,
                volume_ml INTEGER NOT NULL,
                FOREIGN KEY (cocktail_id) REFERENCES cocktails (id),
                FOREIGN KEY (drink_id) REFERENCES drinks (id),
                PRIMARY KEY (cocktail_id, drink_id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_type TEXT NOT NULL,  -- 'drink' или 'cocktail'
                item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_drink(self, drink: Drink):
        self.cursor.execute('''
            INSERT INTO drinks (name, alcohol_percent, volume_ml, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (drink.name, drink.alcohol_percent, drink.volume_ml, drink.price, drink.quantity))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_drink(self, drink_id: int) -> Drink:
        self.cursor.execute('SELECT * FROM drinks WHERE id = ?', (drink_id,))
        row = self.cursor.fetchone()
        if row:
            return Drink(*row)
        return None

    def update_drink(self, drink: Drink):
        self.cursor.execute('''
            UPDATE drinks 
            SET name = ?, alcohol_percent = ?, volume_ml = ?, price = ?, quantity = ?
            WHERE id = ?
        ''', (drink.name, drink.alcohol_percent, drink.volume_ml, drink.price, drink.quantity, drink.id))
        self.conn.commit()

    def get_all_drinks(self) -> List[Drink]:
        self.cursor.execute('SELECT * FROM drinks')
        return [Drink(*row) for row in self.cursor.fetchall()]

    def add_cocktail(self, cocktail: Cocktail) -> int:
        self.cursor.execute('''
            INSERT INTO cocktails (name, strength, price)
            VALUES (?, ?, ?)
        ''', (cocktail.name, cocktail.strength, cocktail.price))
        cocktail_id = self.cursor.lastrowid

        for drink_name, volume_ml in cocktail.ingredients.items():
            drink_id = self._get_drink_id_by_name(drink_name)
            if drink_id:
                self.cursor.execute('''
                    INSERT INTO cocktail_ingredients (cocktail_id, drink_id, volume_ml)
                    VALUES (?, ?, ?)
                ''', (cocktail_id, drink_id, volume_ml))

        self.conn.commit()
        return cocktail_id

    def _get_drink_id_by_name(self, name: str) -> int:
        self.cursor.execute('SELECT id FROM drinks WHERE name = ?', (name,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_cocktail(self, cocktail_id: int) -> Cocktail:
        self.cursor.execute('SELECT * FROM cocktails WHERE id = ?', (cocktail_id,))
        row = self.cursor.fetchone()
        if not row:
            return None

        self.cursor.execute('''
            SELECT d.name, ci.volume_ml 
            FROM cocktail_ingredients ci
            JOIN drinks d ON ci.drink_id = d.id
            WHERE ci.cocktail_id = ?
        ''', (cocktail_id,))
        ingredients = {row[0]: row[1] for row in self.cursor.fetchall()}

        return Cocktail(id=row[0], name=row[1], strength=row[2], price=row[3], ingredients=ingredients)

    def get_all_cocktails(self) -> List[Cocktail]:
        self.cursor.execute('SELECT id FROM cocktails')
        return [self.get_cocktail(row[0]) for row in self.cursor.fetchall()]

    def calculate_cocktail_strength(self, ingredients: Dict[str, int]) -> float:
        total_alcohol = 0
        total_volume = 0

        for drink_name, volume_ml in ingredients.items():
            self.cursor.execute('SELECT alcohol_percent FROM drinks WHERE name = ?', (drink_name,))
            row = self.cursor.fetchone()
            if row:
                alcohol_percent = row[0]
                total_alcohol += (alcohol_percent / 100) * volume_ml
                total_volume += volume_ml

        return (total_alcohol / total_volume) * 100 if total_volume > 0 else 0

    def sell_drink(self, drink_id: int, quantity: int):
        drink = self.get_drink(drink_id)
        if not drink:
            raise ValueError("Напиток не найден")

        if drink.quantity < quantity:
            raise ValueError("Недостаточно напитков на складе")

        drink.quantity -= quantity
        self.update_drink(drink)

        total_price = drink.price * quantity
        self.cursor.execute('''
            INSERT INTO sales (item_type, item_id, quantity, total_price)
            VALUES (?, ?, ?, ?)
        ''', ('drink', drink_id, quantity, total_price))
        self.conn.commit()

    def sell_cocktail(self, cocktail_id: int, quantity: int):
        cocktail = self.get_cocktail(cocktail_id)
        if not cocktail:
            raise ValueError("Коктейль не найден")

        for drink_name, volume_ml in cocktail.ingredients.items():
            drink_id = self._get_drink_id_by_name(drink_name)
            drink = self.get_drink(drink_id)
            if drink.quantity * drink.volume_ml < volume_ml * quantity:
                raise ValueError(f"Недостаточно ингредиента {drink_name} для приготовления")

        for drink_name, volume_ml in cocktail.ingredients.items():
            drink_id = self._get_drink_id_by_name(drink_name)
            drink = self.get_drink(drink_id)
            used_volume = volume_ml * quantity
            used_quantity = used_volume // drink.volume_ml
            if used_volume % drink.volume_ml != 0:
                used_quantity += 1
            drink.quantity -= used_quantity
            self.update_drink(drink)

        total_price = cocktail.price * quantity
        self.cursor.execute('''
            INSERT INTO sales (item_type, item_id, quantity, total_price)
            VALUES (?, ?, ?, ?)
        ''', ('cocktail', cocktail_id, quantity, total_price))
        self.conn.commit()

    def restock_drink(self, drink_id: int, quantity: int):
        drink = self.get_drink(drink_id)
        if not drink:
            raise ValueError("Напиток не найден")

        drink.quantity += quantity
        self.update_drink(drink)
        self.conn.commit()

    def get_inventory(self):
        self.cursor.execute('SELECT name, quantity FROM drinks')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


def main():
    manager = BarManager()

    while True:
        print("\n=== I love drink ===")
        print("1. Учет напитков")
        print("2. Управление коктейлями")
        print("3. Операции")
        print("4. Выход")

        choice = input("Выберите раздел: ")

        if choice == "1":
            while True:
                print("\nУчет напитков:")
                print("1. Добавить напиток")
                print("2. Просмотреть все напитки")
                print("3. Редактировать напиток")
                print("4. Пополнить запас")
                print("5. Назад")

                sub_choice = input("Выберите действие: ")

                if sub_choice == "1":
                    name = input("Название: ")
                    alcohol = float(input("Крепость (%): "))
                    volume = int(input("Объем (мл): "))
                    price = float(input("Цена: "))
                    quantity = int(input("Количество: "))

                    drink = Drink(name=name, alcohol_percent=alcohol, volume_ml=volume, price=price, quantity=quantity)
                    manager.add_drink(drink)
                    print("Напиток добавлен!")

                elif sub_choice == "2":
                    drinks = manager.get_all_drinks()
                    print("\nСписок напитков:")
                    for drink in drinks:
                        print(f"{drink.id}. {drink.name} ({drink.alcohol_percent}%), {drink.volume_ml}мл, {drink.price}₽, {drink.quantity}шт")

                elif sub_choice == "3":
                    drink_id = int(input("ID напитка для редактирования: "))
                    drink = manager.get_drink(drink_id)
                    if not drink:
                        print("Напиток не найден")
                    else:
                        print(
                            f"Текущие данные: {drink.name}, {drink.alcohol_percent}%, {drink.volume_ml}мл, {drink.price}₽, {drink.quantity}шт")
                        name = input(f"Название [{drink.name}]: ") or drink.name
                        alcohol = input(f"Крепость (%) [{drink.alcohol_percent}]: ") or drink.alcohol_percent
                        volume = input(f"Объем (мл) [{drink.volume_ml}]: ") or drink.volume_ml
                        price = input(f"Цена [{drink.price}]: ") or drink.price

                        updated_drink = Drink(
                            id=drink.id,
                            name=name,
                            alcohol_percent=float(alcohol),
                            volume_ml=int(volume),
                            price=float(price),
                            quantity=drink.quantity
                        )
                        manager.update_drink(updated_drink)
                        print("Данные обновлены!")

                elif sub_choice == "4":
                    drink_id = int(input("ID напитка: "))
                    quantity = int(input("Количество для пополнения: "))
                    manager.restock_drink(drink_id, quantity)
                    print("Запас пополнен!")

                elif sub_choice == "5":
                    break

        elif choice == "2":
            while True:
                print("\nУправление коктейлями:")
                print("1. Добавить коктейль")
                print("2. Просмотреть все коктейли")
                print("3. Просмотреть состав коктейля")
                print("4. Назад")

                sub_choice = input("Выберите действие: ")

                if sub_choice == "1":
                    name = input("Название коктейля: ")

                    ingredients = {}
                    while True:
                        drink_name = input("Название напитка (или пусто для завершения): ")
                        if not drink_name:
                            break
                        volume = int(input("Объем (мл): "))
                        ingredients[drink_name] = volume

                    if not ingredients:
                        print("Нужно добавить хотя бы один ингредиент!")
                        continue

                    strength = manager.calculate_cocktail_strength(ingredients)
                    print(f"Крепость коктейля: {strength:.1f}%")

                    price = float(input("Цена коктейля: "))

                    cocktail = Cocktail(name=name, strength=strength, ingredients=ingredients, price=price)
                    manager.add_cocktail(cocktail)
                    print("Коктейль добавлен!")

                elif sub_choice == "2":
                    cocktails = manager.get_all_cocktails()
                    print("\nСписок коктейлей:")
                    for cocktail in cocktails:
                        print(f"{cocktail.id}. {cocktail.name} ({cocktail.strength:.1f}%), {cocktail.price}₽")

                elif sub_choice == "3":
                    cocktail_id = int(input("ID коктейля: "))
                    cocktail = manager.get_cocktail(cocktail_id)
                    if not cocktail:
                        print("Коктейль не найден")
                    else:
                        print(f"\nСостав коктейля '{cocktail.name}':")
                        for drink, volume in cocktail.ingredients.items():
                            print(f"- {drink}: {volume}мл")
                        print(f"Крепость: {cocktail.strength:.1f}%")
                        print(f"Цена: {cocktail.price}₽")

                elif sub_choice == "4":
                    break

        elif choice == "3":
            while True:
                print("\nОперации:")
                print("1. Продать напиток")
                print("2. Продать коктейль")
                print("3. Просмотреть остатки")
                print("4. Назад")

                sub_choice = input("Выберите действие: ")

                if sub_choice == "1":
                    drink_id = int(input("ID напитка: "))
                    quantity = int(input("Количество: "))
                    try:
                        manager.sell_drink(drink_id, quantity)
                        print("Продажа оформлена!")
                    except ValueError as e:
                        print(f"Ошибка: {e}")

                elif sub_choice == "2":
                    cocktail_id = int(input("ID коктейля: "))
                    quantity = int(input("Количество: "))
                    try:
                        manager.sell_cocktail(cocktail_id, quantity)
                        print("Продажа оформлена!")
                    except ValueError as e:
                        print(f"Ошибка: {e}")

                elif sub_choice == "3":
                    inventory = manager.get_inventory()
                    print("\nОстатки на складе:")
                    for name, quantity in inventory:
                        print(f"- {name}: {quantity}шт")

                elif sub_choice == "4":
                    break

        elif choice == "4":
            manager.close()
            print("До свидания!")
            break


if __name__ == "__main__":
    main()