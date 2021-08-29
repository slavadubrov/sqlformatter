#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON ?= python3.6
PIP = $(VENV)/bin/pip
VENV = $(PROJECT_DIR)/.venv
VIRTUALENV = $(PYTHON) -m venv

#################################################################################
# virtual environment and dependencies                                          #
#################################################################################

.PHONY: venv
## create virtual environment
venv: ./.venv/.requirements

.venv:
	$(VIRTUALENV) $(VENV)
	$(PIP) install -U pip setuptools wheel

.venv/.requirements: .venv
	$(PIP) install -r $(PROJECT_DIR)/requirements.txt
	$(PIP) install -r $(PROJECT_DIR)/requirements-dev.txt
	touch $(VENV)/.requirements

.PHONY: venv-clean
## clean virtual environment
venv-clean:
	rm -rf $(VENV)

.PHONY: compile-reqs
## compiles the requirements from requirements.in and updates the requirements.txt file accordingly
compile-reqs:
	$(VENV)/bin/pip-compile requirements.in
	$(VENV)/bin/pip-compile requirements-dev.in

#################################################################################
# code format / code style                                                      #
#################################################################################

.PHONY: format-code-check
## check compliance with code style (via 'black')
format-code-check: .venv/.requirements
	$(VENV)/bin/black --check $(PROJECT_DIR)/

.PHONY: format-code
## reformat code for compliance with code style (via 'black')
format-code: venv
	$(VENV)/bin/black $(PROJECT_DIR)/


#################################################################################
# Tests                                                                         #
#################################################################################

.PHONY: test
test: venv
## run pytest
	@PYTHONPATH=$(PYTHONPATH):$(PROJECT_DIR) $(VENV)/bin/pytest $(PROJECT_DIR)

.PHONY: lint
lint: venv
	@PYTHONPATH=$(PYTHONPATH):$(PROJECT_DIR) $(VENV)/bin/pylint --rcfile=setup.cfg $(PROJECT_DIR)/sqlformatter


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
