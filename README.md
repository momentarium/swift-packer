# Swift-Packer CLI 📦

**Swift-Packer** is a simple command-line utility for iOS developers that bundles all source code from a Swift project into a single text file.

This tool is specifically designed for preparing context when working with LLMs (ChatGPT, Claude, and others), allowing you to pass the entire project in one file while preserving folder structure and file location context.

## ✨ Features

- 📂 **Project Tree Generation**: Creates a visual directory structure at the beginning of the file.
- 🧹 **Smart Filtering**: Automatically ignores `Pods`, `DerivedData`, `.git`, `build`, and other system folders.
- 🎨 **Markdown Highlighting**: All code in the output file is wrapped in ` ```swift ` blocks, helping neural networks better understand the syntax.
- 🧩 **Lightweight**: Written in pure Python, requires no external dependencies.

## 🚀 Installation

To use the utility as a system command from any folder:

1. Make sure you have the `packer.py` file.
2. Move the file
   ```bash
   mv packer.py /usr/local/bin/swift-pack
   ```
3. Make the file executable:
   ```bash
   chmod +x packer.py
   ```

## 📖 Usage
Simply navigate to the root folder of your Swift project and run:

```bash
swift-pack
```

### Additional Parameters
* Specify the project path (if you're not in its folder):

```bash
swift-pack /path/to/your/project
```

* Change the output file name:

```bash
swift-pack . -o my_project_context.txt
```

## 📋 Example Output
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

## 💡 Tip for Working with ChatGPT / Claude

After generating the file, simply drag the resulting `.txt` file into the chat window and use the following prompt:

> I have uploaded a file with my project's code. The file begins with a folder structure for understanding the architecture. Analyze this code and [your question: for example, find memory leaks or suggest refactoring].
or in Russian:
> Я загрузил файл с кодом моего проекта. В начале файла приведена структура папок для понимания архитектуры. Проанализируй этот код и [твой вопрос: например, найди утечки памяти или предложи рефакторинг]

## 🛠 Default Exclusions
The script automatically skips the following folders to save tokens:
- `.git`, `Pods`, `.build`, `DerivedData`
- `build`, `tests`, `Fastlane`
- `.xcodeproj`, `.xcworkspace`

---
Created for convenient Swift development 🚀
