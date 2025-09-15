import sys

sys.path.insert(0, "src")

from unittest.mock import patch  # noqa: E402

from basiccli.commands.hello import HelloCommand  # noqa: E402


class TestHelloCommand:
    def test_greets_user_with_name(self, capsys):
        command = HelloCommand("Alice")
        result = command.execute()

        captured = capsys.readouterr()
        assert "Alice" in captured.out
        assert "Welcome to BasicCli" in captured.out
        assert result.success is True

    def test_includes_time_based_greeting(self, capsys):
        command = HelloCommand("Bob")
        command.execute()

        captured = capsys.readouterr()
        assert any(
            greeting in captured.out
            for greeting in ["Good morning", "Good afternoon", "Good evening"]
        )

    def test_uppercase_option(self, capsys):
        command = HelloCommand("Charlie", uppercase=True)
        command.execute()

        captured = capsys.readouterr()
        assert captured.out.isupper()
        assert "CHARLIE" in captured.out

    def test_repeat_option(self, capsys):
        command = HelloCommand("David", repeat=3)
        command.execute()

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 3
        assert all("David" in line for line in lines)

    def test_returns_successful_result(self):
        command = HelloCommand("Eve")
        result = command.execute()

        assert result.success is True
        assert result.is_success() is True
        assert "Eve" in result.message

    @patch("basiccli.commands.hello.datetime")
    def test_time_of_day_detection(self, mock_datetime, capsys):
        # Test morning
        mock_datetime.now.return_value.hour = 9
        command = HelloCommand("Test")
        command.execute()
        captured = capsys.readouterr()
        assert "Good morning" in captured.out

        # Test afternoon
        mock_datetime.now.return_value.hour = 14
        command = HelloCommand("Test")
        command.execute()
        captured = capsys.readouterr()
        assert "Good afternoon" in captured.out

        # Test evening
        mock_datetime.now.return_value.hour = 20
        command = HelloCommand("Test")
        command.execute()
        captured = capsys.readouterr()
        assert "Good evening" in captured.out

    def test_error_handling(self):
        # Test with invalid parameters that might cause errors
        command = HelloCommand("Test", repeat=0)
        result = command.execute()

        # Should handle gracefully and not repeat
        assert result.success is True
