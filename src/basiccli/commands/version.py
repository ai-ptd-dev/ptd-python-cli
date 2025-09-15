import json
import platform
import sys
from dataclasses import dataclass
from typing import Any, Dict

from ..utils.result import Result


@dataclass
class VersionCommand:
    output_json: bool = False

    VERSION = "1.0.0"
    BUILD_DATE = "2025-01-15"

    def execute(self) -> Result:
        try:
            version_info = self._build_version_info()

            if self.output_json:
                print(json.dumps(version_info, indent=2))
            else:
                self._display_formatted(version_info)

            return Result(success=True, message="Version displayed successfully")
        except Exception as e:
            return Result(success=False, message=str(e))

    def _build_version_info(self) -> Dict[str, Any]:
        return {
            "name": "BasicCli",
            "version": self.VERSION,
            "build_date": self.BUILD_DATE,
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "description": "Polyglot Transpilation Development Reference Implementation",
            "repository": "https://github.com/ai-ptd-dev/ptd-python-cli",
        }

    def _display_formatted(self, info: Dict[str, Any]) -> None:
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                       BasicCli                            ║")
        print("╠═══════════════════════════════════════════════════════════╣")
        print(f"║ Version:        {info['version']:<44} ║")
        print(f"║ Build Date:     {info['build_date']:<44} ║")
        print(f"║ Python Version: {info['python_version']:<44} ║")
        print(f"║ Platform:       {info['platform']:<44} ║")
        print("╠═══════════════════════════════════════════════════════════╣")
        print(f"║ {info['description']:^57} ║")
        print("╚═══════════════════════════════════════════════════════════╝")
