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
