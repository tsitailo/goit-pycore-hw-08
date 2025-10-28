import pytest
import pickle
from pathlib import Path
from address_book.address_book import AddressBook, Record


class TestAddressBookSerialization:
    """Тести для серіалізації та десеріалізації адресної книги"""

    @pytest.fixture
    def address_book(self):
        """Створює адресну книгу з тестовими даними"""
        book = AddressBook()

        # Додаємо кілька записів
        record1 = Record("John")
        record1.add_phone("1234567890")
        record1.add_phone("0987654321")
        record1.add_birthday("15.03.1990")
        book.add_record(record1)

        record2 = Record("Jane")
        record2.add_phone("5555555555")
        record2.add_birthday("20.05.1985")
        book.add_record(record2)

        record3 = Record("Bob")
        record3.add_phone("1111111111")
        book.add_record(record3)

        return book

    @pytest.fixture
    def temp_filename(self, tmp_path):
        """Створює тимчасовий файл для тестів"""
        return tmp_path / "test_addressbook.pkl"

    def test_save_to_file_creates_file(self, address_book, temp_filename):
        """Тест: файл створюється після збереження"""
        address_book.save_to_file(str(temp_filename))
        assert temp_filename.exists()

    def test_save_to_file_contains_pickle_data(self, address_book, temp_filename):
        """Тест: файл містить валідні pickle дані"""
        address_book.save_to_file(str(temp_filename))

        with open(temp_filename, "rb") as f:
            data = pickle.load(f)

        assert isinstance(data, dict)
        assert len(data) == 3
        assert "John" in data
        assert "Jane" in data
        assert "Bob" in data

    def test_load_from_file_restores_data(self, address_book, temp_filename):
        """Тест: дані коректно відновлюються з файлу"""
        # Зберігаємо дані
        address_book.save_to_file(str(temp_filename))

        # Створюємо нову книгу і завантажуємо дані
        new_book = AddressBook()
        result = new_book.load_from_file(str(temp_filename))

        assert result is True
        assert len(new_book.data) == 3
        assert "John" in new_book.data
        assert "Jane" in new_book.data
        assert "Bob" in new_book.data

    def test_load_from_file_restores_phones(self, address_book, temp_filename):
        """Тест: телефони коректно відновлюються"""
        address_book.save_to_file(str(temp_filename))

        new_book = AddressBook()
        new_book.load_from_file(str(temp_filename))

        john = new_book.find("John")
        assert len(john.phones) == 2
        assert john.phones[0].value == "1234567890"
        assert john.phones[1].value == "0987654321"

        jane = new_book.find("Jane")
        assert len(jane.phones) == 1
        assert jane.phones[0].value == "5555555555"

    def test_load_from_file_restores_birthdays(self, address_book, temp_filename):
        """Тест: дні народження коректно відновлюються"""
        address_book.save_to_file(str(temp_filename))

        new_book = AddressBook()
        new_book.load_from_file(str(temp_filename))

        john = new_book.find("John")
        assert john.birthday is not None
        assert john.birthday.value.strftime("%d.%m.%Y") == "15.03.1990"

        jane = new_book.find("Jane")
        assert jane.birthday is not None
        assert jane.birthday.value.strftime("%d.%m.%Y") == "20.05.1985"

        bob = new_book.find("Bob")
        assert bob.birthday is None

    def test_load_from_nonexistent_file(self, temp_filename):
        """Тест: завантаження з неіснуючого файлу"""
        book = AddressBook()
        result = book.load_from_file(str(temp_filename))

        assert result is False
        assert len(book.data) == 0

    def test_save_empty_address_book(self, temp_filename):
        """Тест: збереження порожньої адресної книги"""
        book = AddressBook()
        book.save_to_file(str(temp_filename))

        assert temp_filename.exists()

        new_book = AddressBook()
        new_book.load_from_file(str(temp_filename))
        assert len(new_book.data) == 0

    def test_overwrite_existing_file(self, address_book, temp_filename):
        """Тест: перезапис існуючого файлу"""
        # Перше збереження
        address_book.save_to_file(str(temp_filename))

        # Змінюємо дані
        address_book.delete("Bob")
        record = Record("Alice")
        record.add_phone("9999999999")
        address_book.add_record(record)

        # Друге збереження (перезапис)
        address_book.save_to_file(str(temp_filename))

        # Завантажуємо і перевіряємо
        new_book = AddressBook()
        new_book.load_from_file(str(temp_filename))

        assert len(new_book.data) == 3
        assert "Bob" not in new_book.data
        assert "Alice" in new_book.data

    def test_load_preserves_record_functionality(self, address_book, temp_filename):
        """Тест: завантажені записи зберігають функціональність"""
        address_book.save_to_file(str(temp_filename))

        new_book = AddressBook()
        new_book.load_from_file(str(temp_filename))

        # Перевіряємо, що можемо працювати з завантаженими записами
        john = new_book.find("John")
        john.add_phone("3333333333")
        assert len(john.phones) == 3

        john.remove_phone("1234567890")
        assert len(john.phones) == 2

    def test_multiple_save_load_cycles(self, temp_filename):
        """Тест: багаторазове збереження та завантаження"""
        # Цикл 1
        book1 = AddressBook()
        record1 = Record("User1")
        record1.add_phone("1111111111")
        book1.add_record(record1)
        book1.save_to_file(str(temp_filename))

        # Цикл 2
        book2 = AddressBook()
        book2.load_from_file(str(temp_filename))
        record2 = Record("User2")
        record2.add_phone("2222222222")
        book2.add_record(record2)
        book2.save_to_file(str(temp_filename))

        # Цикл 3
        book3 = AddressBook()
        book3.load_from_file(str(temp_filename))

        assert len(book3.data) == 2
        assert "User1" in book3.data
        assert "User2" in book3.data

    def test_save_with_default_filename(self, address_book, tmp_path, monkeypatch):
        """Тест: збереження з дефолтним іменем файлу"""
        # Змінюємо робочу директорію на тимчасову
        monkeypatch.chdir(tmp_path)

        address_book.save_to_file()

        default_file = Path("addressbook.pkl")
        assert default_file.exists()

    def test_load_with_default_filename(self, address_book, tmp_path, monkeypatch):
        """Тест: завантаження з дефолтним іменем файлу"""
        # Змінюємо робочу директорію на тимчасову
        monkeypatch.chdir(tmp_path)

        address_book.save_to_file()

        new_book = AddressBook()
        result = new_book.load_from_file()

        assert result is True
        assert len(new_book.data) == 3

    def test_load_corrupted_file(self, temp_filename):
        """Тест: обробка пошкодженого файлу"""
        # Створюємо пошкоджений файл
        with open(temp_filename, "w") as f:
            f.write("This is not a pickle file")

        book = AddressBook()
        result = book.load_from_file(str(temp_filename))

        assert result is False
        assert len(book.data) == 0