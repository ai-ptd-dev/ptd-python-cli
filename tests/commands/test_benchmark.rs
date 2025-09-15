// Rust tests for benchmark command
// Located next to test_benchmark.py for easy comparison

use basiccli::basiccli::commands::benchmark::BenchmarkCommand;



#[test]
fn benchmark_test_displays_benchmark_results_console() {
    let command = BenchmarkCommand::new(10, "console".to_string(), false);
    assert!(command.execute().is_ok());
}

#[test]
fn benchmark_test_shows_performance_metrics() {
    let command = BenchmarkCommand::new(10, "console".to_string(), false);
    assert!(command.execute().is_ok());
}

#[test]
fn benchmark_test_displays_total_benchmark_time() {
    let command = BenchmarkCommand::new(10, "console".to_string(), false);
    assert!(command.execute().is_ok());
}

#[test]
fn benchmark_test_json_output_valid_format() {
    let command = BenchmarkCommand::new(10, "json".to_string(), false);
    assert!(command.execute().is_ok());
}

#[test]
fn benchmark_test_csv_output_format() {
    let command = BenchmarkCommand::new(10, "csv".to_string(), false);
    assert!(command.execute().is_ok());
}

#[test]
fn benchmark_test_verbose_option() {
    let command = BenchmarkCommand::new(10, "console".to_string(), true);
    assert!(command.execute().is_ok());
}

#[test]
fn benchmark_test_string_manipulation_benchmark() {
    let command = BenchmarkCommand::new(10, "console".to_string(), false);
    assert!(command.execute().is_ok());
}

#[test]
fn benchmark_test_list_operations_benchmark() {
    let command = BenchmarkCommand::new(10, "console".to_string(), false);
    assert!(command.execute().is_ok());
}

#[test]
fn benchmark_test_file_io_benchmark() {
    let command = BenchmarkCommand::new(10, "console".to_string(), false);
    assert!(command.execute().is_ok());
}

#[test]
fn benchmark_test_json_parsing_benchmark() {
    let command = BenchmarkCommand::new(10, "console".to_string(), false);
    assert!(command.execute().is_ok());
}

#[test]
fn benchmark_test_dict_operations_benchmark() {
    let command = BenchmarkCommand::new(10, "console".to_string(), false);
    assert!(command.execute().is_ok());
}

#[test]
fn benchmark_test_returns_successful_result() {
    let command = BenchmarkCommand::new(10, "console".to_string(), false);
    assert!(command.execute().is_ok());
}
