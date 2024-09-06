release:
	poetry publish --build

format:
	black .
	isort .