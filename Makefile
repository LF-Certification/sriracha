.PHONY: setup test lint

envsetup: .venv/initialized

.venv/initialized:
	python3 -m venv .venv
	./.venv/bin/pip install -e .
	./.venv/bin/pip install -r requirements-dev.txt
	touch .venv/initialized

functional-tests:
	behave

pre-commit-install:
	pre-commit install

lint: envsetup
	@# Tee-ing to .pre-commit.out allows the CI pipeline to extract
	@# any relevant error messages and post to a github PR.
	bash -eo pipefail -c ". ./.venv/bin/activate &&  pre-commit run --files ./scripts/*.* ./* | tee .pre-commit.out"

test: envsetup
	@# Tee-ing to .pre-commit.out allows the CI pipeline to extract
	@# any relevant error messages and post to a github PR.
	bash -eo pipefail -c "./.venv/bin/python3 -m pytest"
