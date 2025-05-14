# German Verb Quiz - Dev Guide

## Run Commands
- Run quiz: `python german_verb_quiz.py`
- Run with linting: `python -m pylint german_verb_quiz.py`
- Run with type checking: `python -m mypy german_verb_quiz.py`
- Run test: `python -m unittest discover tests`

## Code Style Guidelines
- **Imports**: Standard library first, then third-party, then local modules; alphabetically within each group
- **Formatting**: 4-space indentation, max 100 characters per line
- **Types**: Use docstrings for type hints, consider adding proper type annotations
- **Naming**:
  - Classes: CamelCase (e.g., `GermanVerbQuiz`)
  - Methods/Functions: snake_case (e.g., `load_verbs`, `get_random_verb`)
  - Variables: snake_case (e.g., `questions_attempted`, `correct_answers`)
- **Documentation**: All classes and methods should have docstrings
- **Error Handling**: Use try/except for user input and file operations
- **File Organization**: Keep CSV data files separate from Python code
- **Comments**: Explain "why" not "what" in comments, use them sparingly

This project is a German verb conjugation learning tool that loads verb forms from a CSV file and quizzes users on conjugations across different tenses and subjects.