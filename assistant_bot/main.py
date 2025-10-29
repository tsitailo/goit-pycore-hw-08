"""
Головний модуль програми з основним циклом обробки команд.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from address_book.address_book import AddressBook
from handlers import add_contact, change_contact, show_phone, show_all, add_birthday, show_birthday, \
    birthdays
from parser import parse_input



def main():
    """
    Головна функція, яка управляє циклом обробки команд.
    """
    with AddressBook("addressbook.pkl") as book:
        print("Welcome to the assistant bot!")

        while True:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "hello":
                print("How can I help you?")

            elif command == "add":
                print(add_contact(args, book))

            elif command == "change":
                print(change_contact(args, book))

            elif command == "phone":
                print(show_phone(args, book))

            elif command == "all":
                print(show_all(book))

            elif command == "add-birthday":
                print(add_birthday(args, book))

            elif command == "show-birthday":
                print(show_birthday(args, book))

            elif command == "birthdays":
                print(birthdays(args, book))

            else:
                print("Invalid command.")


if __name__ == "__main__":
    main()
