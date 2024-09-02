install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*whl

package-reinstall:
	pip install --forse-reinstall dist/*.whl

uninstall:
	python3 -m pip uninstall hexlet-code

lint:
	poetry run flake8 page_analyzer

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh