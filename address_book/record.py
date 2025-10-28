"""Клас для зберігання інформації про контакт."""

from .birthday import Birthday
from .name import Name
from .phone import Phone


class Record:
    """
    Клас для зберігання інформації про контакт.

    Включає ім'я та список телефонів.

    Attributes:
        name (Name): Ім'я контакту
        phones (list[Phone]): Список телефонів контакту
        birthday (Birthday): День народження контакту
    """

    def __init__(self, name):
        """
        Ініціалізація запису контакту.

        Args:
            name: Ім'я контакту

        Raises:
            ValueError: Якщо ім'я не валідне
        """
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        """
        Додавання дня народження до запису.

        Args:
            birthday: День народження у форматі DD.MM.YYYY

        Raises:
            ValueError: Якщо дата не валідна або має неправильний формат
        """
        if not isinstance(birthday, str) or not all(part.isdigit() for part in birthday.split('.')):
            raise ValueError("Birthday must be a string in format DD.MM.YYYY")

        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        """
        Додавання телефону до запису.

        Args:
            phone: Номер телефону (10 цифр)

        Raises:
            ValueError: Якщо номер не валідний або не містить 10 цифр
        """
        if not isinstance(phone, str) or not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone must be a string of 10 digits")
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        """
        Видалення телефону з запису.

        Args:
            phone: Номер телефону для видалення

        Raises:
            ValueError: Якщо телефон не знайдено
        """
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError(f"Phone {phone} not found")

    def edit_phone(self, old_phone, new_phone):
        """
        Редагування телефону.

        Args:
            old_phone: Старий номер телефону
            new_phone: Новий номер телефону

        Raises:
            ValueError: Якщо старий номер не знайдено або новий номер не валідний
        """
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            # Валідуємо новий номер
            new_phone_obj = Phone(new_phone)
            # Замінюємо старий номер на новий
            index = self.phones.index(phone_obj)
            self.phones[index] = new_phone_obj
        else:
            raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone):
        """
        Пошук телефону в записі.

        Args:
            phone: Номер телефону для пошуку

        Returns:
            Phone: Об'єкт Phone якщо знайдено, None інакше
        """
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def __str__(self):
        """
        Повертає строкове представлення запису.

        Returns:
            str: Форматований рядок з ім'ям та телефонами
        """
        birthday_str = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}"

    def __repr__(self):
        """
        Повертає представлення об'єкта для розробників.

        Returns:
            str: Представлення об'єкта
        """
        return f"Record(name={self.name.value!r}, phones={[p.value for p in self.phones]})"
