import csv
import json
import platform
import sys
import tempfile
import time
from dataclasses import dataclass
from io import StringIO
from typing import Any, Dict

from ..utils.result import Result


@dataclass
class BenchmarkCommand:
    iterations: int
    output_format: str = "console"
    verbose: bool = False

    def execute(self) -> Result:
        try:
            if self.verbose:
                print(f"Running benchmarks with {self.iterations} iterations...")

            results = self._run_benchmarks()

            if self.output_format == "json":
                self._output_json(results)
            elif self.output_format == "csv":
                self._output_csv(results)
            else:
                self._output_console(results)

            return Result(success=True, message="Benchmarks completed successfully")
        except Exception as e:
            return Result(success=False, message=str(e))

    def _run_benchmarks(self) -> Dict[str, Dict[str, Any]]:
        results = {}

        # String manipulation benchmark
        results["string_manipulation"] = self._benchmark_string_manipulation()

        # List operations benchmark
        results["list_operations"] = self._benchmark_list_operations()

        # File I/O benchmark
        results["file_io"] = self._benchmark_file_io()

        # JSON parsing benchmark
        results["json_parsing"] = self._benchmark_json_parsing()

        # Dict operations benchmark
        results["dict_operations"] = self._benchmark_dict_operations()

        return results

    def _benchmark_string_manipulation(self) -> Dict[str, Any]:
        start_time = time.perf_counter()

        for i in range(self.iterations):
            text = f"Hello World {i}"
            text = text.upper()
            text = text[::-1]  # reverse
            text = "".join("*" if c in "AEIOU" else c for c in text)
            "-".join(text)

        end_time = time.perf_counter()
        total_time = end_time - start_time

        return {
            "name": "String Manipulation",
            "iterations": self.iterations,
            "total_time": total_time,
            "avg_time": total_time / self.iterations,
            "ops_per_sec": self.iterations / total_time,
        }

    def _benchmark_list_operations(self) -> Dict[str, Any]:
        start_time = time.perf_counter()

        for _ in range(self.iterations):
            arr = list(range(1, 101))
            arr = [n * 2 for n in arr]
            arr = [n for n in arr if n % 3 == 0]
            arr = sorted(arr, reverse=True)
            sum(arr)

        end_time = time.perf_counter()
        total_time = end_time - start_time

        return {
            "name": "List Operations",
            "iterations": self.iterations,
            "total_time": total_time,
            "avg_time": total_time / self.iterations,
            "ops_per_sec": self.iterations / total_time,
        }

    def _benchmark_file_io(self) -> Dict[str, Any]:
        start_time = time.perf_counter()

        with tempfile.NamedTemporaryFile(mode="w+", delete=True) as temp_file:
            for i in range(self.iterations):
                temp_file.seek(0)
                temp_file.write(f"Line {i}: {'x' * 100}\n")
                temp_file.flush()
                temp_file.seek(0)
                temp_file.read()

        end_time = time.perf_counter()
        total_time = end_time - start_time

        return {
            "name": "File I/O",
            "iterations": self.iterations,
            "total_time": total_time,
            "avg_time": total_time / self.iterations,
            "ops_per_sec": self.iterations / total_time,
        }

    def _benchmark_json_parsing(self) -> Dict[str, Any]:
        sample_data = {
            "users": [
                {
                    "id": i,
                    "name": f"User {i}",
                    "email": f"user{i}@example.com",
                    "metadata": {
                        "created_at": time.ctime(),
                        "tags": ["python", "ptd", "cli", "benchmark"],
                    },
                }
                for i in range(1, 11)
            ]
        }

        json_string = json.dumps(sample_data)

        start_time = time.perf_counter()

        for _ in range(self.iterations):
            parsed = json.loads(json_string)
            json.dumps(parsed)

        end_time = time.perf_counter()
        total_time = end_time - start_time

        return {
            "name": "JSON Parsing",
            "iterations": self.iterations,
            "total_time": total_time,
            "avg_time": total_time / self.iterations,
            "ops_per_sec": self.iterations / total_time,
        }

    def _benchmark_dict_operations(self) -> Dict[str, Any]:
        start_time = time.perf_counter()

        for _ in range(self.iterations):
            data = {}
            for i in range(100):
                data[f"key_{i}"] = i * 2
            sorted(data.keys())
            sum(data.values())
            data.update({"extra": 999})
            {k: v for k, v in data.items() if isinstance(v, int) and v > 50}

        end_time = time.perf_counter()
        total_time = end_time - start_time

        return {
            "name": "Dict Operations",
            "iterations": self.iterations,
            "total_time": total_time,
            "avg_time": total_time / self.iterations,
            "ops_per_sec": self.iterations / total_time,
        }

    def _output_console(self, results: Dict[str, Dict[str, Any]]) -> None:
        print("\n" + "=" * 60)
        print(f"{' ' * 20}BENCHMARK RESULTS")
        print("=" * 60)

        for result in results.values():
            print(f"\n{result['name']}:")
            print(f"  Iterations:     {result['iterations']}")
            print(f"  Total time:     {self._format_time(result['total_time'])}")
            print(f"  Avg time/op:    {self._format_time(result['avg_time'])}")
            print(f"  Ops/second:     {result['ops_per_sec']:.2f}")

        total_time = sum(r["total_time"] for r in results.values())
        print("\n" + "=" * 60)
        print(f"Total benchmark time: {self._format_time(total_time)}")
        print("=" * 60)

    def _output_json(self, results: Dict[str, Dict[str, Any]]) -> None:
        output = {
            "timestamp": time.ctime(),
            "platform": platform.platform(),
            "python_version": sys.version.split()[0],
            "benchmarks": [
                {
                    "name": r["name"],
                    "iterations": r["iterations"],
                    "total_time_ms": round(r["total_time"] * 1000, 3),
                    "avg_time_ms": round(r["avg_time"] * 1000, 6),
                    "ops_per_second": round(r["ops_per_sec"], 2),
                }
                for r in results.values()
            ],
        }

        print(json.dumps(output, indent=2))

    def _output_csv(self, results: Dict[str, Dict[str, Any]]) -> None:
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(
            ["Benchmark", "Iterations", "Total Time (s)", "Avg Time (s)", "Ops/Second"]
        )

        for r in results.values():
            writer.writerow(
                [
                    r["name"],
                    r["iterations"],
                    round(r["total_time"], 6),
                    round(r["avg_time"], 9),
                    round(r["ops_per_sec"], 2),
                ]
            )

        print(output.getvalue())

    def _format_time(self, seconds: float) -> str:
        if seconds < 0.001:
            return f"{round(seconds * 1_000_000, 2)} μs"
        elif seconds < 1:
            return f"{round(seconds * 1000, 2)} ms"
        else:
            return f"{round(seconds, 2)} s"
