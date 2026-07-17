#!/usr/bin/env python3
import os
import argparse
import fnmatch
from pathlib import Path

# Список папок, которые мы игнорируем по умолчанию
EXCLUDE_DIRS = {
    '.git', 'Pods', '.build', 'DerivedData',
    'build', 'tests', 'Fastlane', '.xcodeproj', '.xcworkspace'
}


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


def get_tree(path, root_path, exclude_patterns, prefix=""):
    """Рекурсивно строит текстовое дерево проекта."""
    tree = ""
    paths = sorted(list(path.iterdir()), key=lambda x: (x.is_file(), x.name))

    # Отфильтровываем дефолтные и пользовательские исключения
    filtered = []
    for p in paths:
        if p.name in EXCLUDE_DIRS:
            continue
        rel = p.relative_to(root_path)
        if is_excluded(rel, exclude_patterns):
            continue
        filtered.append(p)

    # Заранее считаем поддеревья для папок, чтобы скрыть пустые (после фильтрации) директории
    entries = []
    for p in filtered:
        if p.is_dir():
            new_prefix_placeholder = ""  # посчитаем позже с правильным prefix
            subtree = get_tree(p, root_path, exclude_patterns, "")
            if subtree.strip():
                entries.append((p, subtree))
        elif p.suffix == ".swift":
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

    with open(output_file, 'w', encoding='utf-8') as out:
        # 1. Пишем заголовок и дерево файлов
        out.write("PROJECT STRUCTURE:\n")
        out.write("================================================\n")
        out.write(f"Root: {root_path.name}\n")
        out.write(get_tree(root_path, root_path, exclude_patterns))
        out.write("================================================\n\n")

        # 2. Собираем содержимое файлов
        for path in root_path.rglob("*.swift"):
            # Проверка дефолтных исключенных папок
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue

            relative_path = path.relative_to(root_path)

            # Проверка пользовательских исключений
            if is_excluded(relative_path, exclude_patterns):
                continue

            out.write(f"\n\n--- FILE START: {relative_path} ---\n")
            out.write("```swift\n")
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
