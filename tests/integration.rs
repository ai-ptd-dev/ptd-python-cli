// Integration tests that use the subdirectory test files
// This allows us to keep test files next to their Python counterparts

mod commands {
    include!("commands/test_hello.rs");
    include!("commands/test_benchmark.rs");
    include!("commands/test_version.rs");
}

mod utils {
    include!("utils/test_file_handler.rs");
    include!("utils/test_logger.rs");
}
