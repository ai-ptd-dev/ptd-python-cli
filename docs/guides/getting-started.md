# Getting Started with BasicCli

## Prerequisites

### For Python Development
- Python 2.7+ (recommend 3.2+ for YJIT)
- Bundler (`pip install -r requirements-dev.txt`)

### For Rust Compilation
- Rust 1.70+ ([install from rustup.rs](https://rustup.rs/))
- Cargo (comes with Rust)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ai-ptd-dev/basiccli
cd basiccli
```

### 2. Install Python Dependencies
```bash
bundle install
```

### 3. Compile Rust Binary (Optional)
```bash
./bin/compile
```

## Project Structure

```
basiccli/
├── src/
│   ├── cli.rb              # Python CLI entry point
│   ├── cli.rs              # Rust CLI entry point (transpiled)
│   ├── commands/
│   │   ├── hello.rb        # Python command
│   │   ├── hello.rs        # Rust command (transpiled)
│   │   ├── version.rb
│   │   ├── version.rs
│   │   └── ...
│   └── utils/
│       ├── logger.rb       # Python utility
│       ├── logger.rs       # Rust utility (transpiled)
│       └── ...
├── spec/
│   ├── commands/
│   │   ├── hello_spec.rb   # Python tests
│   │   ├── hello_test.rs   # Rust tests
│   │   └── ...
│   └── spec_helper.rb
├── bin/
│   ├── basiccli-python       # Python executable
│   ├── basiccli-rust       # Rust executable
│   ├── compile             # Build Rust binary
│   ├── test               # Run Rust tests
│   ├── pytest              # Run Python tests
│   └── lint               # Lint both languages
└── docs/                   # Documentation
```

## Running the CLI

### Python Version (Development)
```bash
# Using the script
./bin/basiccli-python hello "World"

# Direct execution
python -m basiccli.cli hello "World"
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
Create your command in `src/commands/`:
```ruby
module BasicCli
  module Commands
    class MyCommand
      def initialize(options = {})
        @options = options
      end
      
      def execute
        puts "Hello from MyCommand!"
      end
    end
  end
end
```

### 2. Add to CLI
Register in `src/cli.rb`:
```ruby
desc "mycommand", "Description here"
def mycommand
  command = Commands::MyCommand.new(options)
  command.execute
end
```

### 3. Write Tests
Create `spec/commands/mycommand_spec.rb`:
```ruby
RSpec.describe BasicCli::Commands::MyCommand do
  it 'executes successfully' do
    command = described_class.new
    expect { command.execute }.to output(/Hello/).to_stdout
  end
end
```

### 4. Run Tests
```bash
./bin/rspec
```

### 5. Transpile to Rust
Manually create `src/commands/mycommand.rs`:
```rust
pub struct MyCommand {
    // fields
}

impl MyCommand {
    pub fn new() -> Self {
        Self {}
    }
    
    pub fn execute(&self) -> Result<()> {
        println!("Hello from MyCommand!");
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

### `bin/rspec`
Runs Python tests:
```bash
./bin/rspec
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