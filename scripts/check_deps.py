"""Проверка, что все импорты из src/ и tests/ покрыты requirements."""

import ast
import sys
from pathlib import Path

# Маппинг import -> package (неоднозначные случаи)
IMPORT_TO_PACKAGE = {
    "sklearn": "scikit-learn",
    "PIL": "pillow",
    "yaml": "pyyaml",
}


def extract_imports(src_dir: Path) -> set[str]:
    """Извлечь все top-level импорты из .py файлов."""
    imports = set()
    for py_file in src_dir.rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
    return imports


def read_requirements(req_file: Path) -> set[str]:
    """Прочитать пакеты из requirements.txt."""
    packages = set()
    if not req_file.exists():
        return packages
    for line in req_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Отрезаем версии: numpy>=1.0 -> numpy
        pkg = line.split("=")[0].split("<")[0].split(">")[0].split("!")[0].strip()
        packages.add(pkg)
    return packages


def main() -> int:
    src_dir = Path("src")
    tests_dir = Path("tests")
    req_file = Path("requirements.txt")
    req_dev_file = Path("requirements-dev.txt")

    imports = extract_imports(src_dir) | extract_imports(tests_dir)
    req_packages = read_requirements(req_file) | read_requirements(req_dev_file)

    # Стандартная библиотека + встроенные модули
    stdlib = {
        "abc", "argparse", "ast", "asyncio", "base64", "collections", "copy",
        "csv", "dataclasses", "datetime", "decimal", "enum", "functools",
        "glob", "hashlib", "http", "importlib", "inspect", "io", "itertools",
        "json", "logging", "math", "operator", "os", "pathlib", "pickle",
        "random", "re", "shutil", "socket", "sqlite3", "statistics", "string",
        "subprocess", "sys", "tempfile", "textwrap", "threading", "time",
        "traceback", "typing", "unittest", "urllib", "uuid", "warnings",
        "xml", "zipfile",
    }

    # Игнорируем локальные модули проекта
    local_modules = {f.stem for f in src_dir.glob("*.py")}
    local_modules.add("src")
    imports -= local_modules

    missing = set()
    for imp in imports:
        if imp in stdlib:
            continue
        mapped = IMPORT_TO_PACKAGE.get(imp, imp)
        if mapped not in req_packages:
            missing.add(imp)

    if missing:
        print("MISSING in requirements:", ", ".join(sorted(missing)))
        return 1

    print("OK: all imports covered")
    return 0


if __name__ == "__main__":
    sys.exit(main())