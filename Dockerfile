FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies needed for Playwright
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the poetry files and install dependencies
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root

# Install Playwright and the required browser binaries with dependencies
RUN poetry run playwright install --with-deps firefox

# Copy the rest of the application code
COPY . /app/

# Set the PYTHONPATH to the app directory
ENV PYTHONPATH=/app
ENV URL=https://parsera.org
ENV FILE=/app/scheme.json
ENV OUTPUT=/app/output/result.json

# Expose the output folder (where the result will be saved)
VOLUME /app/output

ENTRYPOINT ["poetry", "run", "python", "-m", "parsera.main"]
