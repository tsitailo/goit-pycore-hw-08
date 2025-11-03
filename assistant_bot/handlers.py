from functools import wraps

from address_book import Record
from address_book import Birthday


def input_error(func):
    """
    Декоратор для обробки помилок введення користувача.

    Обробляє винятки:
    - ValueError: Неправильні значення аргументів
    - KeyError: Контакт не знайдено
    - IndexError: Недостатньо аргументів
    """

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command"
        except Exception as e:
            return f"Error: {str(e)}"

    return inner


@input_error
def add_contact(args, book):
    """
    Додає новий контакт до книги контактів.

    Args:
        args (list): Список аргументів [ім'я, телефон]
        book (AddressBook): Об'єкт книги контактів

    Returns:
        str: Повідомлення про результат операції

    Raises:
        IndexError: Якщо недостатньо аргументів
        ValueError: Якщо контакт вже існує
    """
    name, phone, *_ = args  # Викине IndexError якщо недостатньо аргументів
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    if phone:
        record.add_phone(phone)

    return message


@input_error
def change_contact(args, book):
    """
    Змінює номер телефону для існуючого контакту.

    Args:
        args (list): Список аргументів [ім'я, новий_телефон]
        book (AddressBook): Об'єкт книги контактів

    Returns:
        str: Повідомлення про результат операції

    Raises:
        IndexError: Якщо недостатньо аргументів
        KeyError: Якщо контакт не знайдено
    """
    name, old_phone, new_phone, *_ = args  # Викине IndexError якщо недостатньо аргументів

    if not book.change(name, old_phone, new_phone):
        raise KeyError(name)  # Декоратор обробить

    return "Contact updated."


@input_error
def show_phone(args, book):
    """
    Show phone numbers for a contact.

    Args:
        args: List with contact name
        book: AddressBook instance

    Returns:
        String with phone numbers or error message
    """
    if len(args) < 1:
        return "Enter the argument for the command"

    name = args[0]
    record = book.find(name)

    if record is None:
        return "Contact not found."

    if not record.phones:
        return f"Contact {name} has no phone numbers."

    phones = "; ".join(phone.value for phone in record.phones)
    return f"{name}: {phones}"


def show_all(contact_book):
    """
    Повертає всі збережені контакти з номерами телефонів.

    Args:
        contact_book (AddressBook): Об'єкт книги контактів

    Returns:
        str: Відформатований список контактів
    """
    if not contact_book.data:
        return "No contacts saved."

    return str(contact_book)


@input_error
def show_birthday(args, book):
    """
    Показує дату народження для вказаного контакту.

    Args:
        args (list): Список аргументів [ім'я]
        book (AddressBook): Об'єкт книги контактів

    Returns:
        str: Дата народження або повідомлення про помилку

    Raises:
        IndexError: Якщо не вказано ім'я
        KeyError: Якщо контакт не знайдено
    """
    name = args[0]  # Викине IndexError якщо немає аргументів
    record = book.find(name)

    if record is None:
        raise KeyError(name)

    if record.birthday is None:
        return "Contact doesn't have birthday set."

    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
def add_birthday(args, book):
    """
    Додає дату народження для вказаного контакту.

    Args:
        args (list): Список аргументів [ім'я, дата_народження]
        book (AddressBook): Об'єкт книги контактів

    Returns:
        str: Повідомлення про результат операції

    Raises:
        IndexError: Якщо недостатньо аргументів
        KeyError: Якщо контакт не знайдено
        ValueError: Якщо неправильний формат дати
    """
    name, birth_date, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError(name)

    record.add_birthday(birth_date)
    return "Birthday added."


@input_error
def birthdays(args, book):
    """
    Показує дні народження, які відбудуться протягом наступного тижня.

    Args:
        args (list): Не використовуються
        book (AddressBook): Об'єкт книги контактів

    Returns:
        str: Список контактів з днями народження або повідомлення про відсутність
    """
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays next week."

    result = []
    for birthday in upcoming:
        result.append(f"{birthday['name']}: {birthday['congratulation_date']}")

    return "\n".join(result)
