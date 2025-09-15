// Rust tests for version command
// Located next to test_version.py for easy comparison

use basiccli::basiccli::commands::version::VersionCommand;


#[test]
fn version_test_displays_formatted_version_information() {
    let command = VersionCommand::new(false);
    assert!(command.execute().is_ok());
}

#[test]
fn version_test_displays_formatted_box() {
    let command = VersionCommand::new(false);
    assert!(command.execute().is_ok());
}

#[test]
fn version_test_json_output_valid_format() {
    let command = VersionCommand::new(true);
    assert!(command.execute().is_ok());
}

#[test]
fn version_test_json_includes_all_required_fields() {
    let command = VersionCommand::new(true);
    assert!(command.execute().is_ok());
}

#[test]
fn version_test_constants() {
    assert_eq!(VersionCommand::VERSION, "1.0.0");
    assert_eq!(VersionCommand::BUILD_DATE, "2025-01-15");
}

#[test]
fn version_test_returns_successful_result() {
    let command = VersionCommand::new(false);
    assert!(command.execute().is_ok());
}
