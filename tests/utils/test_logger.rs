// Rust tests for logger utility
// Located next to test_logger.py for easy comparison

use basiccli::basiccli::utils::logger::{Logger, LogLevel};


#[test]
fn logger_test_initialize_default_log_level() {
    let _logger = Logger::new(LogLevel::Info);
    // Test passes if no panic occurs during initialization
}

#[test]
fn logger_test_initialize_verbose_sets_debug_level() {
    let _logger = Logger::new(LogLevel::Debug);
    // Test passes if no panic occurs during initialization
}

#[test]
fn logger_test_debug_logging() {
    let logger = Logger::new(LogLevel::Debug);
    logger.debug("Test debug message");
    // Test passes if no panic occurs during logging
}

#[test]
fn logger_test_info_logging() {
    let logger = Logger::new(LogLevel::Info);
    logger.info("Test info message");
    // Test passes if no panic occurs during logging
}

#[test]
fn logger_test_warn_logging() {
    let logger = Logger::new(LogLevel::Warn);
    logger.warn("Test warning message");
    // Test passes if no panic occurs during logging
}

#[test]
fn logger_test_error_logging() {
    let logger = Logger::new(LogLevel::Error);
    logger.error("Test error message");
    // Test passes if no panic occurs during logging
}

#[test]
fn logger_test_fatal_logging() {
    let logger = Logger::new(LogLevel::Fatal);
    logger.fatal("Test fatal message");
    // Test passes if no panic occurs during logging
}

#[test]
fn logger_test_log_level_filtering() {
    let logger = Logger::new(LogLevel::Warn);
    
    logger.debug("Debug message");
    logger.info("Info message");
    logger.warn("Warning message");
    // Test passes if no panic occurs during logging
}

#[test]
fn logger_test_with_timing_context_manager() {
    let logger = Logger::new(LogLevel::Info);
    
    let result = logger.with_timing("Test operation", || {
        std::thread::sleep(std::time::Duration::from_millis(1));
        "done"
    });
    
    assert_eq!(result, "done");
}
