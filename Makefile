PORT ?= 5000

install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 page_analyzer

start:
	poetry run gunicorn -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh