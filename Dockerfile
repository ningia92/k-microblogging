# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:0.13.9-python3.14-trixie-slim

WORKDIR /app

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering
ENV PYTHONUNBUFFERED=1

# Omit development dependencies
ENV UV_NO_DEV=1

# Leverage layer caching since these files rarely change
COPY pyproject.toml uv.lock ./

# Install the project's dependencies using the lockfile
RUN uv sync --locked

# Then, add the rest of the project source code (changes frequently)
# Copying separately from its dependencies allows optimal layer caching
COPY . /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]