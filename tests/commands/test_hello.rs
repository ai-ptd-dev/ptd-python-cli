// Rust tests for hello command
// Located next to test_hello.py for easy comparison

use basiccli::basiccli::commands::hello::HelloCommand;

#[test]
fn hello_test_basic_greeting() {
    let command = HelloCommand::new("Alice".to_string(), false, 1);
    assert!(command.execute().is_ok());
}

#[test]
fn hello_test_uppercase_option() {
    let command = HelloCommand::new("Bob".to_string(), true, 1);
    assert!(command.execute().is_ok());
}

#[test]
fn hello_test_repeat_option() {
    let command = HelloCommand::new("Charlie".to_string(), false, 3);
    assert!(command.execute().is_ok());
}

#[test]
fn hello_test_greets_user_with_name() {
    let command = HelloCommand::new("Alice".to_string(), false, 1);
    assert!(command.execute().is_ok());
}

#[test]
fn hello_test_time_of_day_detection() {
    let command = HelloCommand::new("Test".to_string(), false, 1);
    let time_of_day = command.get_time_of_day();
    assert!(["Good morning", "Good afternoon", "Good evening"].contains(&time_of_day));
}

#[test]
fn hello_test_returns_successful_result() {
    let command = HelloCommand::new("Eve".to_string(), false, 1);
    assert!(command.execute().is_ok());
}

#[test]
fn hello_test_error_handling() {
    let command = HelloCommand::new("Test".to_string(), false, 0);
    assert!(command.execute().is_ok());
}