Swift-Packer CLI 📦

Swift-Packer is a simple command-line utility for iOS developers that bundles all source code from a Swift project into a single text file.

This tool is specifically designed for preparing context when working with LLMs (ChatGPT, Claude, and others), allowing you to pass the entire project in one file while preserving folder structure and file location context.

✨ Features

* 📂 Project Tree Generation: Creates a visual directory structure at the beginning of the file.
* 🧹 Smart Filtering: Automatically ignores `Pods`, `DerivedData`, `.git`, `build`, and other system folders.
* 🎯 Custom Exclusions: Exclude any additional files or folders using glob patterns (e.g. `Mocks`, `*.generated.swift`, `Views/Legacy/*`).
* 🎨 Markdown Highlighting: All code in the output file is wrapped in ````swift` blocks, helping neural networks better understand the syntax.
* 🧩 Lightweight: Written in pure Python, requires no external dependencies.

🚀 Installation

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

📖 Usage

Simply navigate to the root folder of your Swift project and run:

```
swift-pack
```

Additional Parameters

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

📋 Example Output

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

💡 Tip for Working with ChatGPT / Claude

After generating the file, simply drag the resulting `.txt` file into the chat window and use the following prompt:

I have uploaded a file with my project's code. The file begins with a folder structure for understanding the architecture. Analyze this code and [your question: for example, find memory leaks or suggest refactoring].

or in Russian:

Я загрузил файл с кодом моего проекта. В начале файла приведена структура папок для понимания архитектуры. Проанализируй этот код и [твой вопрос: например, найди утечки памяти или предложи рефакторинг]

🛠 Default Exclusions

The script automatically skips the following folders to save tokens:

* `.git`, `Pods`, `.build`, `DerivedData`
* `build`, `tests`, `Fastlane`
* `.xcodeproj`, `.xcworkspace`

🎯 Custom Exclusions (`-e` / `--exclude`)

Beyond the default exclusions, you can exclude any additional files or directories using the `-e` (or `--exclude`) flag. It accepts one or more glob-style patterns and works on:

* File or folder **names**, e.g. `-e Mocks` will exclude any file or folder named `Mocks` at any level of the project.
* **Wildcards**, e.g. `-e "*.generated.swift"` will exclude all files ending in `.generated.swift`.
* **Relative paths**, e.g. `-e "Views/Legacy/*"` will exclude everything inside `Views/Legacy/`.

Excluded folders are also removed from the project tree at the top of the output file (empty folders left over after filtering won't be shown either).

Examples:

```
# Exclude a single folder anywhere in the project
swift-pack . -e Mocks

# Exclude generated files
swift-pack . -e "*.generated.swift"

# Exclude a specific nested folder
swift-pack . -e "Views/Legacy/*"

# Combine several patterns at once
swift-pack . -e Mocks "*.generated.swift" "Views/Legacy/*" "*Tests.swift"
```

> ⚠️ Tip: quote patterns that contain `*` (e.g. `"*.generated.swift"`) so your shell doesn't try to expand them itself.

Created for convenient Swift development 🚀
