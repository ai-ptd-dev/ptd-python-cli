---
description: Automatically transpile changed Python files to Rust
agent: rust-transpiler
model: anthropic/claude-sonnet-4-20250514
---

Automatically detect changed Python files and transpile them to Rust implementations.

## Git Status
!`git status --porcelain`

## Current Diff
!`git diff`

## Instructions:

1. **Detect Changes**: Look at the git status output above to identify modified Python files (.py)
2. **Analyze Changes**: Review the git diff to understand what changed in each Python file
3. **Transpile to Rust**: For each changed Python file:
   - Find the corresponding Rust file (e.g., src/basiccli/commands/hello.py → src/basiccli/commands/hello.rs)
   - Apply the equivalent changes to the Rust implementation
   - Ensure the Rust code follows idiomatic patterns and matches the Python functionality exactly
   - Handle any new error cases or edge cases introduced

4. **Test the Changes**:
   - Run the Rust tests: `cargo test`
   - Run the Python tests: `python -m pytest`
   - Ensure all tests pass

5. **Lint and Format**:
   - Run Rust linter: `cargo clippy`
   - Run Rust formatter: `cargo fmt`
   - Fix any issues found

6. **Verification**:
   - Build the Rust binary: `cargo build --release`
   - Compare outputs between Python and Rust implementations for consistency

## Project Structure:
- Python files: src/basiccli/**/*.py
- Rust files: src/basiccli/**/*.rs (side-by-side with Python)
- Python tests: tests/**/*test_*.py
- Rust tests: tests/**/*test_*.rs (side-by-side with Python)

## Important:
- Preserve the exact behavior and output formatting
- Match error messages and exit codes
- Ensure memory safety in Rust implementations
- Use the same algorithms and logic flow