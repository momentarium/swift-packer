#!/usr/bin/env python3
import os
import argparse
import fnmatch
from pathlib import Path

# Список папок, которые мы игнорируем по умолчанию
EXCLUDE_DIRS = {
    '.git', 'Pods', '.build', 'DerivedData',
    'build', 'tests', 'Fastlane',
    'xcuserdata', 'xcschemes', 'xcuserdatad'
}


def should_exclude_dir(dir_name: str) -> bool:
    """
    Проверяет, должна ли папка быть исключена по умолчанию.
    Проверяет как точное совпадение, так и суффиксы (.xcodeproj, .xcworkspace, .xcassets).
    """
    # Точное совпадение или в списке
    if dir_name in EXCLUDE_DIRS:
        return True
    
    # Проверка суффиксов для Xcode-специфичных папок
    if dir_name.endswith('.xcodeproj') or dir_name.endswith('.xcworkspace') or dir_name.endswith('.xcassets'):
        return True
    
    return False


def is_excluded(rel_path: Path, patterns) -> bool:
    """
    Проверяет, должен ли файл/папка быть исключен.
    rel_path - путь относительно корня проекта.
    patterns - список пользовательских glob-шаблонов (например "*.generated.swift", "Views/*", "Mocks").
    """
    if not patterns:
        return False

    rel_str = rel_path.as_posix()
    name = rel_path.name

    for pattern in patterns:
        # Сравнение с полным относительным путем (поддержка "Views/*.swift", "Sources/**")
        if fnmatch.fnmatch(rel_str, pattern):
            return True
        # Сравнение с именем файла/папки (поддержка "*.generated.swift", "Mocks")
        if fnmatch.fnmatch(name, pattern):
            return True
        # Сравнение с каждой частью пути (чтобы "Mocks" исключал Mocks/ на любом уровне)
        if any(fnmatch.fnmatch(part, pattern) for part in rel_path.parts):
            return True

    return False


SUPPORTED_EXTENSIONS = {
    '.swift', '.strings', '.xcstrings', '.plist', '.json', '.yaml', '.yml', '.xml',
    '.h', '.m', '.mm', '.c', '.cpp', '.hpp', '.cc', '.cxx', '.kt', '.java', '.rb', '.py', '.sh',
    '.metal'
}

# Маппинг расширений файлов на языки для подсветки синтаксиса
LANGUAGE_MAP = {
    '.swift': 'swift',
    '.metal': 'metal',
    '.json': 'json',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.xml': 'xml',
    '.plist': 'xml',
    '.py': 'python',
    '.sh': 'bash',
    '.rb': 'ruby',
    '.java': 'java',
    '.kt': 'kotlin',
    '.c': 'c',
    '.h': 'c',
    '.cpp': 'cpp',
    '.cc': 'cpp',
    '.cxx': 'cpp',
    '.mm': 'objc',
    '.m': 'objc',
    '.hpp': 'cpp',
}


def get_language(path: Path) -> str:
    """Определяет язык программирования для подсветки синтаксиса файла."""
    return LANGUAGE_MAP.get(path.suffix.lower(), 'text')


def is_bundle_file(path: Path) -> bool:
    """Определяет, является ли файл подходящим для включения в bundle."""
    if not path.is_file():
        return False

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False

    try:
        with path.open('rb') as handle:
            chunk = handle.read(1024)
    except OSError:
        return False

    return b'\x00' not in chunk


def get_tree(path, root_path, exclude_patterns, prefix=""):
    """Рекурсивно строит текстовое дерево проекта."""
    tree = ""
    paths = sorted(list(path.iterdir()), key=lambda x: (x.is_file(), x.name))

    # Отфильтровываем дефолтные и пользовательские исключения
    filtered = []
    for p in paths:
        if should_exclude_dir(p.name):
            continue
        rel = p.relative_to(root_path)
        if is_excluded(rel, exclude_patterns):
            continue
        filtered.append(p)

    # Заранее считаем поддеревья для папок, чтобы скрыть пустые (после фильтрации) директории
    entries = []
    for p in filtered:
        if p.is_dir():
            subtree = get_tree(p, root_path, exclude_patterns, "")
            if subtree.strip():
                entries.append((p, subtree))
        elif p.is_file() and is_bundle_file(p):
            entries.append((p, None))

    for i, (p, _) in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "

        if p.is_dir():
            tree += f"{prefix}{connector}{p.name}/\n"
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree += get_tree(p, root_path, exclude_patterns, new_prefix)
        else:
            tree += f"{prefix}{connector}{p.name}\n"

    return tree


def pack_project(input_dir, output_file, exclude_patterns):
    root_path = Path(input_dir).resolve()
    output_path = Path(output_file)
    if not output_path.is_absolute():
        output_path = (root_path / output_path).resolve()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as out:
        # 1. Пишем заголовок и дерево файлов
        out.write("PROJECT STRUCTURE:\n")
        out.write("================================================\n")
        out.write(f"Root: {root_path.name}\n")
        out.write(get_tree(root_path, root_path, exclude_patterns))
        out.write("================================================\n\n")

        # 2. Собираем содержимое файлов
        for path in root_path.rglob("*"):
            if not path.is_file():
                continue

            # Проверка дефолтных исключенных папок
            if any(should_exclude_dir(part) for part in path.parts):
                continue

            relative_path = path.relative_to(root_path)

            # Проверка пользовательских исключений
            if is_excluded(relative_path, exclude_patterns):
                continue

            if not is_bundle_file(path):
                continue

            out.write(f"\n\n--- FILE START: {relative_path} ---\n")
            language = get_language(path)
            out.write(f"```{language}\n")
            try:
                out.write(path.read_text(encoding='utf-8'))
            except Exception as e:
                out.write(f"// Error reading file: {e}")
            out.write("\n```\n")
            out.write(f"--- FILE END: {relative_path} ---\n")

    print(f"✅ Готово! Весь код собран в: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pack Swift project into a single text file for LLM")
    parser.add_argument("input", help="Путь к папке проекта", default=".", nargs="?")
    parser.add_argument("-o", "--output", help="Имя выходного файла", default="project_bundle.txt")
    parser.add_argument(
        "-e", "--exclude",
        help="Шаблоны (glob) для исключения файлов/папок из результата. "
             "Можно указать несколько через пробел. "
             "Примеры: -e Mocks '*.generated.swift' 'Views/Legacy/*'",
        nargs="+",
        default=[]
    )
    args = parser.parse_args()
    pack_project(args.input, args.output, args.exclude)
