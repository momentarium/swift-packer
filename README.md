# Swift-Packer CLI 📦

Choose your language:

* [English](#english)
* [Русский](#русский)

## English

Swift-Packer is a simple command-line utility for iOS developers that bundles Swift source files and common text-based project assets into a single text file.

This tool is specifically designed for preparing context when working with LLMs (ChatGPT, Claude, and others), allowing you to pass the entire project in one file while preserving folder structure and file location context.

> Русская версия: [Русский](#русский)

## Features

* 📂 Project Tree Generation: Creates a visual directory structure at the beginning of the file.
* 🧹 Smart Filtering: Automatically ignores `Pods`, `DerivedData`, `.git`, `build`, and other system folders.
* 🎯 Custom Exclusions: Exclude any additional files or folders using glob patterns or exact relative paths (for example `Mocks`, `*.generated.swift`, `Views/Legacy/*`, or `StoreSync/Localizable.xcstrings`).
* 🎨 Markdown Highlighting: Included files are wrapped in fenced code blocks with a language hint, such as `swift` for Swift sources and `text` for other text-based assets.
* 🧩 Lightweight: Written in pure Python, requires no external dependencies.

## Installation

To use the utility as a system command from any folder:

1. Make sure you have the `packer.py` file.
2. Move the file

```
mv packer.py /usr/local/bin/swift-pack
```

3. Make the file executable:

```
chmod +x packer.py
```

## Usage

Simply navigate to the root folder of your Swift project and run:

```
swift-pack
```

### Additional Parameters

* Specify the project path (if you're not in its folder):

```
swift-pack /path/to/your/project
```

* Change the output file name:

```
swift-pack . -o my_project_context.txt
```

* Exclude specific files or folders from the result:

```
swift-pack . -e Mocks
```

* Exclude multiple patterns at once:

```
swift-pack . -e Mocks "*.generated.swift" "Views/Legacy/*"
```

* Exclude a specific file by relative path:

```
swift-pack . -e StoreSync/Localizable.xcstrings
```

## Example Output

The resulting file project_bundle.txt will look like this:

```
PROJECT STRUCTURE:
================================================
Root: MyApp
├── Models/
│   └── User.swift
├── Views/
│   └── MainView.swift
└── AppDelegate.swift
================================================

--- FILE START: Models/User.swift ---
```swift
struct User {
    let name: String
}
--- FILE END: Models/User.swift ---

```

## Tips for Working with ChatGPT / Claude

After generating the file, simply drag the resulting `.txt` file into the chat window and use the following prompt:

```
I have uploaded a file with my project's code. The file begins with a folder structure for understanding the architecture. Analyze this code and [your question: for example, find memory leaks or suggest refactoring].
```

or in Russian:

```
Я загрузил файл с кодом моего проекта. В начале файла приведена структура папок для понимания архитектуры. Проанализируй этот код и [твой вопрос: например, найди утечки памяти или предложи рефакторинг]
```

## Default Exclusions

The script automatically skips the following folders to save tokens:

* `.git`, `Pods`, `.build`, `DerivedData`
* `build`, `tests`, `Fastlane`
* `.xcodeproj`, `.xcworkspace`

## Custom Exclusions (`-e` / `--exclude`)

Beyond the default exclusions, you can exclude any additional files or directories using the `-e` (or `--exclude`) flag. It accepts one or more patterns and works on:

* File or folder **names**, e.g. `-e Mocks` will exclude any file or folder named `Mocks` at any level of the project.
* **Wildcards**, e.g. `-e "*.generated.swift"` will exclude all files ending in `.generated.swift`.
* **Relative paths**, e.g. `-e "Views/Legacy/*"` will exclude everything inside `Views/Legacy/`, and `-e "StoreSync/Localizable.xcstrings"` will exclude that exact file.

Excluded folders and files are also removed from the project tree at the top of the output file (empty folders left over after filtering won't be shown either).

Examples:

```
# Exclude a single folder anywhere in the project
swift-pack . -e Mocks

# Exclude generated files
swift-pack . -e "*.generated.swift"

# Exclude a specific nested folder
swift-pack . -e "Views/Legacy/*"

# Exclude a concrete file by relative path
swift-pack . -e "StoreSync/Localizable.xcstrings"

# Combine several patterns at once
swift-pack . -e Mocks "*.generated.swift" "Views/Legacy/*" "*Tests.swift"
```
## Supported Files
Supported bundle content includes common source and text-based resource files such as `.swift`, `.strings`, `.xcstrings`, `.plist`, `.json`, `.yaml`, `.yml`, `.xml`, and similar text files.

> ⚠️ Tip: quote patterns that contain `*` (e.g. `"*.generated.swift"`) so your shell doesn't try to expand them itself.

Created for convenient Swift development 🚀
## Русский

> English version: [English](#english)

Swift-Packer — это простой инструмент командной строки для iOS-разработчиков, который упаковывает Swift-файлы и текстовые проектные ресурсы в один текстовый файл.

Этот инструмент специально создан для подготовки контекста при работе с LLM (ChatGPT, Claude и другими), позволяя передать весь проект в одном файле с сохранением структуры папок и расположения файлов.

## Возможности

* 📂 Генерация структуры проекта: создает визуальное дерево каталогов в начале файла.
* 🧹 Умная фильтрация: автоматически исключает `Pods`, `DerivedData`, `.git`, `build` и другие системные папки.
* 🎯 Пользовательские исключения: можно исключать дополнительные файлы и папки с помощью glob-паттернов или точных относительных путей (например, `Mocks`, `*.generated.swift`, `Views/Legacy/*` или `StoreSync/Localizable.xcstrings`).
* 🎨 Подсветка Markdown: включенные файлы оборачиваются в блоки кода с указанием языка, например `swift` для Swift-исходников и `text` для других текстовых ресурсов.
* 🧩 Легковесность: написано на чистом Python, не требует внешних зависимостей.

## Установка

Чтобы использовать утилиту как системную команду из любой папки:

1. Убедитесь, что файл `packer.py` находится в каталоге.
2. Переместите файл:

```
mv packer.py /usr/local/bin/swift-pack
```

3. Сделайте файл исполняемым:

```
chmod +x packer.py
```

## Использование

Просто перейдите в корневую папку вашего Swift-проекта и выполните:

```
swift-pack
```

### Дополнительные параметры

* Укажите путь к проекту, если вы не находитесь в его папке:

```
swift-pack /path/to/your/project
```

* Измените имя выходного файла:

```
swift-pack . -o my_project_context.txt
```

* Исключите конкретные файлы или папки из результата:

```
swift-pack . -e Mocks
```

* Исключите несколько паттернов одновременно:

```
swift-pack . -e Mocks "*.generated.swift" "Views/Legacy/*"
```

* Исключите конкретный файл по относительному пути:

```
swift-pack . -e StoreSync/Localizable.xcstrings
```

## Пример результата

Файл `project_bundle.txt` будет выглядеть примерно так:

```
PROJECT STRUCTURE:
================================================
Root: MyApp
├── Models/
│   └── User.swift
├── Views/
│   └── MainView.swift
└── AppDelegate.swift
================================================

--- FILE START: Models/User.swift ---
```swift
struct User {
    let name: String
}
--- FILE END: Models/User.swift ---
```

## Советы для работы с ChatGPT / Claude

После генерации файла просто перетащите полученный `.txt` в окно чата и используйте следующий запрос:

```
Я загрузил файл с кодом моего проекта. В начале файла приведена структура папок для понимания архитектуры. Проанализируй этот код и [твой вопрос: например, найди утечки памяти или предложи рефакторинг]
```

## Исключения по умолчанию

Скрипт автоматически пропускает следующие папки, чтобы экономить токены:

* `.git`, `Pods`, `.build`, `DerivedData`
* `build`, `tests`, `Fastlane`
* `.xcodeproj`, `.xcworkspace`

## Пользовательские исключения (`-e` / `--exclude`)

Помимо исключений по умолчанию, вы можете исключать дополнительные файлы или папки с помощью флага `-e` (или `--exclude`). Он принимает один или несколько шаблонов и работает с:

* Именами файлов или папок, например `-e Mocks` исключит любой файл или папку с именем `Mocks` на любом уровне проекта.
* Подстановочными символами, например `-e "*.generated.swift"` исключит все файлы, оканчивающиеся на `.generated.swift`.
* Относительными путями, например `-e "Views/Legacy/*"` исключит всё внутри `Views/Legacy/`, а `-e "StoreSync/Localizable.xcstrings"` — конкретный файл.

Исключенные папки и файлы также удаляются из дерева проекта в начале выходного файла (пустые папки после фильтрации не отображаются).

Примеры:

```
# Исключить одну папку на любом уровне проекта
swift-pack . -e Mocks

# Исключить сгенерированные файлы
swift-pack . -e "*.generated.swift"

# Исключить конкретную вложенную папку
swift-pack . -e "Views/Legacy/*"

# Исключить конкретный файл по относительному пути
swift-pack . -e "StoreSync/Localizable.xcstrings"

# Объединить несколько шаблонов одновременно
swift-pack . -e Mocks "*.generated.swift" "Views/Legacy/*" "*Tests.swift"
```

## Поддерживаемые файлы

Поддерживаются общие исходные и текстовые ресурсы, такие как `.swift`, `.strings`, `.xcstrings`, `.plist`, `.json`, `.yaml`, `.yml`, `.xml` и похожие текстовые файлы.

> ⚠️ Совет: заключайте шаблоны с `*` в кавычки (например, "*.generated.swift"), чтобы оболочка не пыталась расширить их.

Создано для удобной разработки на Swift 🚀