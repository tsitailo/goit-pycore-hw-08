"""Клас для зберігання та управління записами."""
import pickle

from collections import UserDict
from datetime import timedelta, date, datetime
from pathlib import Path
from .record import Record


class AddressBook(UserDict):
    """
    Клас для зберігання та управління записами контактів.

    Наслідується від UserDict для зручної роботи зі словником.
    Ключем є ім'я контакту, значенням - об'єкт Record.
    """
    def add_record(self, record):
        """
        Додавання запису до адресної книги.

        Args:
            record (Record): Запис для додавання

        Note:
            Якщо запис з таким ім'ям вже існує, він буде перезаписаний
        """
        if not isinstance(record, Record):
            raise TypeError("Only Record instances can be added")
        self.data[record.name.value] = record

    def get_upcoming_birthdays(self, days=7):
        """
        Знаходить контакти з днями народження в найближчі days днів.

        Args:
            days (int): Кількість днів для перевірки (за замовчуванням 7)

        Returns:
            list[dict]: Список словників з іменем та датою вітання
                       [{"name": "John", "congratulation_date": "2025.10.30"}, ...]
        """
        today = datetime.today().date()
        horizon = today + timedelta(days=days)
        result = []

        for record in self.data.values():
            # Пропускаємо записи без дня народження
            if not record.birthday:
                continue

            birthday = record.birthday.value

            year = today.year
            try:
                birthday_this_year = birthday.replace(year=year)
            except ValueError:
                # Для 29 лютого у невисокосний рік
                birthday_this_year = date(year, 2, 28)

            if birthday_this_year < today:
                year += 1
                try:
                    birthday_this_year = birthday.replace(year=year)
                except ValueError:
                    birthday_this_year = date(year, 2, 28)

            if today <= birthday_this_year <= horizon:
                congratulation_date = birthday_this_year

                # Переносимо вітання з вихідних на понеділок
                if congratulation_date.weekday() == 5:  # субота
                    congratulation_date = congratulation_date + timedelta(days=2)
                elif congratulation_date.weekday() == 6:  # неділя
                    congratulation_date = congratulation_date + timedelta(days=1)

                result.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })

        return result

    def find(self, name):
        """
        Пошук запису за іменем.

        Args:
            name: Ім'я контакту для пошуку

        Returns:
            Record: Знайдений запис або None якщо не знайдено
        """
        return self.data.get(name)

    def delete(self, name):
        """
        Видалення запису за іменем.

        Args:
            name: Ім'я контакту для видалення

        Raises:
            KeyError: Якщо контакт не знайдено
        """
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact {name} not found")

    def change(self, name: str, new_phone: str) -> bool:
        """
        Змінює номер телефону для існуючого контакту.

        Args:
            name: Ім'я контакту  
            new_phone: Новий номер телефону для встановлення

        Returns:
            True якщо контакт знайдено і телефон змінено, False в іншому випадку

        Raises:
            ValueError: Якщо новий номер телефону недійсний
        """
        record = self.find(name)
        if record is None:
            return False

        record.phones.clear()
        record.add_phone(new_phone)

        return True

    def __str__(self):
        """
        Повертає строкове представлення адресної книги.

        Returns:
            str: Список всіх контактів
        """
        if not self.data:
            return "Address book is empty"
        return "\n".join(str(record) for record in self.data.values())

    def __repr__(self):
        """
        Повертає представлення об'єкта для розробників.

        Returns:
            str: Представлення об'єкта
        """
        return f"AddressBook(records={len(self.data)})"

    def __init__(self, filename="addressbook.pkl"):
        super().__init__()
        self.data = {}
        self.filename = filename

    def __enter__(self):
        """Завантажує дані при вході в context"""
        self.load_from_file(self.filename)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматично зберігає дані при виході"""
        self.save_to_file(self.filename)
        return False

    def save_to_file(self, filename=None):
        """Зберігає адресну книгу у файл"""
        if filename is None:
            filename = self.filename
        try:
            with open(filename, "wb") as file:
                pickle.dump(self.data, file)
            print(f"Адресну книгу збережено у файл {filename}")
        except Exception as e:
            print(f"Помилка при збереженні: {e}")

    def load_from_file(self, filename=None):
        """Завантажує адресну книгу з файлу"""
        if filename is None:
            filename = self.filename
        try:
            if Path(filename).exists():
                with open(filename, "rb") as file:
                    self.data = pickle.load(file)
                print(f"Адресну книгу завантажено з файлу {filename}")
                return True
            else:
                print(f"Файл {filename} не знайдено. Створено нову адресну книгу.")
                return False
        except Exception as e:
            print(f"Помилка при завантаженні: {e}")
            return False
