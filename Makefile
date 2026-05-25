# --- Variables ---
PYTHON := .venv/bin/python
PIP := .venv/bin/pip

# --- Targets ---
.PHONY: venv run-app

venv:
	python3 -m venv .venv
	$(PIP) install --upgrade pip

run-app:
	$(PYTHON) src/app.py