FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1

COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /uvx /bin/

# create /app and cd into it (like cd backend)
WORKDIR /app 

ENV PATH="/app/.venv/bin:$PATH"

# copy backend/pyproject.toml → /app/pyproject.toml
COPY pyproject.toml uv.lock ./

# creates /app/.venv INSIDE the image
RUN uv sync --frozen --no-dev

# copy backend/app/ → /app/app/
COPY app/ ./app/

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
