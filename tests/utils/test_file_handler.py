import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, "src")
from basiccli.utils.file_handler import FileError, FileHandler


class TestFileHandler:
    @pytest.fixture
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_json_read_write(self, temp_dir):
        filepath = Path(temp_dir) / "test.json"
        data = {"name": "Test", "value": 42, "items": [1, 2, 3]}

        FileHandler.write(filepath, data, format="json")
        assert filepath.exists()

        read_data = FileHandler.read(filepath, format="json")
        assert read_data["name"] == data["name"]
        assert read_data["value"] == data["value"]
        assert read_data["items"] == data["items"]

    def test_json_pretty_formatting(self, temp_dir):
        filepath = Path(temp_dir) / "pretty.json"
        data = {"test": "data"}

        FileHandler.write(filepath, data, format="json", pretty=True)
        content = filepath.read_text()

        assert "\n" in content
        assert "  " in content

    def test_json_compact_formatting(self, temp_dir):
        filepath = Path(temp_dir) / "compact.json"
        data = {"test": "data"}

        FileHandler.write(filepath, data, format="json", pretty=False)
        content = filepath.read_text()

        assert "\n" not in content.strip()

    def test_yaml_read_write(self, temp_dir):
        filepath = Path(temp_dir) / "test.yaml"
        data = {"config": {"host": "localhost", "port": 3000}}

        FileHandler.write(filepath, data, format="yaml")
        read_data = FileHandler.read(filepath, format="yaml")

        assert isinstance(read_data, dict)
        assert read_data["config"]["host"] == "localhost"
        assert read_data["config"]["port"] == 3000

    def test_csv_read_write(self, temp_dir):
        filepath = Path(temp_dir) / "test.csv"
        data = [
            {"name": "Alice", "age": 30, "city": "NYC"},
            {"name": "Bob", "age": 25, "city": "LA"},
        ]

        FileHandler.write(filepath, data, format="csv")
        read_data = FileHandler.read(filepath, format="csv")

        assert len(read_data) == 2
        assert read_data[0]["name"] == "Alice"
        assert read_data[0]["age"] == "30"  # CSV reads as strings
        assert read_data[1]["name"] == "Bob"

    def test_text_read_write(self, temp_dir):
        filepath = Path(temp_dir) / "test.txt"
        content = "Plain text content\nWith multiple lines"

        FileHandler.write(filepath, content)
        read_content = FileHandler.read(filepath)

        assert read_content == content

    def test_automatic_format_detection(self, temp_dir):
        # Test JSON detection
        json_file = Path(temp_dir) / "auto.json"
        FileHandler.write(json_file, {"test": True})
        result = FileHandler.read(json_file)
        assert isinstance(result, dict)
        assert result["test"] is True

        # Test YAML detection
        yaml_file = Path(temp_dir) / "auto.yaml"
        FileHandler.write(yaml_file, {"test": True})
        result = FileHandler.read(yaml_file)
        assert isinstance(result, dict)

        # Test CSV detection
        csv_file = Path(temp_dir) / "auto.csv"
        FileHandler.write(csv_file, [{"a": 1, "b": 2}])
        result = FileHandler.read(csv_file)
        assert isinstance(result, list)

    def test_copy_file(self, temp_dir):
        source = Path(temp_dir) / "source.txt"
        dest = Path(temp_dir) / "subdir" / "dest.txt"

        source.write_text("test content")

        FileHandler.copy(source, dest)

        assert dest.exists()
        assert dest.read_text() == "test content"
        assert source.exists()  # Original should still exist

    def test_copy_creates_directories(self, temp_dir):
        source = Path(temp_dir) / "source.txt"
        dest = Path(temp_dir) / "deep" / "nested" / "dest.txt"

        source.write_text("test content")

        FileHandler.copy(source, dest, create_dirs=True)
        assert dest.exists()

    def test_copy_nonexistent_source_raises_error(self, temp_dir):
        dest = Path(temp_dir) / "dest.txt"

        with pytest.raises(FileError, match="Source file not found"):
            FileHandler.copy("/nonexistent/file.txt", dest)

    def test_move_file(self, temp_dir):
        source = Path(temp_dir) / "source.txt"
        dest = Path(temp_dir) / "moved.txt"

        source.write_text("move me")

        FileHandler.move(source, dest)

        assert not source.exists()
        assert dest.exists()
        assert dest.read_text() == "move me"

    def test_move_creates_directories(self, temp_dir):
        source = Path(temp_dir) / "source.txt"
        nested_dest = Path(temp_dir) / "nested" / "dir" / "file.txt"

        source.write_text("content")

        FileHandler.move(source, nested_dest, create_dirs=True)
        assert nested_dest.exists()

    def test_delete_existing_file(self, temp_dir):
        filepath = Path(temp_dir) / "delete_me.txt"
        filepath.write_text("temporary")

        result = FileHandler.delete(filepath)
        assert result is True
        assert not filepath.exists()

    def test_delete_nonexistent_file(self):
        result = FileHandler.delete("/nonexistent/file.txt")
        assert result is False

    def test_exists_method(self, temp_dir):
        filepath = Path(temp_dir) / "exists.txt"
        filepath.write_text("content")

        assert FileHandler.exists(filepath) is True
        assert FileHandler.exists("/nonexistent/file.txt") is False

    def test_size_method(self, temp_dir):
        filepath = Path(temp_dir) / "sized.txt"
        content = "Hello World"
        filepath.write_text(content)

        assert FileHandler.size(filepath) == len(content.encode())

    def test_size_nonexistent_raises_error(self):
        with pytest.raises(FileError):
            FileHandler.size("/nonexistent/file.txt")

    def test_checksum_default_sha256(self, temp_dir):
        filepath = Path(temp_dir) / "checksum.txt"
        filepath.write_text("Hello World")

        checksum = FileHandler.checksum(filepath)
        assert isinstance(checksum, str)
        assert len(checksum) == 64  # SHA256 is 64 hex chars

    def test_checksum_algorithms(self, temp_dir):
        filepath = Path(temp_dir) / "checksum.txt"
        filepath.write_text("Hello World")

        md5_checksum = FileHandler.checksum(filepath, algorithm="md5")
        assert len(md5_checksum) == 32  # MD5 is 32 hex chars

        sha1_checksum = FileHandler.checksum(filepath, algorithm="sha1")
        assert len(sha1_checksum) == 40  # SHA1 is 40 hex chars

        sha512_checksum = FileHandler.checksum(filepath, algorithm="sha512")
        assert len(sha512_checksum) == 128  # SHA512 is 128 hex chars

    def test_checksum_unsupported_algorithm(self, temp_dir):
        filepath = Path(temp_dir) / "checksum.txt"
        filepath.write_text("Hello World")

        with pytest.raises(ValueError, match="Unsupported algorithm"):
            FileHandler.checksum(filepath, algorithm="invalid")

    def test_stats_method(self, temp_dir):
        filepath = Path(temp_dir) / "stats.txt"
        filepath.write_text("test content")

        stats = FileHandler.stats(filepath)

        assert stats["size"] == 12
        assert stats["file"] is True
        assert stats["directory"] is False
        assert stats["readable"] is True
        assert stats["writable"] is True
        assert isinstance(stats["modified_at"], float)
        assert isinstance(stats["created_at"], float)
        assert isinstance(stats["accessed_at"], float)
        assert len(stats["permissions"]) == 3

    def test_atomic_write(self, temp_dir):
        filepath = Path(temp_dir) / "atomic.json"
        data = {"atomic": True, "value": 42}

        FileHandler.atomic_write(filepath, data, format="json")

        assert filepath.exists()
        read_data = FileHandler.read(filepath, format="json")
        assert read_data["atomic"] is True

    def test_read_nonexistent_file_raises_error(self):
        with pytest.raises(FileError, match="File not found"):
            FileHandler.read("/nonexistent/file.txt")

    def test_invalid_json_raises_error(self, temp_dir):
        filepath = Path(temp_dir) / "invalid.json"
        filepath.write_text("{invalid json}")

        with pytest.raises(FileError, match="Invalid JSON"):
            FileHandler.read(filepath, format="json")

    def test_invalid_yaml_raises_error(self, temp_dir):
        filepath = Path(temp_dir) / "invalid.yaml"
        filepath.write_text(":\n  invalid: yaml: structure:")

        with pytest.raises(FileError, match="Invalid YAML"):
            FileHandler.read(filepath, format="yaml")

    def test_invalid_csv_raises_error(self, temp_dir):
        filepath = Path(temp_dir) / "invalid.csv"
        filepath.write_text('"unclosed quote,data')

        with pytest.raises(FileError, match="Invalid CSV"):
            FileHandler.read(filepath, format="csv")
