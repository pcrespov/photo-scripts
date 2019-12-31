VERSION:=$(shell date +0.0.%Y%m%d-%H%M%S)


# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help clean

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

.venv: 
	@python3 -m venv $@

.PHONY: devenv
devenv: .venv ##  Creates python virtual environment
	@.venv/bin/pip install --upgrade pip wheel setuptools
	@.venv/bin/pip install -r requirements.txt

.PHONY: clean
clean: 
	@rm -rf .venv
