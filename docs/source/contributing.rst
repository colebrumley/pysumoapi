Contributing
============

We welcome contributions to pysumoapi! This document provides guidelines and instructions for contributing to the project.

Development Setup
----------------

1. Fork the repository
2. Clone your fork:

.. code-block:: bash

    git clone https://github.com/your-username/pysumoapi.git
    cd pysumoapi

3. Install development dependencies:

.. code-block:: bash

    uv pip install -e ".[dev]"

4. Install pre-commit hooks:

.. code-block:: bash

    pre-commit install

Code Style
----------

pysumoapi follows these code style guidelines:

- Use Black for code formatting
- Use Ruff for linting
- Use MyPy for type checking
- Follow Google-style docstrings

Run the following commands to ensure your code meets these standards:

.. code-block:: bash

    # Format code
    black .

    # Run linter
    ruff check .

    # Run type checker
    mypy .

Testing
-------

All code changes should include tests. The project uses pytest for testing:

.. code-block:: bash

    # Run all tests
    pytest

    # Run tests with coverage
    pytest --cov=pysumoapi

    # Run specific test file
    pytest tests/test_client.py

Pull Request Process
-------------------

1. Create a new branch for your feature/fix:

.. code-block:: bash

    git checkout -b feature/your-feature-name

2. Make your changes and commit them:

.. code-block:: bash

    git commit -m "Description of your changes"

3. Push to your fork:

.. code-block:: bash

    git push origin feature/your-feature-name

4. Create a pull request to the main repository

Documentation
------------

When adding new features or making changes:

1. Update the relevant documentation in the ``docs/source`` directory
2. Add or update docstrings in the code
3. Include examples if applicable

Release Process
--------------

1. Update version in ``pyproject.toml``
2. Update ``CHANGELOG.md``
3. Create a new release on GitHub
4. The release will trigger the CI/CD pipeline to publish to PyPI

Questions?
----------

If you have any questions, feel free to:

- Open an issue on GitHub
- Join our community chat
- Contact the maintainers directly 