"""
Тести для модуля parser.py
"""

import pytest

from assistant_bot.parser import parse_input


class TestParseInput:
    """Тести для функції parse_input."""

    # Тести базової функціональності
    def test_parse_simple_command(self):
        """Тест парсингу простої команди без аргументів."""
        cmd, args = parse_input("hello")
        assert cmd == "hello"
        assert args == []

    def test_parse_command_with_one_argument(self):
        """Тест парсингу команди з одним аргументом."""
        cmd, args = parse_input("phone John")
        assert cmd == "phone"
        assert args == ["John"]

    def test_parse_command_with_two_arguments(self):
        """Тест парсингу команди з двома аргументами."""
        cmd, args = parse_input("add John 1234567890")
        assert cmd == "add"
        assert args == ["John", "1234567890"]

    def test_parse_command_with_multiple_arguments(self):
        """Тест парсингу команди з багатьма аргументами."""
        cmd, args = parse_input("add John Doe 1234567890")
        assert cmd == "add"
        assert args == ["John", "Doe", "1234567890"]

    # Тести з регістром
    def test_parse_uppercase_command(self):
        """Тест парсингу команди у верхньому регістрі."""
        cmd, args = parse_input("HELLO")
        assert cmd == "hello"
        assert args == []

    def test_parse_mixed_case_command(self):
        """Тест парсингу команди у змішаному регістрі."""
        cmd, args = parse_input("HeLLo")
        assert cmd == "hello"
        assert args == []

    def test_parse_command_arguments_preserve_case(self):
        """Тест що аргументи зберігають регістр."""
        cmd, args = parse_input("add JOHN 1234567890")
        assert cmd == "add"
        assert args == ["JOHN", "1234567890"]

    # Тести з пробілами
    def test_parse_command_with_extra_spaces(self):
        """Тест парсингу команди з зайвими пробілами."""
        cmd, args = parse_input("  add   John   1234567890  ")
        assert cmd == "add"
        assert args == ["John", "1234567890"]

    def test_parse_command_with_leading_spaces(self):
        """Тест парсингу команди з пробілами на початку."""
        cmd, args = parse_input("   hello")
        assert cmd == "hello"
        assert args == []

    def test_parse_command_with_trailing_spaces(self):
        """Тест парсингу команди з пробілами в кінці."""
        cmd, args = parse_input("hello   ")
        assert cmd == "hello"
        assert args == []

    def test_parse_command_with_multiple_spaces_between_args(self):
        """Тест парсингу команди з множинними пробілами між аргументами."""
        cmd, args = parse_input("add    John    1234567890")
        assert cmd == "add"
        assert args == ["John", "1234567890"]

    # Тести команд виходу
    def test_parse_exit_command(self):
        """Тест парсингу команди exit."""
        cmd, args = parse_input("exit")
        assert cmd == "exit"
        assert args == []

    def test_parse_close_command(self):
        """Тест парсингу команди close."""
        cmd, args = parse_input("close")
        assert cmd == "close"
        assert args == []

    # Тести крайніх випадків
    def test_parse_empty_string(self):
        """Тест парсингу порожнього рядка."""
        cmd, args = parse_input("")
        assert cmd == ""
        assert args == []

    def test_parse_only_spaces(self):
        """Тест парсингу рядка тільки з пробілів."""
        cmd, args = parse_input("     ")
        assert cmd == ""
        assert args == []

    def test_parse_single_character_command(self):
        """Тест парсингу команди з одного символу."""
        cmd, args = parse_input("a")
        assert cmd == "a"
        assert args == []

    # Тести з табуляцією та спеціальними символами
    def test_parse_command_with_tabs(self):
        """Тест парсингу команди з табуляцією."""
        cmd, args = parse_input("add\tJohn\t1234567890")
        assert cmd == "add"
        assert args == ["John", "1234567890"]

    def test_parse_command_with_mixed_whitespace(self):
        """Тест парсингу команди зі змішаними пробілами та табуляцією."""
        cmd, args = parse_input("  add \t John  \t 1234567890  ")
        assert cmd == "add"
        assert args == ["John", "1234567890"]

    def test_parse_arguments_with_special_characters(self):
        """Тест парсингу аргументів зі спеціальними символами."""
        cmd, args = parse_input("add John-Doe +380-50-123-45-67")
        assert cmd == "add"
        assert args == ["John-Doe", "+380-50-123-45-67"]

    def test_parse_arguments_with_underscores(self):
        """Тест парсингу аргументів з підкресленнями."""
        cmd, args = parse_input("add John_Doe 123_456")
        assert cmd == "add"
        assert args == ["John_Doe", "123_456"]

    def test_parse_arguments_with_dots(self):
        """Тест парсингу аргументів з крапками."""
        cmd, args = parse_input("add John.Doe 123.456")
        assert cmd == "add"
        assert args == ["John.Doe", "123.456"]

    # Тести реальних команд
    def test_parse_add_command(self):
        """Тест парсингу команди add."""
        cmd, args = parse_input("add Jime 0501234356")
        assert cmd == "add"
        assert args == ["Jime", "0501234356"]

    def test_parse_change_command(self):
        """Тест парсингу команди change."""
        cmd, args = parse_input("change Jime 0509999999")
        assert cmd == "change"
        assert args == ["Jime", "0509999999"]

    def test_parse_phone_command(self):
        """Тест парсингу команди phone."""
        cmd, args = parse_input("phone Jime")
        assert cmd == "phone"
        assert args == ["Jime"]

    def test_parse_all_command(self):
        """Тест парсингу команди all."""
        cmd, args = parse_input("all")
        assert cmd == "all"
        assert args == []

    def test_parse_hello_command(self):
        """Тест парсингу команди hello."""
        cmd, args = parse_input("hello")
        assert cmd == "hello"
        assert args == []

    # Тести типів даних
    def test_parse_returns_tuple(self):
        """Тест що функція повертає кортеж."""
        result = parse_input("hello")
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_parse_command_is_string(self):
        """Тест що команда є рядком."""
        cmd, args = parse_input("hello")
        assert isinstance(cmd, str)

    def test_parse_args_is_list(self):
        """Тест що аргументи є списком."""
        cmd, args = parse_input("add John 123")
        assert isinstance(args, list)
        assert all(isinstance(arg, str) for arg in args)

    def test_parse_empty_args_is_empty_list(self):
        """Тест що без аргументів повертається порожній список."""
        cmd, args = parse_input("hello")
        assert isinstance(args, list)
        assert len(args) == 0

    # Тести з unicode
    def test_parse_command_with_unicode(self):
        """Тест парсингу команди з Unicode символами."""
        cmd, args = parse_input("add Іван +380501234567")
        assert cmd == "add"
        assert args == ["Іван", "+380501234567"]

    def test_parse_command_with_cyrillic(self):
        """Тест парсингу команди з кирилицею."""
        cmd, args = parse_input("add Марія 0987654321")
        assert cmd == "add"
        assert args == ["Марія", "0987654321"]

    # Параметризовані тести
    @pytest.mark.parametrize("input_str,expected_cmd,expected_args", [
        ("hello", "hello", []),
        ("add John 123", "add", ["John", "123"]),
        ("CHANGE Alice 456", "change", ["Alice", "456"]),
        ("phone Bob", "phone", ["Bob"]),
        ("all", "all", []),
        ("  exit  ", "exit", []),
        ("", "", []),
        ("   ", "", []),
        ("ADD John 123", "add", ["John", "123"]),
        ("Phone ALICE", "phone", ["ALICE"]),
    ])
    def test_parse_various_inputs(self, input_str, expected_cmd, expected_args):
        """Параметризований тест різних вхідних даних."""
        cmd, args = parse_input(input_str)
        assert cmd == expected_cmd
        assert args == expected_args

    # Стрес-тести
    def test_parse_very_long_command(self):
        """Тест парсингу дуже довгої команди."""
        long_name = "A" * 1000
        cmd, args = parse_input(f"add {long_name} 123")
        assert cmd == "add"
        assert args == [long_name, "123"]

    def test_parse_many_arguments(self):
        """Тест парсингу команди з багатьма аргументами."""
        input_str = "command " + " ".join([f"arg{i}" for i in range(100)])
        cmd, args = parse_input(input_str)
        assert cmd == "command"
        assert len(args) == 100
        assert args[0] == "arg0"
        assert args[99] == "arg99"

    # Тести граничних випадків
    def test_parse_command_with_numbers(self):
        """Тест парсингу команди з цифрами."""
        cmd, args = parse_input("command123 arg456")
        assert cmd == "command123"
        assert args == ["arg456"]

    def test_parse_only_command_lowercase(self):
        """Тест що команда завжди в нижньому регістрі."""
        test_cases = [
            "HELLO",
            "Hello",
            "HeLLo",
            "hello"
        ]
        for test_input in test_cases:
            cmd, args = parse_input(test_input)
            assert cmd == "hello"

    def test_parse_preserves_argument_case(self):
        """Тест що регістр аргументів зберігається."""
        cmd, args = parse_input("add JOHN john JoHn")
        assert cmd == "add"
        assert args == ["JOHN", "john", "JoHn"]
        assert args[0] != args[1]
        assert args[1] != args[2]

    # Тести помилкових сценаріїв
    def test_parse_newline_in_input(self):
        """Тест парсингу вводу з переносом рядка."""
        cmd, args = parse_input("add John\n1234567890")
        # \n розглядається як частина аргументу або видаляється strip()
        assert cmd == "add"
        # Результат залежить від реалізації

    def test_parse_multiple_newlines(self):
        """Тест парсингу вводу з кількома переносами рядків."""
        cmd, args = parse_input("hello\n\n")
        assert cmd == "hello"

    # Додаткові тести для покриття
    def test_parse_returns_correct_structure(self):
        """Тест що функція завжди повертає (str, list)."""
        test_inputs = [
            "",
            "hello",
            "add John 123",
            "  spaces  everywhere  ",
            "UPPER",
        ]
        for test_input in test_inputs:
            cmd, args = parse_input(test_input)
            assert isinstance(cmd, str), f"Command should be str for input: {test_input}"
            assert isinstance(args, list), f"Args should be list for input: {test_input}"
