.PHONY: create-practice remove-practice install test lint format type-check build clean upload-test check-missing-reqs ci

create-practice:
ifndef NAME
	$(error NAME if not defined)
endif
	mkdir -p $(NAME)
	cp PracticeMakefile $(NAME)/Makefile

remove-practice:
ifndef NAME
	$(error NAME if not defined)
endif
	rm -rf $(NAME)


PYTHON := python3
PIP := $(PYTHON) -m pip

install:
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

test:
	$(PYTHON) -m pytest tests/ -v --cov=mortgage_calc --cov-report=term-missing --cov-report=html

lint:
	$(PYTHON) -m ruff check src/ tests/
	$(PYTHON) -m ruff format --check src/ tests/

format:
	$(PYTHON) -m ruff format src/ tests/

type-check:
	$(PYTHON) -m mypy src/ tests/

build:
	$(PYTHON) -m build

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

upload-test:
	$(PYTHON) -m twine upload --repository testpypi dist/*

check-missing-reqs:
	@echo "Проверка импортов, отсутствующих в requirements.txt..."
	@find . -name "*.py" ! -path "*/venv/*" ! -path "*/env/*" ! -path "*/.tox/*" \
		-exec grep -hE '^[[:space:]]*(from|import)[[:space:]]+([a-zA-Z0-9_]+)' {} \; \
		| awk '{print $$2}' \
		| sed 's/[.,].*//' \
		| sort -u > /tmp/imported_modules.tmp
	@grep -v '^#' requirements.txt requirements-dev.txt 2>/dev/null \
		| sed 's/[=<>~!].*//' \
		| sort -u > /tmp/required_packages.tmp
	@{ echo "os sys re math decimal json argparse pathlib typing dataclasses"; } \
		| tr ' ' '\n' > /tmp/stdlib_modules.tmp
	@comm -23 /tmp/imported_modules.tmp /tmp/required_packages.tmp \
		| grep -v -F -f /tmp/stdlib_modules.tmp || true
	@rm -f /tmp/imported_modules.tmp /tmp/required_packages.tmp /tmp/stdlib_modules.tmp

ci: lint type-check test build

.DEFAULT_GOAL := install-dev