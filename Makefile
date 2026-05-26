# --- Auto-detect OS ---
ifeq ($(OS),Windows_NT)
    PYTHON := .venv/Scripts/python
    PIP := .venv/Scripts/pip
else
    PYTHON := .venv/bin/python
    PIP := .venv/bin/pip
endif

# --- Targets ---
.PHONY: venv install run-app check-requirements typecheck

venv:
	python3 -m venv .venv
	$(PIP) install --upgrade pip

install:
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt

run-app:
	cd src && ../$(PYTHON) app.py

typecheck:
	cd src && ../$(PYTHON) -m mypy app.py

check-requirements:
	$(PYTHON) scripts/check_deps.py