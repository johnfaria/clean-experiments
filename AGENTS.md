# Clean Experiments - Agent Guidelines

## Build/Test Commands
- **Run all tests**: `task test` (pytest with PYTHONDONTWRITEBYTECODE=1)
- **Run single test**: `pytest path/to/test_file.py::TestClass::test_method`
- **Format code**: `task format` (ruff format)
- **Lint code**: `task lint` (ruff check)
- **Mypy type check**: `task typing` (mypy src)
- **Run dev server**: `task dev` (composition root)
- **Basedpyright type check** `task basedpyright` (basedpyright src)

## Code Style Guidelines
- **Python version**: >=3.13
- **Imports**: Core imports first, then third-party, then local (src.modules.*)
- **Docstrings**: Google style (see ruff config), with Args/Returns/Raises sections
- **Type hints**: Use proper typing, including TypedDict for structured data
- **Classes**: Use @dataclass(frozen=True) for value objects, dataclass for entities
- **Error handling**: Raise ValueError with descriptive messages for validation errors
- **Naming**: snake_case for functions/variables, PascalCase for classes, descriptive names
- **Structure**: Domain-driven design, modules/domain separation, value objects pattern
- **Tests**: Use pytest with class-based organization, descriptive test method names
- **Methods**: Use @override decorator when overriding parent methods
- **Commands vs Queries**: Separate command methods (modify state) from query methods (return values)

## Cursor/Copilot Rules
- No Cursor or Copilot rules present in this repository.
