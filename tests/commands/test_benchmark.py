import json
import sys

sys.path.insert(0, "src")

import pytest  # noqa: E402

from basiccli.commands.benchmark import BenchmarkCommand  # noqa: E402


class TestBenchmarkCommand:
    @pytest.fixture
    def iterations(self):
        return 10  # Use small number for tests

    def test_displays_benchmark_results_console(self, iterations, capsys):
        command = BenchmarkCommand(iterations)
        result = command.execute()

        captured = capsys.readouterr()
        assert "BENCHMARK RESULTS" in captured.out
        assert "String Manipulation" in captured.out
        assert "List Operations" in captured.out
        assert "File I/O" in captured.out
        assert "JSON Parsing" in captured.out
        assert "Dict Operations" in captured.out
        assert result.success is True

    def test_shows_performance_metrics(self, iterations, capsys):
        command = BenchmarkCommand(iterations)
        command.execute()

        captured = capsys.readouterr()
        assert "Iterations:" in captured.out
        assert "Total time:" in captured.out
        assert "Avg time/op:" in captured.out
        assert "Ops/second:" in captured.out

    def test_displays_total_benchmark_time(self, iterations, capsys):
        command = BenchmarkCommand(iterations)
        command.execute()

        captured = capsys.readouterr()
        assert "Total benchmark time:" in captured.out

    def test_json_output_valid_format(self, iterations, capsys):
        command = BenchmarkCommand(iterations, output_format="json")
        command.execute()

        captured = capsys.readouterr()
        json_data = json.loads(captured.out)

        assert "timestamp" in json_data
        assert "platform" in json_data
        assert "python_version" in json_data
        assert "benchmarks" in json_data

    def test_json_includes_all_benchmark_results(self, iterations, capsys):
        command = BenchmarkCommand(iterations, output_format="json")
        command.execute()

        captured = capsys.readouterr()
        json_data = json.loads(captured.out)
        benchmarks = json_data["benchmarks"]

        assert isinstance(benchmarks, list)
        assert len(benchmarks) == 5

        benchmark_names = [b["name"] for b in benchmarks]
        assert "String Manipulation" in benchmark_names
        assert "List Operations" in benchmark_names
        assert "File I/O" in benchmark_names
        assert "JSON Parsing" in benchmark_names
        assert "Dict Operations" in benchmark_names

    def test_json_includes_timing_data(self, iterations, capsys):
        command = BenchmarkCommand(iterations, output_format="json")
        command.execute()

        captured = capsys.readouterr()
        json_data = json.loads(captured.out)
        benchmarks = json_data["benchmarks"]

        for benchmark in benchmarks:
            assert "iterations" in benchmark
            assert "total_time_ms" in benchmark
            assert "avg_time_ms" in benchmark
            assert "ops_per_second" in benchmark

    def test_csv_output_format(self, iterations, capsys):
        command = BenchmarkCommand(iterations, output_format="csv")
        command.execute()

        captured = capsys.readouterr()
        lines = captured.out.split("\n")
        assert "Benchmark,Iterations,Total Time" in lines[0]
        assert len(lines) > 1

    def test_verbose_option(self, iterations, capsys):
        command = BenchmarkCommand(iterations, verbose=True)
        command.execute()

        captured = capsys.readouterr()
        assert f"Running benchmarks with {iterations} iterations" in captured.out

    def test_string_manipulation_benchmark(self, iterations):
        command = BenchmarkCommand(iterations)
        result = command._benchmark_string_manipulation()

        assert result["name"] == "String Manipulation"
        assert result["iterations"] == iterations
        assert isinstance(result["total_time"], float)
        assert isinstance(result["avg_time"], float)
        assert result["ops_per_sec"] > 0

    def test_list_operations_benchmark(self, iterations):
        command = BenchmarkCommand(iterations)
        result = command._benchmark_list_operations()

        assert result["name"] == "List Operations"
        assert isinstance(result["total_time"], float)

    def test_file_io_benchmark(self, iterations):
        command = BenchmarkCommand(iterations)
        result = command._benchmark_file_io()

        assert result["name"] == "File I/O"
        assert isinstance(result["total_time"], float)

    def test_json_parsing_benchmark(self, iterations):
        command = BenchmarkCommand(iterations)
        result = command._benchmark_json_parsing()

        assert result["name"] == "JSON Parsing"
        assert isinstance(result["total_time"], float)

    def test_dict_operations_benchmark(self, iterations):
        command = BenchmarkCommand(iterations)
        result = command._benchmark_dict_operations()

        assert result["name"] == "Dict Operations"
        assert isinstance(result["total_time"], float)

    def test_returns_successful_result(self, iterations):
        command = BenchmarkCommand(iterations)
        result = command.execute()

        assert result.success is True
        assert result.is_success() is True
        assert "Benchmarks completed successfully" in result.message
