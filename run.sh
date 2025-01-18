#!/usr/bin/env sh
#
# Build and run the example Docker image.
#
# Mounts the local project directory to reflect a common development workflow.
#
# The `docker run` command uses the following options:
#
#   --rm                        Remove the container after exiting
#   --volume .:/app             Mount the current directory to `/app` so code changes don't require an image rebuild
#   --volume /app/.venv         Mount the virtual environment separately, so the developer's environment doesn't end up in the container
#   --publish 8000:8000         Expose the web server port 8000 to the host
#   -it $(docker build -q .)    Build the image, then use it as a run target
#   $@                          Pass any arguments to the container

if [ -t 1 ]; then
    INTERACTIVE="-it"
else
    INTERACTIVE=""
fi

# Build the Docker image and get its ID
IMAGE_ID=$(docker build -q .)

if [ "$1" = "-test" ]; then
    # Start the container in the background
    CONTAINER_ID=$(docker run \
        --rm \
        --volume .:/app \
        --volume /app/.venv \
        --publish 8000:8000 \
        --detach \
        "$IMAGE_ID" \
        fastapi dev --host 0.0.0.0 app/main.py)

    # Wait for the API to initialize
    echo "Waiting for the API to initialize..."

    # Run tests
    echo "Running tests..."
    docker exec -it "$CONTAINER_ID" uv run pytest tests/

    # Stop the container after tests complete
    docker stop "$CONTAINER_ID"
else
    # Run the container normally, showing the logs for the FastAPI service
    docker run \
        --rm \
        --volume .:/app \
        --volume /app/.venv \
        --publish 8000:8000 \
        $INTERACTIVE \
        "$IMAGE_ID" \
        fastapi dev --host 0.0.0.0 app/main.py
fi