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

# Source the virtual environment if it exists
if [ -d .venv ]; then
    . .venv/bin/activate
fi

# Copy the .env file to the root directory from the example file if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
fi

# Build the Docker image and get its ID
IMAGE_ID=$(docker build -q .)

# Check the argument provided
if [ "$1" = "-test" ]; then
    # Run the tests locally without starting the container
    echo "Running tests..."
    pytest tests/
else
    # Run the container, showing the logs for the FastAPI service
    echo "Starting the FastAPI service..."
    docker run \
        --rm \
        --volume .:/app \
        --volume /app/.venv \
        --publish 8000:8000 \
        $INTERACTIVE \
        "$IMAGE_ID"
fi
