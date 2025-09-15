# Getting Started with BasicCli

## Prerequisites

### For Python Development
- Python 3.10+ (recommend 3.12+ for best performance)
- pip (`pip install -r requirements-dev.txt`)

### For Rust Compilation
- Rust 1.70+ ([install from rustup.rs](https://rustup.rs/))
- Cargo (comes with Rust)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ai-ptd-dev/ptd-python-cli
cd ptd-python-cli
```

### 2. Install Python Dependencies
```bash
pip install -r requirements-dev.txt
```

### 3. Compile Rust Binary (Optional)
```bash
./bin/compile
```

## Project Structure

```
ptd-python-cli/
├── src/
│   ├── basiccli/
│   │   ├── cli.py          # Python CLI entry point
│   │   ├── commands/
│   │   │   ├── hello.py    # Python command
│   │   │   ├── hello.rs    # Rust command (side-by-side)
│   │   │   ├── version.py
│   │   │   ├── version.rs
│   │   │   └── ...
│   │   └── utils/
│   │       ├── logger.py   # Python utility
│   │       ├── logger.rs   # Rust utility (side-by-side)
│   │       └── ...
│   ├── cli.rs              # Rust CLI entry point
│   └── lib.rs              # Rust library exports
├── tests/
│   ├── commands/
│   │   ├── test_hello.py   # Python tests
│   │   ├── test_hello.rs   # Rust tests (side-by-side)
│   │   └── ...
│   └── utils/
│       ├── test_logger.py  # Python utility tests
│       ├── test_logger.rs  # Rust utility tests (side-by-side)
│       └── ...
├── bin/
│   ├── basiccli-python     # Python executable
│   ├── basiccli-rust       # Rust executable
│   ├── compile             # Build Rust binary
│   ├── test               # Run Rust tests
│   ├── pytest            # Run Python tests
│   └── lint               # Lint both languages
└── docs/                   # Documentation
```

## Running the CLI

### Python Version (Development)
```bash
# Using the script
./bin/basiccli-python hello "World"

# Direct execution
PYTHONPATH=src python -m basiccli.cli hello "World"
```

### Rust Version (Production)
```bash
# First compile
./bin/compile

# Then run
./bin/basiccli-rust hello "World"

# Or directly
./target/release/basiccli-rust hello "World"
```

## Available Commands

### Hello Command
```bash
# Basic greeting
./bin/basiccli-python hello "Alice"

# With options
./bin/basiccli-python hello "Bob" --uppercase --repeat 3
```

### Version Command
```bash
# Human-readable
./bin/basiccli-python version

# JSON output
./bin/basiccli-python version --json
```

### Benchmark Command
```bash
# Run benchmarks
./bin/basiccli-python benchmark 1000

# Output formats
./bin/basiccli-python benchmark 1000 --output json
./bin/basiccli-python benchmark 1000 --output csv

# Verbose mode
./bin/basiccli-python benchmark 1000 --verbose
```

### Process Command
```bash
# Process JSON file
./bin/basiccli-python process data.json

# With options
./bin/basiccli-python process data.json --pretty --stats
```

## Development Workflow

### 1. Write Python Code
Create your command in `src/basiccli/commands/`:
```python
from dataclasses import dataclass
from typing import Optional

from ..utils.result import Result

@dataclass
class MyCommand:
    name: str
    options: Optional[dict] = None
    
    def execute(self) -> Result:
        print(f"Hello from MyCommand, {self.name}!")
        return Result(success=True, message="Command executed successfully")
```

### 2. Add to CLI
Register in `src/basiccli/cli.py`:
```python
@cli.command()
@click.argument('name')
def mycommand(name: str):
    """Description here"""
    command = MyCommand(name)
    result = command.execute()
    if not result.success:
        click.echo(f"Error: {result.message}", err=True)
        sys.exit(1)
```

### 3. Write Tests
Create `tests/commands/test_mycommand.py`:
```python
import sys

sys.path.insert(0, "src")

from basiccli.commands.mycommand import MyCommand  # noqa: E402

def test_executes_successfully():
    command = MyCommand("TestUser")
    result = command.execute()
    assert result.success is True
    assert "TestUser" in result.message
```

### 4. Run Tests
```bash
./bin/pytest
```

### 5. Transpile to Rust
Create side-by-side `src/basiccli/commands/mycommand.rs`:
```rust
use anyhow::Result;

pub struct MyCommand {
    name: String,
}

impl MyCommand {
    pub fn new(name: String) -> Self {
        Self { name }
    }
    
    pub fn execute(&self) -> Result<()> {
        println!("Hello from MyCommand, {}!", self.name);
        Ok(())
    }
}
```

### 6. Compile and Test
```bash
./bin/compile
./bin/test
```

## Helper Scripts

### `bin/compile`
Builds the Rust binary with optimizations:
```bash
./bin/compile
```

### `bin/test`
Runs Rust tests:
```bash
./bin/test
```

### `bin/pytest`
Runs Python tests:
```bash
./bin/pytest
```

### `bin/lint`
Lints and auto-fixes both Python and Rust:
```bash
./bin/lint
```

## Performance Comparison

Compare Python vs Rust performance:
```bash
# Python version
time ./bin/basiccli-python benchmark 1000

# Rust version
time ./bin/basiccli-rust benchmark 1000
```

## Next Steps

1. **Explore the code**: Look at existing commands for patterns
2. **Add your command**: Follow the development workflow
3. **Benchmark**: Compare Python vs Rust performance
4. **Optimize**: Profile and improve bottlenecks
5. **Deploy**: Use the Rust binary in production

## Tips

- Keep Python and Rust implementations functionally identical
- Use Python for rapid prototyping
- Transpile to Rust for production deployment
- Run both test suites to ensure parity
- Use the performance benchmarks to validate improvements
- Files are organized side-by-side for easy comparison and maintenance