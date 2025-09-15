# PTD Python CLI - Developer-First Framework with OpenCode AI

> **Write Python, Ship Rust**: Real developers using OpenCode AI agents to achieve 250x performance gains through automatic transpilation.

This framework demonstrates **PTD (Polyglot Transpilation Development)** - a developer-first approach where you write Python code and OpenCode AI agents automatically create optimized Rust versions. No manual porting, no compromise on performance.

**Note**: This is a Python/Rust implementation forked from the original [Ruby/Rust PTD repository](https://github.com/ai-ptd-dev/ptd-ruby-cli). All concepts and methodologies remain the same, but now using Python as the high-level language instead of Ruby.

## 🚀 Quick Start for Developers

### Start Your Own Project (Fork This!)
```bash
# 1. Fork this repository on GitHub first, then:
git clone https://github.com/YOUR-USERNAME/ptd-python-cli.git
cd ptd-python-cli

# 2. Install dependencies
pip install -r requirements-dev.txt

# 3. Customize it for your project with OpenCode
opencode
> /setup
> [Answer questions about your CLI project]
> [AI renames everything and configures your project]
> /transpile  # (if /setup renamed things)
> [AI generates Rust versions of your renamed code]
> exit

# 4. Try the example commands (now with your project name!)
./bin/yourcli-python hello
./bin/yourcli-python version

# 5. Build and run the Rust version
./bin/compile
./bin/yourcli-rust hello  # 250x faster startup!
```

### See a Complete Example: TodoCLI
Want to see what you can build? Check out the **[todo-list-example branch](https://github.com/ai-ptd-dev/ptd-python-cli/tree/todo-list-example)**:
- Full todo list manager with SQLite
- 7 commands, 69 tests, 250x performance gain
- Shows OpenCode agents in action

```bash
# View the example (don't clone, just browse)
# https://github.com/ai-ptd-dev/ptd-python-cli/tree/todo-list-example
```

## 📊 AI-Achieved Performance Gains

OpenCode agents automatically optimized the transpilation to achieve:

| Metric | Python | Rust | AI Improvement |
|--------|--------|------|----------------|
| **Startup Time** | 250ms | 1ms | **250x faster** |
| **Memory Usage** | 29MB | 3MB | **90% reduction** |
| **Binary Size** | 40MB+ deps | 1.1MB | **97% smaller** |
| **Cold Start** | Python + venv | Native binary | **Instant execution** |

## 🎯 What is PTD?

**Polyglot Transpilation Development** is an AI-powered programming paradigm where:

1. **🚀 Rapid Development**: Write in expressive languages (Python, Ruby)
2. **🤖 AI Transpilation**: OpenCode agents automatically convert to system languages (Rust, Go)  
3. **⚡ Production Deployment**: Ship optimized native binaries with massive performance gains
4. **🔄 Continuous Parity**: Maintain identical functionality across language implementations

### The OpenCode Advantage

- **🧠 AI-Powered**: Agents understand semantics, not just syntax
- **🎯 Context-Aware**: Maintains business logic and error handling
- **📋 Test Generation**: Creates comprehensive test suites automatically
- **🔧 Optimization**: Applies language-specific performance patterns
- **🔄 Language Agnostic**: Works with Python→Rust (this repo) and Ruby→Rust (original)

[Learn more about PTD →](docs/base/ptd-paradigm.md)

## 🤖 OpenCode Integration

### The .opencode Directory - Your AI Development Team

```
.opencode/
├── agent/                  # AI agent personalities
│   ├── python-dev.md      # Python expert following SOLID principles
│   └── rust-transpiler.md # Rust expert for transpilation
└── command/               # OpenCode commands you can run
    ├── transpile.md       # Auto-transpile Python changes to Rust
    └── setup.md          # Convert boilerplate to your project
```

### How to Use OpenCode Agents

```bash
# 1. Start an OpenCode interactive session
opencode

# 2. Inside the OpenCode session, use these commands:
/setup      # Interactive setup for your new project (after forking)
            # - Asks for project name, description, purpose
            # - Renames all BasicCli references to your project
            # - Updates documentation and configuration

/transpile  # Automatically transpile Python changes to Rust
            # - Detects modified Python files via git
            # - Generates equivalent Rust code
            # - Runs tests for both languages
            # - Applies formatting and linting

# 3. Or call specific agents directly:
@python-dev      # Python expert for SOLID principles & clean code
                 # "Create a new command that processes CSV files"
                 
@rust-transpiler # Rust expert for manual transpilation
                 # "Convert this Python method to idiomatic Rust"

# 4. Example workflow after forking:
opencode
> /setup
> "What is your CLI project name?" MyCoolTool
> "What does your CLI do?" Manages deployments
> [AI renames everything and sets up your project]

# 5. Development cycle:
vim src/basiccli/commands/deploy.py  # Write Python code
opencode
> /transpile                          # AI transpiles to Rust
# OR manually with agents:
> @python-dev help me improve this command
> @rust-transpiler convert the deploy command to Rust
> exit

./bin/pytest                         # Verify Python tests
./bin/test                           # Verify Rust tests  
./bin/compile                        # Build optimized binary
```

### Developer Workflow with OpenCode

1. **Write Python First**: Focus on functionality, not performance
2. **OpenCode Transpiles**: AI agents convert to idiomatic Rust
3. **Tests Ensure Parity**: Both implementations tested automatically
4. **Deploy Rust Binary**: Ship the performance-optimized version

## 📁 Project Structure

```
ptd-python-cli/
├── .opencode/              # OpenCode AI configuration
│   ├── agent/             # AI agent definitions
│   └── command/           # Automation commands
├── src/
│   ├── basiccli/          # Python source tree
│   │   ├── cli.py         # Python entry point
│   │   ├── commands/
│   │   │   ├── *.py       # Python implementations
│   │   │   └── *.rs       # Rust versions (side-by-side)
│   │   └── utils/
│   │       ├── *.py       # Python utilities
│   │       └── *.rs       # Rust utilities (side-by-side)
│   ├── cli.rs             # Rust entry point
│   └── lib.rs             # Rust library exports
├── tests/                  # Test suites for both languages
│   ├── commands/
│   │   ├── test_*.py      # Python tests
│   │   └── test_*.rs      # Rust tests (side-by-side)
│   └── utils/
│       ├── test_*.py      # Python utility tests  
│       └── test_*.rs      # Rust utility tests (side-by-side)
├── bin/                    # Developer tools
│   ├── compile            # Build Rust binary
│   ├── test              # Run Rust tests
│   ├── pytest           # Run Python tests
│   └── lint              # Lint both languages
└── docs/                   # Documentation
```

## 🛠 Features

### Commands Included
- **hello** - Greeting with time-based messages
- **version** - Version info (text/JSON)
- **benchmark** - Performance testing suite
- **process** - JSON file processing

### Utilities
- **Logger** - Colored output, progress bars, timing
- **FileHandler** - JSON/YAML/CSV support, atomic writes

### Developer Tools
- `./bin/compile` - Build optimized Rust binary
- `./bin/test` - Run Rust test suite
- `./bin/pytest` - Run Python test suite
- `./bin/lint` - Auto-fix code style issues

## 💻 Real Developer Workflow

### Step 1: Write Your Python Code (Focus on Logic)
```python
# src/basiccli/commands/myfeature.py
from dataclasses import dataclass
from typing import Optional

from ..utils.database import Database
from ..utils.result import Result

@dataclass
class MyFeature:
    def execute(self, filter_option: Optional[str] = None) -> Result:
        # Write clean Python - OpenCode handles the rest
        database = Database()
        results = database.query(filter_option)
        print(self.format_output(results))
        return Result(success=True, message="Feature executed")
```

### Step 2: OpenCode Transpiles Automatically
```bash
# Start OpenCode session and run transpile
opencode
> /transpile

# OpenCode AI agent:
# ✓ Detects your Python changes via git
# ✓ Understands the business logic
# ✓ Generates idiomatic Rust code
# ✓ Maintains error handling patterns
# ✓ Creates equivalent tests
```

### Step 3: AI-Generated Rust (Optimized)
```rust
// src/commands/myfeature.rs (AI-generated)
use crate::utils::database::Database;
use crate::utils::result::Result as CliResult;
use anyhow::Result;

pub struct MyFeature;

impl MyFeature {
    pub fn execute(&self, filter: Option<&str>) -> Result<CliResult> {
        let db = Database::new()?;
        let results = db.query(filter)?;
        println!("{}", self.format_output(&results));
        Ok(CliResult::new(true, "Feature executed".to_string()))
    }
}
```

### Step 4: Verify & Deploy
```bash
# Tests pass for both implementations
./bin/pytest  # ✓ Python tests
./bin/test    # ✓ Rust tests

# Ship the fast version
./bin/compile
./bin/todocli-rust myfeature  # 250x faster startup!
```

## 📈 Real-World Impact: TodoCLI Case Study

### Proven Performance Gains (todo-list-example branch)

**Daily CLI Usage (100 operations)**:
- **Python Version**: 25 seconds total startup overhead
- **Rust Version**: 0.1 seconds total startup time
- **Net Benefit**: 24.9 seconds saved daily (99.6% improvement)

**Batch Processing (1000 database operations)**:
- **Python Implementation**: 4.2 minutes execution time
- **Rust Implementation**: 4 seconds execution time  
- **Net Benefit**: 4+ minutes saved per batch (98.4% improvement)

### Development Velocity Impact
- **Python Development Time**: 2 days for full TodoCLI implementation
- **Manual Rust Port Time**: Estimated 5-7 days for equivalent functionality
- **OpenCode Transpilation Time**: Automated in minutes
- **Total Time Saved**: 3-5 days of development effort

### OpenCode Agent Value Demonstration
- **🚀 Instant Transpilation**: No manual rewriting of business logic
- **🧪 Comprehensive Testing**: 69 tests generated automatically
- **🎯 Perfect Parity**: Identical functionality guaranteed across languages
- **⚡ Performance Optimization**: Best practices applied without manual effort

## 🎓 Learn More About OpenCode & PTD

### Essential Documentation
- [**OpenCode Guide**](opencode.md) - Complete guide to using OpenCode agents
- [**PTD Paradigm**](docs/base/ptd-paradigm.md) - Understanding polyglot development
- [**Getting Started**](docs/guides/getting-started.md) - Setup and first steps
- [**Performance Analysis**](docs/base/performance.md) - Real benchmarks

### OpenCode Agent Capabilities
- **python-dev Agent**: Writes clean Python following SOLID principles
- **rust-transpiler Agent**: Converts Python to optimized Rust
- **Semantic Understanding**: Preserves business logic, not just syntax
- **Test Generation**: Creates comprehensive test suites
- **Performance Optimization**: Applies Rust best practices automatically

### Try the TodoCLI Example
The **[todo-list-example branch](https://github.com/ai-ptd-dev/ptd-python-cli/tree/todo-list-example)** contains a complete todo list manager showing:
- Full CRUD operations with SQLite
- Priority management and filtering
- JSON export/import
- 69 auto-generated tests
- 250x performance improvement

## 🔧 Use This Boilerplate

1. **Fork this repository**
2. **Rename** BasicCli to your project name
3. **Add commands** following the pattern
4. **Write tests** for both Python and Rust
5. **Deploy** the Rust binary

### Customization Example

```bash
# Fork and rename
git clone https://github.com/yourusername/mycli
cd mycli

# Add your command
vim src/basiccli/commands/deploy.py
vim src/commands/deploy.rs

# Test both versions
./bin/pytest
./bin/test

# Ship it!
./bin/compile
cp target/release/mycli-rust /usr/local/bin/mycli
```

## 🤝 Contributing to PTD & OpenCode

### Ways to Contribute
1. **🔧 Framework Improvements**: Enhance the PTD boilerplate
2. **🤖 Agent Enhancement**: Improve transpilation quality and coverage
3. **📊 Benchmarking**: Add performance analysis and optimization
4. **📚 Documentation**: Expand PTD methodology and examples
5. **🌐 Language Support**: Extend Python→Rust transpilation or add other language pairs

### Contribution Guidelines
- Maintain functional parity between language implementations
- Include comprehensive test coverage for both languages
- Document AI agent decision patterns and optimizations
- Ensure performance benchmarks validate improvements

## 📄 License

MIT License - Use freely in your projects

## 🌟 Why BasicCli?

- **Best of Both Worlds**: Python's expressiveness, Rust's performance
- **Side-by-Side Code**: See Python and Rust implementations together
- **Production Ready**: Full test suites, linting, documentation
- **Real Performance**: Not theoretical - actual 50x startup improvement
- **Developer Friendly**: Helper scripts for common tasks

## 🚦 Status

- ✅ Python implementation complete
- ✅ Rust transpilation complete  
- ✅ Test suites passing
- ✅ Documentation complete
- ✅ Performance validated

## 🔗 Links

- [PTD Methodology](https://github.com/ai-ptd-dev)
- [Performance Report](docs/base/performance.md)
- [Getting Started Guide](docs/guides/getting-started.md)

---

**Ready to build fast CLIs?** Fork BasicCli and experience the PTD paradigm! 🚀
