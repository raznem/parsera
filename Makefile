release:
	poetry publish --build

format:
	black .
	isort .

doc-deploy:
	mkdocs gh-deploy

doc-run:
	mkdocs serve

# Define variables
IMAGE_NAME = parsera
CONTAINER_NAME = parsera
DOCKER_COMPOSE_FILE = docker-compose.yaml

# Targets
.PHONY: build up down restart logs shell

# Build Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Start containers using Docker Compose
up:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up --build -d

# Stop and remove containers using Docker Compose
down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

# Restart containers using Docker Compose
restart: down up

# View logs of the containers
logs:
	docker-compose -f $(DOCKER_COMPOSE_FILE) logs -f

# Open a shell in the running container
shell:
	docker exec -it $(CONTAINER_NAME) /bin/sh

# Remove all stopped containers, unused networks, and dangling images
clean:
	docker system prune -f