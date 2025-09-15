import sys
import threading
import time
from datetime import datetime
from enum import IntEnum
from typing import Any, Dict, Optional, TextIO


class LogLevel(IntEnum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    FATAL = 4


class Logger:
    COLORS = {
        LogLevel.DEBUG: "\033[36m",  # Cyan
        LogLevel.INFO: "\033[32m",  # Green
        LogLevel.WARN: "\033[33m",  # Yellow
        LogLevel.ERROR: "\033[31m",  # Red
        LogLevel.FATAL: "\033[35m",  # Magenta
        "reset": "\033[0m",
    }

    def __init__(
        self,
        level: LogLevel = LogLevel.INFO,
        verbose: bool = False,
        use_colors: bool = True,
        output: TextIO = sys.stdout,
    ):
        self.level = LogLevel.DEBUG if verbose else level
        self.use_colors = use_colors and output.isatty()
        self.output = output
        self.mutex = threading.Lock()

    def debug(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self._log(LogLevel.DEBUG, message, metadata or {})

    def info(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self._log(LogLevel.INFO, message, metadata or {})

    def warn(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self._log(LogLevel.WARN, message, metadata or {})

    def error(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self._log(LogLevel.ERROR, message, metadata or {})

    def fatal(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self._log(LogLevel.FATAL, message, metadata or {})

    def with_timing(self, message: str) -> Any:
        """Context manager for timing operations"""

        class TimingContext:
            def __init__(self, logger: "Logger", message: str) -> None:
                self.logger = logger
                self.message = message
                self.start_time: Optional[float] = None

            def __enter__(self) -> "TimingContext":
                self.start_time = time.perf_counter()
                self.logger.info(f"Starting: {self.message}")
                return self

            def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
                elapsed = time.perf_counter() - (self.start_time or 0)
                if exc_type is None:
                    self.logger.info(
                        f"Completed: {self.message} ({self._format_duration(elapsed)})"
                    )
                else:
                    self.logger.error(
                        f"Failed: {self.message} ({self._format_duration(elapsed)}) - {exc_val}"
                    )

            def _format_duration(self, seconds: float) -> str:
                if seconds < 1:
                    return f"{round(seconds * 1000, 2)}ms"
                elif seconds < 60:
                    return f"{round(seconds, 2)}s"
                else:
                    minutes = int(seconds // 60)
                    secs = round(seconds % 60)
                    return f"{minutes}m {secs}s"

        return TimingContext(self, message)

    def progress(self, current: int, total: int, message: str = "Progress") -> None:
        percentage = round(current / total * 100, 1)
        bar_length = 30
        filled = round(bar_length * (current / total))

        bar = ("█" * filled) + ("░" * (bar_length - filled))

        with self.mutex:
            self.output.write(f"\r{message}: [{bar}] {percentage}% ({current}/{total})")
            if current >= total:
                self.output.write("\n")
            self.output.flush()

    def _log(self, severity: LogLevel, message: str, metadata: Dict[str, Any]) -> None:
        if severity < self.level:
            return

        timestamp = datetime.now().isoformat()
        formatted_message = self._format_message(severity, timestamp, message, metadata)

        with self.mutex:
            self.output.write(formatted_message + "\n")
            self.output.flush()

    def _format_message(
        self, severity: LogLevel, timestamp: str, message: str, metadata: Dict[str, Any]
    ) -> str:
        severity_str = severity.name.ljust(5)

        if self.use_colors:
            severity_color = self.COLORS[severity]
            reset_color = self.COLORS["reset"]
            formatted = (
                f"{severity_color}[{timestamp}] {severity_str}{reset_color} | {message}"
            )
        else:
            formatted = f"[{timestamp}] {severity_str} | {message}"

        if metadata:
            formatted += f" | {self._format_metadata(metadata)}"

        return formatted

    def _format_metadata(self, metadata: Dict[str, Any]) -> str:
        return " ".join(f"{k}={repr(v)}" for k, v in metadata.items())


class FileLogger(Logger):
    def __init__(self, filename: str, **options: Any) -> None:
        self.file = open(filename, "a")
        super().__init__(**{**options, "output": self.file, "use_colors": False})

    def __del__(self) -> None:
        if hasattr(self, "file") and not self.file.closed:
            self.file.close()


class MultiLogger:
    def __init__(self, *loggers: Logger) -> None:
        self.loggers = loggers

    def debug(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        for logger in self.loggers:
            logger.debug(message, metadata)

    def info(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        for logger in self.loggers:
            logger.info(message, metadata)

    def warn(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        for logger in self.loggers:
            logger.warn(message, metadata)

    def error(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        for logger in self.loggers:
            logger.error(message, metadata)

    def fatal(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        for logger in self.loggers:
            logger.fatal(message, metadata)

    def with_timing(self, message: str) -> Any:
        return self.loggers[0].with_timing(message)

    def progress(self, current: int, total: int, message: str = "Progress") -> None:
        for logger in self.loggers:
            logger.progress(current, total, message)
