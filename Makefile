install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=main --cov=src test_*.py

format:
	black *.py src/*.py

lint:
	pylint --disable=R,C --ignore-patterns=test_.*?py *.py src/*.py

container-lint:
	docker run --rm -i hadolint/hadolint < .devcontainer/Dockerfile

refactor: format lint

build:
	docker build -f .devcontainer/Dockerfile -t linkedin-scraper .

# Pass date args: make scrape ARGS="--start-date 2026-02-17 --end-date 2026-02-23"
scrape:
	python main.py scrape $(ARGS)

report:
	python main.py report

deploy:
	#deploy goes here

all: install lint test format deploy
