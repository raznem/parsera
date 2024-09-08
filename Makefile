release:
	poetry publish --build

format:
	black .
	isort .

doc-deploy:
	mkdocs gh-deploy
