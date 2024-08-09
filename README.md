# fastapi-template
Python FastAPI template repo

## Prerequisites

- Python 3.12
- uv (Python package manager)

## Setup

1. Create and activate a virtual environment:

```bash
uv venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
uv pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following environment variables:

```bash
EXAMPLE1=<value>
EXAMPLE2=<value>
```

## Development

This project uses several tools for development:

- `mypy` for static type checking
- `ruff` for linting
- `isort` for import sorting

You can run these tools using the following make commands:
make mypy
make lint
make isort

### To add a dependency

```bash
uv pip install <dependency>
```

and freeze it with (it's like a lock file):

```bash
make freeze
```

### Run it!

For local dev it's better to use `docker compose` to run the app.

First terminal:
```bash
docker compose up --build
```

## API Endpoints

Get the docs at `http://localhost:8000/docs#/`