// Rust tests for file handler utility
// Located next to test_file_handler.py for easy comparison

use basiccli::basiccli::utils::file_handler::FileHandler;
use tempfile::tempdir;


#[test]
fn file_handler_test_json_read_write() {
    let temp_dir = tempdir().unwrap();
    let file_path = temp_dir.path().join("test.json");
    
    let data = r#"{"name": "test", "value": 42, "items": ["a", "b", "c"]}"#;
    
    assert!(FileHandler::write(&file_path, data).is_ok());
    assert!(file_path.exists());
    
    let read_data = FileHandler::read(&file_path).unwrap();
    assert!(read_data.contains("test"));
    assert!(read_data.contains("42"));
}

#[test]
fn file_handler_test_copy_file() {
    let temp_dir = tempdir().unwrap();
    let source = temp_dir.path().join("source.txt");
    let dest = temp_dir.path().join("dest.txt");
    
    std::fs::write(&source, "test content").unwrap();
    
    assert!(FileHandler::copy(&source, &dest).is_ok());
    assert!(dest.exists());
    assert_eq!(std::fs::read_to_string(&dest).unwrap(), "test content");
}

#[test]
fn file_handler_test_move_file() {
    let temp_dir = tempdir().unwrap();
    let source = temp_dir.path().join("source.txt");
    let dest = temp_dir.path().join("dest.txt");
    
    std::fs::write(&source, "test content").unwrap();
    
    assert!(FileHandler::move_file(&source, &dest).is_ok());
    assert!(dest.exists());
    assert!(!source.exists());
}

#[test]
fn file_handler_test_delete_file() {
    let temp_dir = tempdir().unwrap();
    let file_path = temp_dir.path().join("test.txt");
    
    std::fs::write(&file_path, "test").unwrap();
    assert!(file_path.exists());
    
    assert!(FileHandler::delete(&file_path).is_ok());
    assert!(!file_path.exists());
}

#[test]
fn file_handler_test_checksum() {
    let temp_dir = tempdir().unwrap();
    let file_path = temp_dir.path().join("test.txt");
    
    std::fs::write(&file_path, "test content").unwrap();
    
    let checksum = FileHandler::checksum(&file_path, "sha256").unwrap();
    assert_eq!(checksum.len(), 64); // SHA256 produces 64-character hex string
}
