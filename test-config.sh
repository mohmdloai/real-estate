#!/bin/bash

echo "Testing pyproject.toml syntax..."
python -c "import tomllib; tomllib.loads(open('pyproject.toml', 'rb').read())" && echo "pyproject.toml is valid"

echo "Installing pre-commit hooks..."
pre-commit install

echo "Running pre-commit on all files..."
pre-commit run --all-files

echo "Testing flake8..."
flake8 --version && flake8 . --count
