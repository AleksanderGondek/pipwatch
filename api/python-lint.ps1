.\.virtualenv\Scripts\pycodestyle.exe pipwatch_api
.\.virtualenv\Scripts\pylint.exe pipwatch_api --rcfile=pylintrc
.\.virtualenv\Scripts\flake8.exe pipwatch_api
.\.virtualenv\Scripts\mypy.exe --ignore-missing-imports pipwatch_api
