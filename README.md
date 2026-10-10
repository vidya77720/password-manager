# Password Generator Project

A secure and customizable password generator built with Python. Perfect for beginners to learn about random number generation, string manipulation, and command-line interfaces.

## Features

- Generate secure random passwords
- Customizable password length
- Include/exclude character types (uppercase, lowercase, digits, symbols)
- Generate multiple passwords at once
- Exclude similar characters (i, l, 1, L, o, 0, O) for better readability
- Password strength checker
- **Password history tracking with timestamps**
- **History statistics and analysis**
- **Export history to JSON/CSV formats**
- **Professional logging system for debugging and monitoring**
- **Configuration management for user preferences**
- **Graphical user interface (GUI) for easy usage**
- Easy-to-use command-line interface
- Beginner-friendly code structure

## Project Structure

```
password-generator/
├── password_generator.py    # Main password generator class
├── password_history.py      # Password history management system
├── config_manager.py        # Configuration management system
├── web_app.py               # Flask web application (Ready for Cloud Deployment)
├── templates/
│   └── index.html           # Modern responsive web UI
├── cli.py                   # Command-line interface
├── gui_app.py               # Tkinter graphical user interface
├── requirements.txt         # Python dependencies
├── Procfile                 # Deployment process command
├── render.yaml              # 1-Click Render blueprint
└── README.md                # Documentation
```

## Installation & Running

```bash
pip install -r requirements.txt
```

### Running the Web App (Browser Interface)
```bash
python web_app.py
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

### Deploying to Render
1. Push this repository to GitHub.
2. Sign in to [Render](https://render.com) and click **New + > Web Service**.
3. Select your GitHub repository.
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `gunicorn web_app:app`
6. Click **Deploy Web Service** — your live link is ready!

## Other Usage Options

### As a Python Module

```python
from password_generator import PasswordGenerator

# Create generator instance
generator = PasswordGenerator()

# Generate a simple password
password = generator.generate(length=12)
print(f"Password: {password}")

# Generate with custom options
password = generator.generate(
    length=16,
    use_uppercase=True,
    use_lowercase=True,
    use_digits=True,
    use_symbols=True,
    exclude_similar=True
)
print(f"Custom Password: {password}")

# Generate multiple passwords
passwords = generator.generate_multiple(count=5, length=14)
for i, pwd in enumerate(passwords, 1):
    print(f"{i}. {pwd}")

