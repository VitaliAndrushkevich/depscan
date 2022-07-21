run:
	poetry run python depscan/main.py
install:
	poetry install
req:
	poetry export --format=requirements.txt > requirements.txt