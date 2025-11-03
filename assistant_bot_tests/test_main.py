"""
Тести для модуля main.
"""

from unittest.mock import patch

from assistant_bot.main import main


class TestMain:
    """Тести для функції main."""

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_hello_command(self, mock_print, mock_input):
        """Тест команди hello."""
        mock_input.side_effect = ["hello", "exit"]
        main()

        # Перевіряємо що було викликано print з правильними повідомленнями
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Welcome to the assistant bot!" in str(call) for call in print_calls)
        assert any("How can I help you?" in str(call) for call in print_calls)
        assert any("Good bye!" in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_exit_command(self, mock_print, mock_input):
        """Тест команди exit."""
        mock_input.side_effect = ["exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Good bye!" in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_close_command(self, mock_print, mock_input):
        """Тест команди close."""
        mock_input.side_effect = ["close"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Good bye!" in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_add_command(self, mock_print, mock_input):
        """Тест команди add."""
        mock_input.side_effect = ["add John 1234567890", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Contact added." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_add_command_no_args(self, mock_print, mock_input):
        """Тест команди add без аргументів."""
        mock_input.side_effect = ["add", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Give me name and phone please." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_add_command_one_arg(self, mock_print, mock_input):
        """Тест команди add з одним аргументом."""
        mock_input.side_effect = ["add John", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Give me name and phone please." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_change_command(self, mock_print, mock_input):
        """Тест команди change."""
        mock_input.side_effect = [
            "add John 1234567890",
            "change John 1234567890 9999999999",
            "exit"
        ]
        main()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_phone_command(self, mock_print, mock_input):
        """Тест команди phone."""
        mock_input.side_effect = [
            "add John 1234567890",
            "phone John",
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("1234567890" in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_all_command(self, mock_print, mock_input):
        """Тест команди all."""
        mock_input.side_effect = [
            "add John 1234567890",
            "add Alice 0987654321",
            "all",
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        # Перевіряємо що виведено обидва контакти
        output = " ".join([str(call) for call in print_calls])
        # Перевіряємо наявність імен та телефонів (гнучкіший формат)
        assert "John" in output and "1234567890" in output, f"John's contact not found in: {output}"
        assert "Alice" in output and "0987654321" in output, f"Alice's contact not found in: {output}"

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_invalid_command(self, mock_print, mock_input):
        """Тест невалідної команди."""
        mock_input.side_effect = ["invalid", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Invalid command." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_multiple_commands(self, mock_print, mock_input):
        """Тест виконання кількох команд підряд."""

        mock_input.side_effect = [
            "hello",
            "add John 1234567890",
            "add Alice 0987654321",
            "phone John",
            "change John 1234567890 9999999999",
            "phone John",
            "all",
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join([str(call) for call in print_calls])

        assert "How can I help you?" in output
        assert "Contact added." in output
        assert "1234567890" in output
        assert "Contact updated." in output

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_case_insensitive_commands(self, mock_print, mock_input):
        """Тест що команди не чутливі до регістру."""
        mock_input.side_effect = [
            "HELLO",
            "ADD John 1234567890",
            "PHONE John",
            "EXIT"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join([str(call) for call in print_calls])

        assert "How can I help you?" in output
        assert "Contact added." in output
        assert "1234567890" in output

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_empty_contact_book_all(self, mock_print, mock_input):
        """Тест команди all на порожній книзі контактів."""
        mock_input.side_effect = ["all", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("No contacts saved." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_phone_non_existing_contact(self, mock_print, mock_input):
        """Тест команди phone для неіснуючого контакту."""
        mock_input.side_effect = ["phone John", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        # Декоратор input_error повертає "Contact not found."
        assert any("Contact not found." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_change_non_existing_contact(self, mock_print, mock_input):
        """Тест команди change для неіснуючого контакту."""
        mock_input.side_effect = ["change John 1234567890 9999999999", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        # Декоратор input_error повертає "Contact not found."
        assert any("Contact not found." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_phone_no_args(self, mock_print, mock_input):
        """Тест команди phone без аргументів."""
        mock_input.side_effect = ["phone", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Enter the argument for the command" in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_change_no_args(self, mock_print, mock_input):
        """Тест команди change без аргументів."""
        mock_input.side_effect = ["change", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Give me name and phone please." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_add_existing_contact(self, mock_print, mock_input):
        """Тест додавання існуючого контакту."""
        mock_input.side_effect = [
            "add John 1234567890",
            "add John 9999999999",
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join([str(call) for call in print_calls])

        # Перевіряємо що спочатку контакт додано, потім оновлено
        assert "Contact added." in output, f"Expected 'Contact added.' message, got: {print_calls}"
        assert "Contact updated." in output, f"Expected 'Contact updated.' message, got: {print_calls}"

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_workflow_from_task_example(self, mock_print, mock_input):
        """Тест згідно з прикладом з завдання."""
        mock_input.side_effect = [
            "add",  # Enter the argument for the command (ValueError)
            "add Bob",  # Enter the argument for the command (ValueError)
            "add Jime 0501234356",  # Contact added.
            "phone",  # Enter the argument for the command (IndexError)
            "all",  # Jime: 0501234356
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join([str(call) for call in print_calls])

        # Перевіряємо повідомлення про помилки
        assert "Give me name and phone please." in output  # для "add" та "add Bob"
        # Перевіряємо успішне додавання
        assert "Contact added." in output
        # Перевіряємо помилку для phone без аргументів
        assert "Enter the argument for the command" in output
        # Перевіряємо що контакт виведено (гнучка перевірка формату)
        assert "Jime" in output and "0501234356" in output, f"Expected Jime with phone 0501234356, got: {output}"

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_whitespace_handling(self, mock_print, mock_input):
        """Тест обробки пробілів у командах."""
        mock_input.side_effect = [
            "  add  John  1234567890  ",
            "  phone  John  ",
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join([str(call) for call in print_calls])

        assert "Contact added." in output
        assert "1234567890" in output

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_sequential_operations(self, mock_print, mock_input):
        """Тест послідовних операцій з одним контактом."""
        mock_input.side_effect = [
            "add John 1111111111",
            "phone John",  # 1111111111
            "change John 1111111111 2222222222",
            "phone John",  # 2222222222
            "all",  # John: 2222222222
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join([str(call) for call in print_calls])

        assert "Contact added." in output
        assert "1111111111" in output
        assert "Contact updated." in output

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_special_characters_in_names(self, mock_print, mock_input):
        """Тест спеціальних символів в іменах."""
        mock_input.side_effect = [
            "add John-Doe 1234567890",  # Використовуємо правильний формат телефону
            "phone John-Doe",
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join([str(call) for call in print_calls])

        # Перевіряємо що контакт додано
        assert "Contact added." in output or "added" in output.lower(), f"Expected contact to be added, got: {output}"
        # Перевіряємо що ім'я з дефісом працює
        assert "John-Doe" in output, f"Expected John-Doe in output, got: {output}"
        # Перевіряємо що телефон виведено
        assert "1234567890" in output, f"Expected phone number in output, got: {output}"

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_unicode_names(self, mock_print, mock_input):
        """Тест українських імен."""
        mock_input.side_effect = [
            "add Іван 0501234567",  # 10 цифр без спецсимволів
            "phone Іван",
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join([str(call) for call in print_calls])

        # Перевіряємо що контакт додано
        assert "Contact added." in output or "added" in output.lower(), f"Expected contact to be added, got: {output}"
        # Перевіряємо що українське ім'я працює
        assert "Іван" in output, f"Expected 'Іван' in output, got: {output}"
        # Перевіряємо що телефон виведено
        assert "0501234567" in output, f"Expected phone number in output, got: {output}"

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_empty_input(self, mock_print, mock_input):
        """Тест порожнього вводу."""
        mock_input.side_effect = ["", "   ", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        # Порожній ввід обробляється як невалідна команда
        assert any("Invalid command." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_all_error_messages(self, mock_print, mock_input):
        """Тест всіх типів повідомлень про помилки."""
        mock_input.side_effect = [
            "add",  # ValueError -> "Give me name and phone please."
            "change",  # ValueError -> "Give me name and phone please."
            "phone",  # IndexError -> "Enter the argument for the command"
            "phone NonExistent",  # KeyError -> "Contact not found."
            "invalid_command",  # Invalid command
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join([str(call) for call in print_calls])

        assert "Give me name and phone please." in output
        assert "Enter the argument for the command" in output
        assert "Contact not found." in output
        assert "Invalid command." in output
