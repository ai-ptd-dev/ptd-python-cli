import sys
import tempfile
from io import StringIO
from unittest.mock import MagicMock

sys.path.insert(0, "src")

import pytest  # noqa: E402

from basiccli.utils.logger import (  # noqa: E402
    FileLogger,
    Logger,
    LogLevel,
    MultiLogger,
)


class TestLogger:
    @pytest.fixture
    def output(self):
        return StringIO()

    @pytest.fixture
    def logger(self, output):
        return Logger(output=output, use_colors=False)

    def test_initialize_default_log_level(self, output):
        logger = Logger(output=output)
        assert logger.level == LogLevel.INFO

    def test_initialize_verbose_sets_debug_level(self, output):
        verbose_logger = Logger(verbose=True, output=output)
        assert verbose_logger.level == LogLevel.DEBUG

    def test_color_detection(self):
        tty_output = MagicMock()
        tty_output.isatty.return_value = True

        color_logger = Logger(output=tty_output)
        assert color_logger.use_colors is True

    def test_debug_logging(self, logger, output):
        logger.level = LogLevel.DEBUG
        logger.debug("Debug message")

        assert "DEBUG" in output.getvalue()
        assert "Debug message" in output.getvalue()

    def test_info_logging(self, logger, output):
        logger.info("Info message")

        assert "INFO" in output.getvalue()
        assert "Info message" in output.getvalue()

    def test_warn_logging(self, logger, output):
        logger.warn("Warning message")

        assert "WARN" in output.getvalue()
        assert "Warning message" in output.getvalue()

    def test_error_logging(self, logger, output):
        logger.error("Error message")

        assert "ERROR" in output.getvalue()
        assert "Error message" in output.getvalue()

    def test_fatal_logging(self, logger, output):
        logger.fatal("Fatal message")

        assert "FATAL" in output.getvalue()
        assert "Fatal message" in output.getvalue()

    def test_metadata_logging(self, logger, output):
        logger.info("Message", {"user_id": 123, "action": "login"})

        assert "user_id=123" in output.getvalue()
        assert "action='login'" in output.getvalue()

    def test_log_level_filtering(self, logger, output):
        logger.level = LogLevel.WARN

        logger.debug("Debug")
        logger.info("Info")
        logger.warn("Warning")

        output_str = output.getvalue()
        assert "Debug" not in output_str
        assert "Info" not in output_str
        assert "Warning" in output_str

    def test_with_timing_context_manager(self, logger, output):
        with logger.with_timing("Task"):
            pass

        output_str = output.getvalue()
        assert "Starting: Task" in output_str
        assert "Completed: Task" in output_str

    def test_with_timing_includes_duration(self, logger, output):
        import time

        with logger.with_timing("Quick task"):
            time.sleep(0.01)

        output_str = output.getvalue()
        assert "Completed: Quick task" in output_str
        assert "ms" in output_str or "s" in output_str

    def test_with_timing_error_handling(self, logger, output):
        with pytest.raises(ValueError):
            with logger.with_timing("Failing task"):
                raise ValueError("Test error")

        output_str = output.getvalue()
        assert "Failed: Failing task" in output_str
        assert "Test error" in output_str

    def test_progress_display(self, logger, output):
        logger.progress(50, 100, "Loading")

        output_str = output.getvalue()
        assert "Loading:" in output_str
        assert "[" in output_str
        assert "]" in output_str
        assert "50.0%" in output_str
        assert "(50/100)" in output_str

    def test_progress_filled_unfilled(self, logger, output):
        logger.progress(30, 100, "Processing")

        output_str = output.getvalue()
        assert "█" in output_str
        assert "░" in output_str

    def test_progress_completion_newline(self, logger, output):
        logger.progress(100, 100, "Done")

        output_str = output.getvalue()
        assert output_str.endswith("\n")

    def test_color_support(self):
        tty_output = MagicMock()
        tty_output.isatty.return_value = True

        color_logger = Logger(output=tty_output, use_colors=True)
        color_logger.info("Colored message")

        # Check that write was called with color codes
        written_content = "".join(
            call[0][0] for call in tty_output.write.call_args_list
        )
        assert "\033[" in written_content

    def test_timestamp_formatting(self, logger, output):
        logger.info("Test")

        # Check for ISO8601-like timestamp format
        import re

        output_str = output.getvalue()
        timestamp_pattern = r"\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
        assert re.search(timestamp_pattern, output_str)


class TestFileLogger:
    def test_writes_logs_to_file(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            file_logger = FileLogger(temp_file.name)
            file_logger.info("File log message")

            # Read the file content
            temp_file.seek(0)
            content = temp_file.read()
            assert "File log message" in content

    def test_no_colors_in_file_output(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            file_logger = FileLogger(temp_file.name)
            file_logger.info("No colors")

            temp_file.seek(0)
            content = temp_file.read()
            assert "\033[" not in content


class TestMultiLogger:
    @pytest.fixture
    def outputs(self):
        return StringIO(), StringIO()

    @pytest.fixture
    def loggers(self, outputs):
        output1, output2 = outputs
        logger1 = Logger(output=output1, use_colors=False)
        logger2 = Logger(output=output2, use_colors=False)
        return logger1, logger2

    @pytest.fixture
    def multi_logger(self, loggers):
        logger1, logger2 = loggers
        return MultiLogger(logger1, logger2)

    def test_logs_to_all_loggers(self, multi_logger, outputs):
        output1, output2 = outputs
        multi_logger.info("Multi message")

        assert "Multi message" in output1.getvalue()
        assert "Multi message" in output2.getvalue()

    def test_supports_all_log_levels(self, multi_logger, loggers, outputs):
        logger1, logger2 = loggers
        output1, output2 = outputs

        logger1.level = LogLevel.DEBUG
        logger2.level = LogLevel.DEBUG

        for level_name in ["debug", "info", "warn", "error", "fatal"]:
            getattr(multi_logger, level_name)(f"{level_name} message")

            assert level_name.upper() in output1.getvalue()
            assert level_name.upper() in output2.getvalue()

    def test_delegates_with_timing(self, multi_logger, outputs):
        output1, output2 = outputs

        with multi_logger.with_timing("Task"):
            pass

        output1_str = output1.getvalue()
        assert "Starting: Task" in output1_str
        assert "Completed: Task" in output1_str
