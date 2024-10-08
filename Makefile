PORT ?= 8080

install:
	poetry install -n -v --no-root

build:
	./build.sh

dev:
	poetry run flask --app page_analyzer:app run

lint:
	poetry run flake8 page_analyzer

start:
	poetry run gunicorn -b 0.0.0.0:$(PORT) page_analyzer:app
