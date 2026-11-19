# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:0.13.9-python3.14-trixie-slim

WORKDIR /app

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering
ENV PYTHONUNBUFFERED=1

# Omit development dependencies
ENV UV_NO_DEV=1

# Keep the virtual environment outside /app, so a bind mount of the
# project directory doesn't hide it
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

# Leverage layer caching since these files rarely change
COPY pyproject.toml uv.lock ./

# Install the project's dependencies using the lockfile
RUN uv sync --locked

# Then, add the rest of the project source code (changes frequently)
# Copying separately from its dependencies allows optimal layer caching
COPY . .

# Place executables in the environment at the front of the path
ENV PATH="/opt/venv/bin:$PATH"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]