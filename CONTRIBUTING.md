Contributing
============

Thanks for your interest in improving tti! This project now uses a modern Python packaging setup, pre-commit hooks, and CI checks.

Developer setup
---------------

- Create and activate a virtual environment (recommended).
- Install the project in editable mode with dev tools:
```shell
pip install -e '.[dev]'
```

- Install pre-commit hooks:

```shell
pre-commit install
```

- Run the test suite locally:
```shell
pytest -q
```
- Run linters/formatters locally:
```shell
ruff check .
ruff format .
```

Packaging and release
---------------------

This project is configured with a PEP 621-compatible `pyproject.toml` using setuptools as the build backend. To build distributions:

- Ensure the version in `pyproject.toml` is updated and in sync with the `README` file.
- Build the package:
```shell
python -m pip install --upgrade build twine
python -m build
```

- Optionally upload to PyPI (requires credentials):
```shell
twine upload dist/*
```
