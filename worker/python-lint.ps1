.\.virtualenv\Scripts\pep8.exe pipwatch_worker
.\.virtualenv\Scripts\pylint.exe pipwatch_worker --rcfile=pylintrc
.\.virtualenv\Scripts\flake8.exe pipwatch_worker
.\.virtualenv\Scripts\mypy.exe --ignore-missing-imports pipwatch_worker
