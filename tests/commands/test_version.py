import json
import sys

sys.path.insert(0, "src")

from basiccli.commands.version import VersionCommand  # noqa: E402


class TestVersionCommand:
    def test_displays_formatted_version_information(self, capsys):
        command = VersionCommand()
        result = command.execute()

        captured = capsys.readouterr()
        assert "BasicCli" in captured.out
        assert "1.0.0" in captured.out
        assert "2025-01-15" in captured.out
        assert "Python Version:" in captured.out
        assert result.success is True

    def test_displays_formatted_box(self, capsys):
        command = VersionCommand()
        command.execute()

        captured = capsys.readouterr()
        assert "╔" in captured.out
        assert "╚" in captured.out
        assert "║" in captured.out

    def test_json_output_valid_format(self, capsys):
        command = VersionCommand(output_json=True)
        command.execute()

        captured = capsys.readouterr()
        json_data = json.loads(captured.out)

        assert json_data["name"] == "BasicCli"
        assert json_data["version"] == "1.0.0"
        assert json_data["build_date"] == "2025-01-15"
        assert "github.com" in json_data["repository"]

    def test_json_includes_all_required_fields(self, capsys):
        command = VersionCommand(output_json=True)
        command.execute()

        captured = capsys.readouterr()
        json_data = json.loads(captured.out)

        required_fields = [
            "name",
            "version",
            "build_date",
            "python_version",
            "platform",
            "description",
            "repository",
        ]

        for field in required_fields:
            assert field in json_data

    def test_constants(self):
        assert VersionCommand.VERSION == "1.0.0"
        assert VersionCommand.BUILD_DATE == "2025-01-15"

    def test_returns_successful_result(self):
        command = VersionCommand()
        result = command.execute()

        assert result.success is True
        assert result.is_success() is True
        assert "Version displayed successfully" in result.message
