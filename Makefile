freeze:
	uv pip freeze > requirements.txt

mypy:
	mypy app/

lint:
	ruff check --fix app/

format:
	ruff format app/

isort:
	isort app/

all:
	mypy app/
	ruff check --fix app/
	ruff format app/
	isort app/
	uv pip freeze > requirements.txt

run:
	docker compose up new-app --build

new-migration:
	alembic revision --autogenerate -m "$(message)"

migrate:
	alembic upgrade head