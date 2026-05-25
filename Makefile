# --- Variables ---
ifeq ($(OS),Windows_NT)
    PYTHON := .venv/Scripts/python.exe
    PIP := $(PYTHON) -m pip
else
    PYTHON := .venv/bin/python
    PIP := $(PYTHON) -m pip
endif

# --- Targets ---
.PHONY: venv install run-app check-requirements

venv:
	python -m venv .venv
	$(PIP) install --upgrade pip

install:
	$(PIP) install -r requirements.txt

run-app:
	$(PYTHON) src/app.py

check-requirements:
	$(PYTHON) scripts/check_deps.py