# Agent Instructions for PTD Python CLI

## Build/Test/Lint Commands
- **Python tests**: `python -m pytest` or `./bin/pytest`
- **Python single test**: `python -m pytest path/to/test.py::test_name` or `python -m pytest -k "test description"`
- **Rust tests**: `cargo test` or `./bin/test`
- **Rust single test**: `cargo test test_name` or `cargo test --test test_file_name`
- **Lint both**: `./bin/lint` (auto-fixes Python with black/isort, Rust with rustfmt/clippy)
- **Compile Rust**: `./bin/compile` or `cargo build --release`

## Code Style Guidelines
**Python**: Double quotes for strings, snake_case methods/vars, PascalCase classes, 88 char lines, type hints encouraged
**Rust**: Use Result<T,E> for errors, prefer &str over String, implement Display/Debug traits, use anyhow for error handling
**Imports**: Python uses relative imports for internal deps; Rust uses anyhow::Result, chrono for time, colored for output
**Testing**: Python pytest with descriptive test functions; Rust #[test] functions in same file or tests/ directory
**Naming**: Commands in src/basiccli/commands/, utilities in src/basiccli/utils/, maintain Python/Rust file parity (e.g., hello.py/hello.rs)
**Error Handling**: Python returns Result objects with success/message; Rust uses Result<(), anyhow::Error>
**Project Structure**: Polyglot development - write Python first, transpile to Rust maintaining same API and behavior

## PTD Paradigm
Develop features in Python for rapid iteration, then transpile to Rust for 50x faster startup and deployment.

## Development Policy
**IMPORTANT**: All new features and modifications should be implemented in Python code only. Do not write or modify Rust code directly. The Rust code will be generated through transpilation from the Python implementation.