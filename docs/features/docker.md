## Running in Docker

You can get access to the CLI or development environment using Docker.

### Prerequisites

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

### Quickstart

1. Create a .env file in the project root directory with the following content:

```env
URL=https://parsera.org
FILE=/app/scheme.json
OUTPUT=/app/output/result.json
SCROLLS=5
```

2. Create `scheme.json` file with the parsing scheme in the repository root directory.

3. Run `make up` in this directory.

4. The output will be saved as `output/results.json` file.

### Docker Make Targets

```sh
make build # Build Docker image

make up # Start containers using Docker Compose

make down # Stop and remove containers using Docker Compose

make restart # Restart containers using Docker Compose

make logs # View logs of the containers

make shell # Open a shell in the running container

make clean # Remove all stopped containers, unused networks, and dangling images
```
