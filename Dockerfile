FROM python:3.13-slim

ARG BUILD_VERSION=1.0.0
ENV APP_NAME="RealEstate"

RUN pip install uv

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*


# Create non-root user first
RUN adduser --disabled-password --gecos '' appuser

RUN mkdir /app && chown appuser:appuser /app
WORKDIR /app/

# Switch to non-root user for file operations
USER appuser

COPY --chown=appuser:appuser pyproject.toml uv.lock /app/


RUN uv sync --frozen
COPY --chown=appuser:appuser . /app/

EXPOSE 8000

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]