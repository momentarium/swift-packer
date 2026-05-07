import os
import argparse
from pathlib import Path

# Список папок, которые мы игнорируем
EXCLUDE_DIRS = {
    '.git', 'Pods', '.build', 'DerivedData', 
    'build', 'tests', 'Fastlane', '.xcodeproj', '.xcworkspace'
}

def get_tree(path, prefix=""):
    """Рекурсивно строит текстовое дерево проекта."""
    tree = ""
    paths = sorted(list(path.iterdir()), key=lambda x: (x.is_file(), x.name))
    
    for i, p in enumerate(paths):
        if p.name in EXCLUDE_DIRS:
            continue
        
        is_last = i == len(paths) - 1
        connector = "└── " if is_last else "├── "
        
        if p.is_dir():
            tree += f"{prefix}{connector}{p.name}/\n"
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree += get_tree(p, new_prefix)
        elif p.suffix == ".swift":
            tree += f"{prefix}{connector}{p.name}\n"
            
    return tree

def pack_project(input_dir, output_file):
    root_path = Path(input_dir).resolve()
    
    with open(output_file, 'w', encoding='utf-8') as out:
        # 1. Пишем заголовок и дерево файлов
        out.write("PROJECT STRUCTURE:\n")
        out.write("================================================\n")
        out.write(f"Root: {root_path.name}\n")
        out.write(get_tree(root_path))
        out.write("================================================\n\n")

        # 2. Собираем содержимое файлов
        for path in root_path.rglob("*.swift"):
            # Проверка, не находится ли файл в игнорируемой папке
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            
            relative_path = path.relative_to(root_path)
            
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

    args = parser.parse_args()
    pack_project(args.input, args.output)