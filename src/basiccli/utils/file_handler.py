import csv
import hashlib
import json
import os
import shutil
import time
from io import StringIO
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Union

import yaml


class FileError(Exception):
    pass


class UnsupportedFormatError(FileError):
    pass


class FileHandler:
    SUPPORTED_FORMATS = [".json", ".yaml", ".yml", ".csv", ".txt", ".log"]

    @classmethod
    def read(cls, filepath: Union[str, Path], format: Optional[str] = None) -> Any:
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileError(f"File not found: {filepath}")

        format = format or cls._detect_format(filepath)
        content = filepath.read_text()

        try:
            if format == "json":
                return cls._parse_json(content)
            elif format == "yaml":
                return cls._parse_yaml(content)
            elif format == "csv":
                return cls._parse_csv(content)
            else:
                return content
        except Exception as e:
            raise FileError(f"Failed to read {filepath}: {e}")

    @classmethod
    def write(
        cls,
        filepath: Union[str, Path],
        data: Any,
        format: Optional[str] = None,
        pretty: bool = True,
    ) -> bool:
        filepath = Path(filepath)
        format = format or cls._detect_format(filepath)

        # Create directories if needed
        filepath.parent.mkdir(parents=True, exist_ok=True)

        try:
            if format == "json":
                content = json.dumps(data, indent=2 if pretty else None)
            elif format == "yaml":
                content = yaml.dump(data, default_flow_style=False)
            elif format == "csv":
                content = cls._generate_csv(data)
            else:
                content = str(data)

            filepath.write_text(content)
            return True
        except Exception as e:
            raise FileError(f"Failed to write {filepath}: {e}")

    @classmethod
    def copy(
        cls,
        source: Union[str, Path],
        destination: Union[str, Path],
        create_dirs: bool = True,
    ) -> bool:
        source = Path(source)
        destination = Path(destination)

        if not source.exists():
            raise FileError(f"Source file not found: {source}")

        try:
            if create_dirs:
                destination.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(source, destination)
            return True
        except Exception as e:
            raise FileError(f"Failed to copy file: {e}")

    @classmethod
    def move(
        cls,
        source: Union[str, Path],
        destination: Union[str, Path],
        create_dirs: bool = True,
    ) -> bool:
        source = Path(source)
        destination = Path(destination)

        if not source.exists():
            raise FileError(f"Source file not found: {source}")

        try:
            if create_dirs:
                destination.parent.mkdir(parents=True, exist_ok=True)

            shutil.move(str(source), str(destination))
            return True
        except Exception as e:
            raise FileError(f"Failed to move file: {e}")

    @classmethod
    def delete(cls, filepath: Union[str, Path]) -> bool:
        filepath = Path(filepath)

        if not filepath.exists():
            return False

        try:
            filepath.unlink()
            return True
        except Exception as e:
            raise FileError(f"Failed to delete {filepath}: {e}")

    @classmethod
    def exists(cls, filepath: Union[str, Path]) -> bool:
        return Path(filepath).exists()

    @classmethod
    def size(cls, filepath: Union[str, Path]) -> int:
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileError(f"File not found: {filepath}")

        return filepath.stat().st_size

    @classmethod
    def checksum(cls, filepath: Union[str, Path], algorithm: str = "sha256") -> str:
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileError(f"File not found: {filepath}")

        hash_algorithms = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512,
        }

        if algorithm not in hash_algorithms:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        hasher = hash_algorithms[algorithm]()

        with filepath.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)

        return hasher.hexdigest()

    @classmethod
    def stats(cls, filepath: Union[str, Path]) -> Dict[str, Any]:
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileError(f"File not found: {filepath}")

        stat = filepath.stat()

        return {
            "size": stat.st_size,
            "modified_at": stat.st_mtime,
            "created_at": stat.st_ctime,
            "accessed_at": stat.st_atime,
            "permissions": oct(stat.st_mode)[-3:],
            "directory": filepath.is_dir(),
            "file": filepath.is_file(),
            "readable": os.access(filepath, os.R_OK),
            "writable": os.access(filepath, os.W_OK),
            "executable": os.access(filepath, os.X_OK),
        }

    @classmethod
    def watch(cls, filepath: Union[str, Path]) -> Iterator[tuple]:
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileError(f"File not found: {filepath}")

        last_mtime = filepath.stat().st_mtime

        while True:
            time.sleep(0.1)
            try:
                current_mtime = filepath.stat().st_mtime

                if current_mtime > last_mtime:
                    yield (filepath, current_mtime)
                    last_mtime = current_mtime
            except FileNotFoundError:
                break

    @classmethod
    def atomic_write(
        cls, filepath: Union[str, Path], data: Any, format: Optional[str] = None
    ) -> bool:
        filepath = Path(filepath)
        temp_file = filepath.with_suffix(f".tmp.{os.getpid()}")

        try:
            cls.write(temp_file, data, format=format)
            temp_file.replace(filepath)
            return True
        finally:
            if temp_file.exists():
                temp_file.unlink()

    @classmethod
    def _detect_format(cls, filepath: Path) -> str:
        ext = filepath.suffix.lower()

        if ext == ".json":
            return "json"
        elif ext in [".yaml", ".yml"]:
            return "yaml"
        elif ext == ".csv":
            return "csv"
        else:
            return "text"

    @classmethod
    def _parse_json(cls, content: str) -> Any:
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise FileError(f"Invalid JSON: {e}")

    @classmethod
    def _parse_yaml(cls, content: str) -> Any:
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise FileError(f"Invalid YAML: {e}")

    @classmethod
    def _parse_csv(cls, content: str) -> List[Dict[str, str]]:
        try:
            reader = csv.DictReader(StringIO(content))
            result = list(reader)
            # Check for malformed CSV by looking for incomplete parsing
            if '"unclosed quote' in content and not any(result):
                raise csv.Error("Malformed CSV with unclosed quotes")
            return result
        except (csv.Error, ValueError) as e:
            raise FileError(f"Invalid CSV: {e}")

    @classmethod
    def _generate_csv(cls, data: Any) -> str:
        if not data:
            return ""

        if isinstance(data, list) and isinstance(data[0], dict):
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            return output.getvalue()
        else:
            return str(data)
