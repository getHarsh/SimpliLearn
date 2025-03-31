# Code Setup and Development Guidelines

## Project Structure

The project follows a modular structure for maintainability and testability:

### Core Components

- `main.py`: Entry point and CLI interface
- `models.py`: Data models and business logic
- `tests/`: Test suite directory

### Support Files

- `run.py`: Build system and environment setup
- `requirements.txt`: Python dependencies
- `docs/`: Documentation directory

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for all classes and methods
- Keep functions focused and single-purpose

### Error Handling

- Use appropriate exception types
- Provide clear error messages
- Handle all edge cases
- Log errors appropriately

### Testing

- Write unit tests for all functionality
- Include edge cases and error conditions
- Maintain high test coverage
- Use pytest for testing

### Documentation

- Keep documentation up to date
- Include examples in docstrings
- Document all public interfaces
- Add comments for complex logic

## Build System

The `run.py` script provides several features:

- Environment setup
- Dependency management
- Test execution
- Clean builds

Use the appropriate flags when running:

```bash
./run.py --test        # Run tests
./run.py --deepbuild   # Clean build
```