# Check password strength
strength = generator.check_strength("MyP@ssw0rd")
print(f"Strength: {strength['strength']}")
print(f"Score: {strength['score']}/{strength['max_score']}")
```

### Command Line Interface

Basic usage:
```bash
python cli.py
```

Generate a 16-character password:
```bash
python cli.py -l 16
```

Generate 5 passwords with 14 characters each:
```bash
python cli.py -c 5 -l 14
```

Generate without special symbols:
```bash
python cli.py -l 20 --no-symbols
```

Exclude similar characters:
```bash
python cli.py --exclude-similar
```

Check password strength:
```bash
python cli.py --check "MyP@ssw0rd"
```

Show help:
```bash
python cli.py --help
```

### Command Line Options

- `-l, --length`: Password length (default: 12, minimum: 4)
- `-c, --count`: Number of passwords to generate (default: 1)
- `--no-uppercase`: Exclude uppercase letters
- `--no-lowercase`: Exclude lowercase letters
- `--no-digits`: Exclude digits
- `--no-symbols`: Exclude special symbols
- `--exclude-similar`: Exclude similar characters (i, l, 1, L, o, 0, O)
- `--check`: Check strength of an existing password
- `--history`: Show password generation history
- `--history-limit N`: Limit history entries to show (default: 10)
- `--history-stats`: Show password generation statistics
- `--clear-history`: Clear all password history
- `--export-history FILE`: Export history to file (JSON or CSV)
- `--no-history`: Disable history logging for this session

## Examples

Run the example script to see various use cases:
```bash
python example_usage.py
```

### Password History Examples

View password generation history:
```bash
python cli.py --history
```

View last 5 passwords:
```bash
python cli.py --history --history-limit 5
```

Show generation statistics:
```bash
python cli.py --history-stats
```

Export history to JSON file:
```bash
python cli.py --export-history backup.json
```

Export history to CSV file:
```bash
python cli.py --export-history backup.csv
```

Clear all history:
```bash
python cli.py --clear-history
```

Generate password without saving to history:
```bash
python cli.py --no-history -l 16
```

### Graphical User Interface

Launch the GUI application:
```bash
python gui_app.py
```

**GUI Features:**
- Interactive password generation with click buttons
- Visual character type selection with checkboxes
- Real-time password strength indicator
- Copy to clipboard functionality
- Recent passwords history display
- User-friendly interface for beginners

### Configuration Management

View current configuration:
```python
from config_manager import ConfigManager
config = ConfigManager()
print(config.get_all())
```

Modify configuration:
```python
config.set("default_length", 16)
config.set("use_symbols", False)
```

Reset to defaults:
```python
config.reset_to_defaults()
```

### Professional Logging

The application includes comprehensive logging:
- All operations are logged to `password_generator.log`
- Includes timestamps, log levels, and detailed messages
- Useful for debugging and monitoring
- File-based and console logging

## Code Explanation

### PasswordGenerator Class

The main class that handles password generation:

- `__init__()`: Initializes character sets, history management, and configuration
- `generate()`: Generates a single password with customizable options (supports config defaults)
- `generate_multiple()`: Generates multiple passwords at once
- `check_strength()`: Analyzes password strength and provides feedback
- `get_history()`: Retrieves password generation history
- `get_recent_passwords()`: Gets most recently generated passwords
- `get_history_statistics()`: Returns generation statistics
- `clear_history()`: Clears all password history
- `export_history()`: Exports history to JSON or CSV file
- `get_history_count()`: Returns total number of history entries

### PasswordHistory Class

Manages password generation history with file-based persistence:

- `add_password()`: Logs a password with timestamp and metadata
- `get_history()`: Retrieves password history entries
- `get_recent_passwords()`: Gets recent passwords as strings
- `search_history()`: Searches history by pattern
- `get_statistics()`: Calculates generation statistics
- `clear_history()`: Clears all history entries
- `export_history()`: Exports history to file
- `delete_entry()`: Deletes specific history entry

### ConfigManager Class

Manages user preferences and application configuration:

- `__init__()`: Initializes configuration with defaults
- `get()`: Retrieves specific configuration value
- `set()`: Updates configuration value
- `get_all()`: Returns all configuration values
- `reset_to_defaults()`: Resets configuration to defaults
- `validate_config()`: Validates configuration values
- `export_config()`: Exports configuration to file
- `import_config()`: Imports configuration from file

### PasswordGeneratorGUI Class

Provides graphical user interface using Tkinter:

- `__init__()`: Initializes GUI and components
- `create_widgets()`: Creates all interface elements
- `generate_password()`: Handles password generation
- `copy_to_clipboard()`: Copies password to clipboard
- `refresh_history()`: Updates history display
- `clear_history()`: Clears password history

### Key Concepts Used

1. **Random Number Generation**: Uses `random` module for secure random selection
2. **String Manipulation**: Uses `string` module for character sets
3. **Type Hints**: Uses Python type hints for better code clarity
4. **Error Handling**: Includes proper error handling for invalid inputs
5. **Command-line Parsing**: Uses `argparse` for CLI interface
6. **File I/O Operations**: JSON file handling for history persistence
7. **DateTime Management**: Timestamp tracking for password generation
8. **Data Persistence**: History management with file-based storage
9. **Professional Logging**: Structured logging with multiple handlers
10. **Configuration Management**: JSON-based user preferences system
11. **GUI Development**: Tkinter-based graphical interface
12. **Event-Driven Programming**: GUI event handling and callbacks

## Beginner Learning Points

This project is great for learning:
- Python classes and object-oriented programming
- String manipulation and character sets
- Random number generation
- Command-line argument parsing
- Error handling
- Type hints
- Code documentation
- File I/O operations and JSON handling
- Data persistence and storage
- DateTime manipulation
- Statistics and data analysis
- Professional logging and debugging
- Configuration management
- GUI development with Tkinter
- Event-driven programming
- User experience design

## Security Notes

- This generator uses Python's `random` module which is suitable for general use
- For high-security applications, consider using `secrets` module instead
- Never store generated passwords in plain text
- Always use unique passwords for different accounts

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to modify and improve this project for your learning!

## Author

Created as a beginner-friendly Python project for learning purposes.
